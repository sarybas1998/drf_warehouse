from storages.backends.s3boto3 import S3Boto3Storage
# from minio import Minio
# from minio.error import S3Error
# from django.conf import settings


class MediaStorage(S3Boto3Storage):
    location = 'media'
    file_overwrite = False

    def url(self, name, parameters=None, expire=None):
        url = super().url(name, parameters, expire)
        if '?' in url:
            url = url.split('?')[0]
        return url


# class MinioStorage:
#     def __init__(self):
#         # Initialize MinIO client
#         self.client = Minio(
#             endpoint=settings.MINIO_STORAGE_ENDPOINT,  # MinIO server URL
#             access_key=settings.MINIO_STORAGE_ACCESS_KEY,
#             secret_key=settings.MINIO_STORAGE_SECRET_KEY,
#             secure=False,  # Set to True if you're using SSL
#             # cert_check=False
#         )
#
#     def list_objects(self):
#         """
#         List all objects in a MinIO bucket using the MinIO SDK.
#         """
#         try:
#             # List objects in the bucket
#             objects = self.client.list_objects(bucket_name=settings.MINIO_STORAGE_MEDIA_BUCKET_NAME, recursive=True)
#             object_list = []
#
#             for obj in objects:
#                 object_list.append({
#                     'name': obj.object_name,
#                     'size': obj.size,
#                     'last_modified': obj.last_modified
#                 })
#             return len(object_list), object_list
#         except S3Error as e:
#             return []
