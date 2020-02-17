from .default import *  # noqa
import django_heroku

DEBUG = False

# To upload your media files to S3
DEFAULT_FILE_STORAGE = "utils.content_manager.aws_S3.S3Storage"

# allow django-admin.py collectstatic to automatically put
# your static files in your bucket set the following in your settings.py
STATICFILES_STORAGE = "utils.content_manager.aws_S3.S3Storage"
