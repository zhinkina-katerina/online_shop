from rest_framework import status
from rest_framework.exceptions import PermissionDenied


class CartNotFoundException(PermissionDenied):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "There is no cart with this number"
    default_code = 'invalid'


class NotSpecifiedCartHex(PermissionDenied):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Parameter not specified cart_hex"
    default_code = 'invalid'
