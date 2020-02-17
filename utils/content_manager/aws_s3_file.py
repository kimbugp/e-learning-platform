import os
from tempfile import SpooledTemporaryFile

from botocore.exceptions import ClientError
from django.utils.deconstruct import deconstructible
from django.utils.encoding import force_bytes, force_text
from django.core.files import File
from .aws_utils import setting


@deconstructible
class S3StorageFile(File):

    """
    The default file object used by the S3Boto3Storage backend.
    This file implements file streaming using boto's multipart
    uploading functionality. The file can be opened in read or
    write mode.
    This class extends Django's File class. However, the contained
    data is only the data contained in the current buffer. So you
    should not access the contained file object directly. You should
    access the data via this class.
    """

    buffer_size = setting("AWS_S3_FILE_BUFFER_SIZE", 5242880)

    def __init__(self, name, mode, storage, buffer_size=None):
        if "r" in mode and "w" in mode:
            raise ValueError("Can't combine 'r' and 'w' in mode.")
        self._storage = storage
        self.name = name[len(self._storage.region_name) :].lstrip("/")
        self._mode = mode
        self._force_mode = (lambda b: b) if "b" in mode else force_text
        self.obj = storage.bucket.Object(storage._encode_name(name))
        if "w" not in mode:
            self.obj.load()
        self._is_dirty = False
        self._raw_bytes_written = 0
        self._file = None
        self._multipart = None
        if buffer_size is not None:
            self.buffer_size = buffer_size
        self._write_counter = 0

    @property
    def size(self):
        return self.obj.content_length

    def _get_file(self):
        if self._file is None:
            self._file = SpooledTemporaryFile(
                max_size=self._storage.max_memory_size,
                suffix=".S3Boto3StorageFile",
                dir=setting("FILE_UPLOAD_TEMP_DIR"),
            )
            if "r" in self._mode:
                self._is_dirty = False
                self.obj.download_fileobj(self._file)
                self._file.seek(0)
        return self._file

    def _set_file(self, value):
        self._file = value

    file = property(_get_file, _set_file)

    def read(self, *args, **kwargs):
        if "r" not in self._mode:
            raise AttributeError("File was not opened in read mode.")
        return self._force_mode(super().read(*args, **kwargs))

    def readline(self, *args, **kwargs):
        if "r" not in self._mode:
            raise AttributeError("File was not opened in read mode.")
        return self._force_mode(super().readline(*args, **kwargs))

    def write(self, content):
        if "w" not in self._mode:
            raise AttributeError("File was not opened in write mode.")
        self._is_dirty = True
        if self._multipart is None:
            self._multipart = self.obj.initiate_multipart_upload(
                **self._storage._get_write_parameters(self.obj.key)
            )
        if self.buffer_size <= self._buffer_file_size:
            self._flush_write_buffer()
        bstr = force_bytes(content)
        self._raw_bytes_written += len(bstr)
        return super().write(bstr)

    @property
    def _buffer_file_size(self):
        pos = self.file.tell()
        self.file.seek(0, os.SEEK_END)
        length = self.file.tell()
        self.file.seek(pos)
        return length

    def _flush_write_buffer(self):
        """
        Flushes the write buffer.
        """
        if self._buffer_file_size:
            self._write_counter += 1
            self.file.seek(0)
            part = self._multipart.Part(self._write_counter)
            part.upload(Body=self.file.read())
            self.file.seek(0)
            self.file.truncate()

    def _create_empty_on_close(self):
        """
        Attempt to create an empty file for this key when this File is closed if no bytes
        have been written and no object already exists on S3 for this key.
        This behavior is meant to mimic the behavior of Django's builtin FileSystemStorage,
        where files are always created after they are opened in write mode:
            f = storage.open("file.txt", mode="w")
            f.close()
        """
        assert "w" in self._mode
        assert self._raw_bytes_written == 0

        try:
            # Check if the object exists on the server; if so, don't do anything
            self.obj.load()
        except ClientError as err:
            if err.response["ResponseMetadata"]["HTTPStatusCode"] == 404:
                self.obj.put(
                    Body=b"",
                    **self._storage._get_write_parameters(self.obj.key)
                )
            else:
                raise

    def close(self):
        if self._is_dirty:
            self._flush_write_buffer()
            parts = [
                {"ETag": part.e_tag, "PartNumber": part.part_number}
                for part in self._multipart.parts.all()
            ]
            self._multipart.complete(MultipartUpload={"Parts": parts})
        else:
            if self._multipart is not None:
                self._multipart.abort()
            if "w" in self._mode and self._raw_bytes_written == 0:
                self._create_empty_on_close()
        if self._file is not None:
            self._file.close()
            self._file = None
