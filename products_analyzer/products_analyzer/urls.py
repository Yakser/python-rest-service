from django.contrib import admin
from django.urls import include, path
from shop_unit.views import ShopUnitDetail, ShopUnitDelete, ShopUnitList, ShopUnitImports


urlpatterns = [
    path('imports/', ShopUnitImports.as_view(), name='shopunit-imports'),
    path('nodes/', ShopUnitList.as_view(), name='shopunit-detail'),
    path('nodes/<uuid:pk>/', ShopUnitDetail.as_view(), name='shopunit-detail'),
    path('delete/<uuid:pk>/', ShopUnitDelete.as_view(), name='shopunit-delete'),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
]
