# from django.conf import settings
# from rest_framework import viewsets
# from rest_framework.decorators import action
#
# from recipe_house_backend.common.utils.helper import (
#     s3_helper,
#     make_validation_dict
# )
# from recipe_house_backend.common.utils.response_helper import (
#     create_http_response,
#     create_internal_response,
#     Status,
# )
#
#
# class FileUploadViewset(viewsets.ViewSet):
#
#     @action(methods=['GET'], detail=False)
#     def presigned_url(self, request):
#         object_name = request.query_params.get('key')
#
#         validation = make_validation_dict(request.query_params, 'key', )
#         if validation:
#             response = create_internal_response(Status.badrequest, validation)
#             return create_http_response(response)
#         bucket_name = settings.S3_DEFAULT_BUCKET_NAME
#         key_prefix = 'Organization'
#         presigned_url = s3_helper.create_presigned_url(bucket_name, object_name, key_prefix)
#
#         response = create_internal_response(Status.ok, {'presigned_url': presigned_url})
#         return create_http_response(response)
