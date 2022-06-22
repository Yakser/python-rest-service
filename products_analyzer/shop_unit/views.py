from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from shop_unit.errors import (ITEM_NOT_FOUND_RESPONSE, OK_RESPONSE,
                              VALIDATION_FAILED_RESPONSE)
from shop_unit.helpers import format_shop_unit_data, build_tree
from shop_unit.models import ShopUnit
from shop_unit.serializers import ShopUnitSerializer
from shop_unit.types import ShopUnitTypes
from shop_unit.validators import (validate_date, validate_parent,
                                  validate_shop_unit, validate_type)


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

            serializer = ShopUnitSerializer(shop_unit,
                                            context={'request': request})

            data = format_shop_unit_data(shop_unit, serializer.data)

            if shop_unit.type == ShopUnitTypes.CATEGORY.name:
                data['children'] = build_tree(shop_unit, request)

            return Response(data)

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
            update_date = data.get('updateDate', '')
            validate_date(update_date)
            items = data['items']

            for item in items:
                validate_shop_unit(item)

                if item.get('parentId', None):
                    parent = ShopUnit.objects.get(id=item.get('parentId', None))
                    validate_parent(parent)
                else:
                    parent = None

                id_ = item.get('id', '')
                name = item.get('name', '')
                type_ = item.get('type', '')
                price = item.get('price', None)

                units = ShopUnit.objects.filter(id=id_)

                if units:
                    unit = units.first()
                    if name:
                        unit.name = name

                    if type_ != unit.type:
                        validate_type(type_, is_new_instance=False)

                    if price:
                        unit.price = price

                else:
                    validate_type(type_)

                    unit = ShopUnit(id=id_,
                                    name=name,
                                    type=type_,
                                    parent=parent,
                                    date=update_date,
                                    price=price)
                unit.save()

            return OK_RESPONSE

        except AssertionError as e:
            print(e)
            return VALIDATION_FAILED_RESPONSE
