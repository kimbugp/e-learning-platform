import mimetypes
import os
import posixpath
import threading

import boto3.session
from botocore.exceptions import ClientError
from django.core.files.storage import Storage
from django.utils.deconstruct import deconstructible
from django.utils.encoding import force_text, smart_text, filepath_to_uri

from .aws_utils import get_available_overwrite_name, setting
from .aws_s3_file import S3StorageFile


@deconstructible
class S3Storage(Storage):
    """
    Amazon Simple Storage Service using Boto3
    """

    default_content_type = "application/octet-stream"
    access_key = setting("AWS_ACCESS_KEY_ID")
    secret_key = setting("AWS_SECRET_ACCESS_KEY")
    file_overwrite = setting("AWS_S3_FILE_OVERWRITE", True)
    object_parameters = setting("AWS_S3_OBJECT_PARAMETERS", {})
    bucket_name = setting("AWS_STORAGE_BUCKET_NAME")
    file_name_charset = setting("AWS_S3_FILE_NAME_CHARSET", "utf-8")
    url_protocol = setting("AWS_S3_URL_PROTOCOL", "http:")
    endpoint_url = setting("AWS_S3_ENDPOINT_URL")
    region_name = setting("AWS_S3_REGION_NAME")
    use_ssl = setting("AWS_S3_USE_SSL", True)
    max_memory_size = setting("AWS_S3_MAX_MEMORY_SIZE", 0)
    location = setting("AWS_LOCATION", "")
    preload_metadata = True
    custom_domain = setting("AWS_CUSTOM_DOMAIN", None)
    default_acl = setting("AWS_DEFAULT_ACL", "public-read")
    expire = setting("AWS_URL_EXPIRE", 3600)

    def __init__(self, bucket=None, region_name=None, **settings):
        for name, value in settings.items():
            if hasattr(self, name):
                setattr(self, name, value)
        if bucket:
            self.bucket_name = bucket
        self._entries = {}
        self._bucket = None
        self._session = None
        self._region_name = setting("AWS_REGION_NAME")
        self._connections = threading.local()

    @property
    def region_name(self):
        if self._region_name is None:
            self._region_name = self._get_region_name()
        return self._region_name

    def _get_region_name(self):
        session = self.get_session()
        return session.region_name

    def __getstate__(self):
        state = self.__dict__.copy()
        state.pop("_connections", None)
        state.pop("_bucket", None)
        return state

    def __setstate__(self, state):
        state["_connections"] = threading.local()
        state["_bucket"] = None
        self.__dict__ = state

    @property
    def connection(self):
        connection = getattr(self._connections, "connection", None)
        if connection is None:
            session = self.get_session()
            self._connections.connection = session.resource(
                "s3",
                aws_access_key_id=self.access_key,
                aws_secret_access_key=self.secret_key,
                region_name=self.region_name,
                use_ssl=self.use_ssl,
                endpoint_url=self.endpoint_url,
            )
        return self._connections.connection

    def get_session(self):
        if not self._session:
            self._session = boto3.session.Session()
        return self._session

    @property
    def bucket(self):
        if self._bucket is None:
            self._bucket = self._get_bucket(self.bucket_name)
        return self._bucket

    @property
    def entries(self):
        """
        Get the locally cached files for the bucket.
        """
        if self.preload_metadata and not self._entries:
            self._entries = {
                self._decode_name(entry.key): entry
                for entry in self.bucket.objects.filter(Prefix=self.location)
            }
        return self._entries

    def _get_bucket(self, name):
        bucket = self.connection.Bucket(name)
        return bucket

    def _clean_name(self, name):
        """
        Cleans the name so that Windows style paths work
        """
        # Normalize Windows style paths
        clean_name = posixpath.normpath(name).replace("\\", "/")

        # os.path.normpath() can strip trailing slashes so we implement
        # a workaround here.
        if name.endswith("/") and not clean_name.endswith("/"):
            # Add a trailing slash as it was stripped.
            clean_name += "/"
        return clean_name

    def _normalize_name(self, *name):
        """
        Normalizes the name so that paths like /path/to/file/../example.txt
        We check to make sure that the path pointed to is not outside
        the directory specified by the LOCATION setting.
        """
        base_path = force_text(self.location)
        base_path = base_path.rstrip("/")
        paths = [force_text(p) for p in name]

        final_path = base_path + "/"
        for path in paths:
            _final_path = posixpath.normpath(posixpath.join(final_path, path))
            if path.endswith("/") or _final_path + "/" == final_path:
                _final_path += "/"
            final_path = _final_path

        if final_path == base_path:
            final_path += "/"

        base_path_len = len(base_path)
        if (
            not final_path.startswith(base_path)
            or final_path[base_path_len] != "/"
        ):
            raise ValueError(
                "the joined path is located outside of the base path"
                " component"
            )
        return final_path.lstrip("/")

    def _encode_name(self, name):
        return smart_text(name, encoding=self.file_name_charset)

    def _decode_name(self, name):
        return force_text(name, encoding=self.file_name_charset)

    def _open(self, name, mode="rb"):
        name = self._normalize_name(self._clean_name(name))
        try:
            f = S3StorageFile(name, mode, self)
        except ClientError as err:
            if err.response["ResponseMetadata"]["HTTPStatusCode"] == 404:
                raise IOError("File does not exist: %s" % name)
            raise  # Let it bubble up if it was some other error
        return f

    def _save(self, name, content):
        cleaned_name = self._clean_name(name)
        name = self._normalize_name(cleaned_name)
        params = self._get_write_parameters(name, content)

        encoded_name = self._encode_name(name)
        obj = self.bucket.Object(encoded_name)
        if self.preload_metadata:
            self._entries[encoded_name] = obj

        content.seek(0, os.SEEK_SET)
        obj.upload_fileobj(content, ExtraArgs=params)
        return cleaned_name

    def delete(self, name):
        name = self._normalize_name(self._clean_name(name))
        self.bucket.Object(self._encode_name(name)).delete()

        if name in self._entries:
            del self._entries[name]

    def exists(self, name):
        name = self._normalize_name(self._clean_name(name))
        if self.entries:
            return name in self.entries
        try:
            self.connection.meta.client.head_object(
                Bucket=self.bucket_name, Key=name
            )
            return True
        except ClientError:
            return False

    def listdir(self, name):
        path = self._normalize_name(self._clean_name(name))
        # The path needs to end with a slash, but if the root is empty, leave
        # it.
        if path and not path.endswith("/"):
            path += "/"

        directories = []
        files = []
        paginator = self.connection.meta.client.get_paginator("list_objects")
        pages = paginator.paginate(
            Bucket=self.bucket_name, Delimiter="/", Prefix=path
        )
        for page in pages:
            for entry in page.get("CommonPrefixes", ()):
                directories.append(posixpath.relpath(entry["Prefix"], path))
            for entry in page.get("Contents", ()):
                files.append(posixpath.relpath(entry["Key"], path))
        return directories, files

    def size(self, name):
        name = self._normalize_name(self._clean_name(name))
        if self.entries:
            entry = self.entries.get(name)
            if entry:
                return (
                    entry.size
                    if hasattr(entry, "size")
                    else entry.content_length
                )
            return 0
        return self.bucket.Object(self._encode_name(name)).content_length

    def _get_write_parameters(self, name, content=None):
        params = {}
        if self.default_acl:
            params["ACL"] = self.default_acl

        _type, encoding = mimetypes.guess_type(name)
        content_type = getattr(content, "content_type", None)
        content_type = content_type or _type or self.default_content_type

        params["ContentType"] = content_type
        if encoding:
            params["ContentEncoding"] = encoding

        params.update(self.get_object_parameters(name))
        return params

    def get_object_parameters(self, name):
        return self.object_parameters.copy()

    def url(self, name, parameters=None):
        name = self._normalize_name(self._clean_name(name))
        if self.custom_domain:
            return "https://{}/{}".format(
                self.custom_domain, filepath_to_uri(name)
            )
        params = parameters.copy() if parameters else {}
        params["Bucket"] = self.bucket.name
        params["Key"] = self._encode_name(name)
        url = self.bucket.meta.client.generate_presigned_url(
            "get_object", Params=params, ExpiresIn=self.expire
        )
        return url

    def get_available_name(self, name, max_length=None):
        """Overwrite existing file with the same name."""
        name = self._clean_name(name)
        if self.file_overwrite:
            return get_available_overwrite_name(name, max_length)
        return super().get_available_name(name, max_length)
