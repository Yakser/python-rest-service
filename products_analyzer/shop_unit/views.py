from rest_framework import viewsets

from shop_unit.models import ShopUnit
from shop_unit.serializers import ShopUnitSerializer


class ShopUnitViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows ShopUnits to be viewed or edited.
    """
    queryset = ShopUnit.objects.all()
    serializer_class = ShopUnitSerializer
