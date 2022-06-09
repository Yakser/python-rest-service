
from rest_framework import status
from rest_framework.response import Response

OK_RESPONSE = Response(
    {
        'code': status.HTTP_200_OK,
        'message': 'ok'
    },
    status=status.HTTP_200_OK
)


ITEM_NOT_FOUND_RESPONSE = Response(
    {
        'code': status.HTTP_404_NOT_FOUND,
        'message': 'Item not found'
    },
    status=status.HTTP_404_NOT_FOUND
)


VALIDATION_FAILED_RESPONSE = Response(
    {
        'code': status.HTTP_400_BAD_REQUEST,
        'message': 'Validation Failed'
    },
    status=status.HTTP_400_BAD_REQUEST
)
