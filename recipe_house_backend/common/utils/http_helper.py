import json

import requests

from recipe_house_backend.common.utils.logger import get_logger
from recipe_house_backend.common.utils.response_helper import create_internal_response, Status

logger = get_logger()


def make_http_post_request(url, params, headers=None):
    return __perform_http_request(url, params, 'POST', headers)


def make_http_get_request(url, params, headers=None):
    return __perform_http_request(url, params, 'GET', headers)


def __perform_http_request(url, params, http_method, headers=None):
    logger.debug(" Params : %s", params)
    logger.debug(" url : %s", url)
    logger.debug(" headers : %s", headers)
    http_response = __execute_api_request(url, http_method, params, headers)
    logger.debug(http_response.content)
    response = __handle_http_response(http_response)

    return response


def __execute_api_request(url, request_method, request_params, headers=None):
    if request_method is "GET":
        response = requests.get(url=url,
                                params=request_params,
                                headers=headers
                                )
    elif request_method is "POST":
        response = requests.post(url=url,
                                 data=request_params,
                                 headers=headers)
    else:
        response = requests.request(method=request_method,
                                    url=url,
                                    data=request_params,
                                    headers=headers)
    return response


def __handle_http_response(response):
    allowed_status_codes = [400, 401, 200]
    logger.debug(response.status_code)
    logger.debug(response.content)
    logger.debug(str(response.headers['content-type']))

    if response.status_code in allowed_status_codes:
        if str(response.headers['content-type'] == "text/json"):
            return create_internal_response(__get_internal_code(response.status_code), json.loads(response.content))
        else:
            return create_internal_response(__get_internal_code(response.status_code), response.content)
    else:
        logger.error("Non 200 response received from server , received status code is  %s",
                     response.status_code)
        logger.error("Error Details : %s", response)
        return None


def __get_internal_code(status_code):
    code_mapping = {
        400: Status.badrequest,
        401: Status.un_authenticated,
        200: Status.ok
    }
    return code_mapping.get(status_code)
