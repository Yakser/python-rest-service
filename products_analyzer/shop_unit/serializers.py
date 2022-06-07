from shop_unit.models import ShopUnit
from rest_framework import serializers


class ShopUnitSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = ShopUnit
        fields = ['id', 'name', 'date', 'parent', 'type', 'price']
