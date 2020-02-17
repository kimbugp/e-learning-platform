import os

from django.conf import settings
from django.core.exceptions import SuspiciousFileOperation


def setting(name, default=None):
    """ Function to get a Django setting by name. If setting doesn't exists
    it will return a default.
    
    Args:
        name (str): Name of setting
        default (obj, optional): Value if setting is unfound. Defaults to None.
    
    Returns:
        obj: Setting's value
    """
    return getattr(settings, name, default)


def get_available_overwrite_name(name, max_length):
    if max_length is None or len(name) <= max_length:
        return name

    # Adapted from Django
    dir_name, file_name = os.path.split(name)
    file_root, file_ext = os.path.splitext(file_name)
    truncation = len(name) - max_length

    file_root = file_root[:-truncation]
    if not file_root:
        raise SuspiciousFileOperation(
            'Storage tried to truncate away entire filename "%s". '
            "Please make sure that the corresponding file field "
            'allows sufficient "max_length".' % name
        )
    return os.path.join(dir_name, "{}{}".format(file_root, file_ext))
