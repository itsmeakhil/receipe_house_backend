from rest_framework import status
from rest_framework.response import Response


def http_200(message, data):
    return Response({'status': 200, 'message': message, 'data': data},
                    status=status.HTTP_200_OK)


def http_200_message(message):
    return Response({'status': 200, 'message': message},
                    status=status.HTTP_200_OK)


def http_201(message, data):
    return Response({'status': 200, 'message': message, 'data': data},
                    status=status.HTTP_200_OK)


def http_204(message):
    return Response({'status': 204, 'message': message}, status=status.HTTP_204_NO_CONTENT)


def http_400(message, error):
    return Response({'status': 400, 'message': message, 'error': error},
                    status=status.HTTP_400_BAD_REQUEST)


def http_400_message(message):
    return Response({'status': 400, 'message': message},
                    status=status.HTTP_400_BAD_REQUEST)


def http_403(error_message):
    return Response({'status': 403, 'message': error_message}, status=status.HTTP_403_FORBIDDEN)


def http_404(error_message):
    return Response({'status': 404, 'message': error_message}, status=status.HTTP_404_NOT_FOUND)


def http_409(error_message):
    return Response({'status': 409, 'message': error_message}, status=status.HTTP_409_CONFLICT)


def http_500(error, message):
    return Response({'status': 500, 'message': message, 'error': error.__str__()},
                    status.HTTP_500_INTERNAL_SERVER_ERROR)
