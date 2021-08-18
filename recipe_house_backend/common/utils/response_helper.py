import enum

from rest_framework import status
from rest_framework.response import Response

from recipe_house_backend.common.utils.logger import get_logger


class Status(enum.Enum):
    error = 500
    badrequest = 400
    ok = 200
    un_authenticated = 401
    not_found = 404


logger = get_logger()


def __generic_resposne(http_status: status, content):
    return Response(data=content,
                    status=http_status,
                    content_type='application/json')


def __generate_ok_response(content):
    return __generic_resposne(status.HTTP_200_OK, content)


def __generate_created_response(content):
    return __generic_resposne(status.HTTP_201_CREATED, content)


def __generate_internal_server_error_response(content):
    return __generic_resposne(status.HTTP_500_INTERNAL_SERVER_ERROR, content)


def __generate_badrequest_response(content):
    return __generic_resposne(status.HTTP_400_BAD_REQUEST, content)


def __generate_not_authenticated_response(content):
    return __generic_resposne(status.HTTP_401_UNAUTHORIZED, content)


def __generate_not_found_response(content):
    return __generic_resposne(status.HTTP_404_NOT_FOUND, content)


# response_generator_map = {
#     Status.ok: __generate_ok_response,
#     # Status.completed: __generate_created_response,
#     Status.badrequest: __generate_badrequest_response,
#     Status.un_authenticated: __generate_not_authenticated_response,
#     Status.error: __generate_internal_server_error_response,
#     Status.not_found: __generate_not_found_response
# }


response_generator_map_number = {
    200: __generate_ok_response,
    400: __generate_badrequest_response,
    401: __generate_not_authenticated_response,
    500: __generate_internal_server_error_response,
    404: __generate_not_found_response
}


def create_http_response(response):
    """
    This method will create a DRF HTTP response as per the internal response format
    :param response:
    :return:
    """
    logger.debug(response)
    handler = response_generator_map_number.get(response['status'], None)
    if handler:
        return handler(response['message'])
    else:
        logger.error("Un-mapped response  found %s", response)
        return __generate_internal_server_error_response({
            "error": "Internal Server error"
        })


def create_internal_response(response_status: Status, response_message):
    """
    This method will create Common response format to communicate between methods/class
    :param response_status:
    :param response_message:
    :return:
    """
    response = {'status': response_status.value}
    if response_status in [Status.error, Status.un_authenticated, Status.not_found, Status.badrequest]:
        response_message = {
            "error": response_message
        }

    response['message'] = response_message
    return response
