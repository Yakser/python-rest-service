from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from shop_unit.views import ShopUnitViewSet


router = routers.DefaultRouter()
router.register(r'nodes', ShopUnitViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
]
