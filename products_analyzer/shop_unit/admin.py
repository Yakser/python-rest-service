from django.contrib import admin

from shop_unit.models import ShopUnit


@admin.register(ShopUnit)
class ShopUnitAdmin(admin.ModelAdmin):
    list_display = ('name', 'date')
