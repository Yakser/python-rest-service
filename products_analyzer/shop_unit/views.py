from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from shop_unit.errors import (ITEM_NOT_FOUND_RESPONSE, OK_RESPONSE,
                              VALIDATION_FAILED_RESPONSE)
from shop_unit.helpers import calculate_category_price
from shop_unit.models import ShopUnit
from shop_unit.serializers import ShopUnitSerializer
from shop_unit.types import ShopUnitTypes
from shop_unit.validators import (validate_date, validate_parent,
                                  validate_shop_unit)


class ShopUnitList(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request, format=None):
        shop_units = ShopUnit.objects.all()
        serializer = ShopUnitSerializer(shop_units,
                                        many=True,
                                        context={'request': request})
        return Response(serializer.data)


class ShopUnitDetail(APIView):
    def get(self, request, pk, format=None):
        try:
            shop_unit = ShopUnit.objects.get(pk=pk)

            if shop_unit.type == ShopUnitTypes.CATEGORY.name:
                shop_unit.price = calculate_category_price(shop_unit)
                shop_unit.save()

            serializer = ShopUnitSerializer(shop_unit,
                                            context={'request': request})

            return Response(serializer.data)

        except ShopUnit.DoesNotExist as e:
            print(e)
            return ITEM_NOT_FOUND_RESPONSE

        except Exception as e:
            print(e)
            return VALIDATION_FAILED_RESPONSE


class ShopUnitDelete(APIView):
    def delete(self, request, pk, format=None):
        try:
            shop_unit = ShopUnit.objects.get(pk=pk)
            shop_unit.delete()
            return OK_RESPONSE

        except ShopUnit.DoesNotExist as e:
            print(e)
            return ITEM_NOT_FOUND_RESPONSE

        except Exception as e:
            print(e)
            return VALIDATION_FAILED_RESPONSE


class ShopUnitImports(APIView):
    def post(self, request, format=None):
        try:
            data = request.data
            validate_date(data.get('updateDate', ''))
            items = data['items']

            for item in items:
                validate_shop_unit(item)

                if item.get('parentId', None):
                    parent = ShopUnit.objects.get(id=item.get('parentId', None))
                    validate_parent(parent)
                else:
                    parent = None

                unit, _ = ShopUnit.objects.update_or_create(id=item.get('id', ''),
                                                            name=item.get('name', ''),
                                                            type=item.get('type', ''),
                                                            parent=parent,
                                                            date=item.get('updateDate', ''),
                                                            price=item.get('price', None))
                unit.save()

            return OK_RESPONSE

        except AssertionError as e:
            print(e)
            return VALIDATION_FAILED_RESPONSE
