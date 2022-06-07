from django.http import Http404
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from shop_unit.helpers import format_date
from shop_unit.models import ShopUnit
from shop_unit.serializers import ShopUnitSerializer


class BaseShopUnitView(APIView):
    def get_object(self, pk):
        try:
            return ShopUnit.objects.get(pk=pk)
        except ShopUnit.DoesNotExist:
            raise Http404


class ShopUnitList(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request, format=None):
        shop_units = ShopUnit.objects.all()
        serializer = ShopUnitSerializer(shop_units,
                                        many=True,
                                        context={'request': request})
        return Response(serializer.data)


class ShopUnitDetail(BaseShopUnitView):
    def get(self, request, pk, format=None):
        shop_unit = self.get_object(pk)
        serializer = ShopUnitSerializer(shop_unit,
                                        context={'request': request})
        return Response(serializer.data)


class ShopUnitDelete(BaseShopUnitView):
    def delete(self, request, pk, format=None):
        shop_unit = self.get_object(pk)
        shop_unit.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ShopUnitImports(APIView):
    def post(self, request, format=None):
        try:
            data = request.data
            items = data['items']
            update_date = format_date(data['updateDate'])

            # todo validation
            for item in items:

                parent = None
                if item['parentId']:
                    parent = ShopUnit.objects.get(id=item['parentId'])

                price = item.get('price', None)

                unit, created = ShopUnit.objects.update_or_create(id=item['id'],
                                                                  name=item['name'],
                                                                  type=item['type'],
                                                                  parent=parent,
                                                                  date=update_date,
                                                                  price=price)
                unit.save()

            return Response([
                200,
                'Вставка или обновление прошли успешно.'
            ])

        except Exception as e:
            # Would be nice to log error
            print(e)
            return Response([
                400,
                'Невалидная схема документа или входные данные не верны.'
            ])
