from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from shop_unit.helpers import calculate_category_price
from shop_unit.models import ShopUnit
from shop_unit.serializers import ShopUnitSerializer
from shop_unit.types import ShopUnitTypes
from shop_unit.validators import (validate_date, validate_id, validate_name,
                                  validate_type)


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

            serializer = ShopUnitSerializer(shop_unit,
                                            context={'request': request})

            return Response(serializer.data)

        except ShopUnit.DoesNotExist:
            return Response({
                'code': status.HTTP_404_NOT_FOUND,
                'message': 'Категория/товар не найден'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            return Response([
                status.HTTP_400_BAD_REQUEST,
                'Невалидная схема документа или входные данные не верны.'
            ], status=status.HTTP_400_BAD_REQUEST)


class ShopUnitDelete(APIView):
    def delete(self, request, pk, format=None):
        try:
            shop_unit = ShopUnit.objects.get(pk=pk)
            shop_unit.delete()
            return Response([status.HTTP_200_OK, 'Удаление прошло успешно.'],
                            status=status.HTTP_200_OK)
        except ShopUnit.DoesNotExist:
            # Would be nice to log error
            return Response({
                'code': status.HTTP_404_NOT_FOUND,
                'message': 'Категория/товар не найден'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            # Would be nice to log error
            print(e)
            return Response([
                status.HTTP_400_BAD_REQUEST,
                'Невалидная схема документа или входные данные не верны.'
            ], status=status.HTTP_400_BAD_REQUEST)


class ShopUnitImports(APIView):
    def post(self, request, format=None):
        try:
            data = request.data

            validate_date(data.get('updateDate', ''))

            items = data['items']

            for item in items:
                validate_type(item.get('type', ''))
                validate_name(item.get('name', ''))
                validate_id(item.get('id', ''))

                if item.get('parentId', None):
                    parent = ShopUnit.objects.get(id=item.get('parentId', None))
                else:
                    parent = None

                price = item.get('price', None)

                unit, created = ShopUnit.objects.update_or_create(id=item['id'],
                                                                  name=item['name'],
                                                                  type=item['type'],
                                                                  parent=parent,
                                                                  date=data['updateDate'],
                                                                  price=price)
                unit.save()

            return Response([
                status.HTTP_200_OK,
                'Вставка или обновление прошли успешно.'
            ])
        except AssertionError as e:
            # Would be nice to log error
            print(e)
            return Response([
                status.HTTP_400_BAD_REQUEST,
                'Невалидная схема документа или входные данные не верны.'
            ], status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            # Would be nice to log error
            print(e)
            return Response([
                status.HTTP_400_BAD_REQUEST,
                'Невалидная схема документа или входные данные не верны.'
            ], status=status.HTTP_400_BAD_REQUEST)
