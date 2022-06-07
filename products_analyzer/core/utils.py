from rest_framework.views import exception_handler
from rest_framework.viewsets import ModelViewSet

from shop_unit.views import ShopUnitViewSet


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        del response.data['detail']
        response.data['status_code'] = response.status_code
        response.data['message'] = 'Validation failed'
        # view: ModelViewSet = context['view']
        # TODO
        # print(view.__class__ == ShopUnitViewSet, '-----------')

    return response
