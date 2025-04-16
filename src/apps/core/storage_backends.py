from storages.backends.s3boto3 import S3Boto3Storage


class StaticStorage(S3Boto3Storage):
    """ S3 storage backend for serving statics on S3. """
    location = 'static'
    default_acl = 'public-read'


class PublicMediaStorage(S3Boto3Storage):
    """ S3 storage backend for serving media on S3. """
    location = 'media'
    default_acl = 'public-read'
    file_overwrite = False
