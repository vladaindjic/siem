import datetime
from calendar import timegm


def jwt_payload_handler(user):
    """ Custom payload handler
    Token encrypts the dictionary returned by this function, and can be decoded by rest_framework_jwt.utils.jwt_decode_handler
    """
    return {
        'id': user.pk,
        'email': user.email,
        'username': user.username,
        'is_superuser': user.is_superuser,
    }


def jwt_response_payload_handler(token, user=None, request=None):
    """ Custom response payload handler.

    This function controlls the custom payload after login or token refresh. This data is returned through the web API.
    """
    print(user)
    return {
        'token': token,
        'user': {
            'email': user.email,
            'username': user.username,
            'is_superuser': user.is_superuser,
        }
    }
