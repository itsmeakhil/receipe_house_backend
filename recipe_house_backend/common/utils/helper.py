import uuid
from ctypes import c_size_t
from datetime import datetime

import boto3
from botocore.client import Config
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework.renderers import JSONRenderer
from rest_framework.utils import json

from recipe_house_backend.common.db.elasticsearch.client import ElasticSearchClient

MESSAGE_FIELD_REQUIRED = "This field is required"


def make_validation_dict(data, *keys, **kwargs):
    """
    Usage:
    validation = make_validation_dict(request.query_params, 'key1', 'key2')
    """
    kwargs.setdefault('message', MESSAGE_FIELD_REQUIRED)
    v = {}
    for i in keys:
        if i in data and data[i]:
            continue
        v[i] = [kwargs['message']]
    return v


def get_dict_from_serializer(serializer_data):
    """
    To handle the nested serializer fields
    :param serializer_data:
    :return:
    """
    content = JSONRenderer().render(serializer_data)
    dict = json.loads(content)
    return dict


def get_value_or_none(dict, key):
    return dict.get(key) if key in dict else None


def connect_to_elasticsearch():
    """
    Function to check elastic search connection,
     if not connected throws environmental error.
    """
    es = ElasticSearchClient.get_client()
    if not es.ping():
        raise EnvironmentError(
            'Django server was unable to start due to, Error connecting to Elasticsearch ')  # noqa: E501


def encode_uid(pk):
    return force_str(urlsafe_base64_encode(force_bytes(pk)))


def decode_uid(pk):
    return force_str(urlsafe_base64_decode(pk))


def generate_user_token(user):
    return default_token_generator.make_token(user)

def check_user_token(user, token):
    return default_token_generator.check_token(user, token)

def generate_hash(data):
    """
    Function to create hash from object
    """
    return c_size_t(hash(json.dumps(data, indent=4, sort_keys=True, default=str))).value


def soft_delete_model_instance(instance, user=None):
    update_fields = []

    if hasattr(instance, 'is_deleted'):
        instance.is_deleted = True
        update_fields.append('is_deleted')

    if hasattr(instance, 'deleted_by'):
        instance.deleted_by = user
        update_fields.append('deleted_by')

    if hasattr(instance, 'deleted_on'):
        instance.deleted_on = datetime.now()
        update_fields.append('deleted_on')

    instance.save(update_fields=update_fields)


# # Helper class to aid aws s3 operations
# class S3Helper:
#     s3_client = boto3.client('s3',
#                              config=Config(signature_version='s3v4'),
#                              aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
#                              aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
#                              region_name=settings.S3_BUCKET_REGION
#                              )
#
#     def create_presigned_url(self, bucket_name, object_name, key_prefix):
#         """
#         Generate a presigned URL to share an S3 object
#         """
#         return self.s3_client.generate_presigned_url(
#             'put_object',
#             Params={
#                 'Bucket': bucket_name,
#                 'Key': "{}/{}/{}".format(key_prefix, uuid.uuid4().hex, object_name),
#                 'ACL': 'public-read-write',
#
#             },
#             ExpiresIn=604799,
#         )
#
#     def upload_public_file(self, file_path, bucket_name, object_name, key_prefix):
#         key = "{}/{}/{}".format(key_prefix, uuid.uuid4().hex, object_name)
#         self.s3_client.upload_file(file_path, bucket_name, key, ExtraArgs={'ACL': 'public-read'})
#         _s3_link = f"https://{bucket_name}.s3.{settings.S3_BUCKET_REGION}.amazonaws.com/{key}"
#         return _s3_link
#
#
# s3_helper = S3Helper()
