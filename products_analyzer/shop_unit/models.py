import uuid

from django.db import models

from shop_unit.types import ShopUnitTypes


class ShopUnit(models.Model):
    """
    Модель ShopUnit - категория или товар

    Attributes:
        id (UUIDField): Уникальный идентфикатор
        name (CharField): Имя
        date (DateTimeField): Время последнего обновления элемента
        parent (self): Родительская категория
        type (str): Тип элемента - категория или товар
        price (int): Целое число, для категории - это средняя цена всех дочерних\
                     товаров(включая товары подкатегорий). Если цена является не\
                     целым числом, округляется в меньшую сторону до целого числа.\
                     Если категория не содержит товаров цена равна null.
    """

    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4,
                          editable=False,
                          verbose_name='Идентфикатор')

    name = models.CharField(null=False,
                            verbose_name='Имя',
                            max_length=120)

    date = models.DateTimeField(null=False,
                                verbose_name='Время последнего обновления элемента')

    # todo
    # parent_id = models.UUIDField(null=True,
    #                              verbose_name='UUID родительской категории',
    #                              )

    parent = models.ForeignKey('self',
                               null=True,
                               verbose_name='Родительская категория',
                               related_name='children',
                               on_delete=models.CASCADE,
                               blank=True)

    type = models.CharField(null=False,
                            choices=ShopUnitTypes.to_choices(),
                            verbose_name='Тип элемента - категория или товар',
                            max_length=120)

    price = models.IntegerField(null=True,
                                verbose_name='Цена',
                                help_text='Целое число, для категории - это средняя цена\
                                    всех дочерних товаров(включая товары подкатегорий). \
                                        Если цена является не целым числом, округляется \
                                            в меньшую сторону до целого числа. Если категория\
                                                не содержит товаров цена равна null.',
                                blank=True)

    class Meta:
        verbose_name = 'Shop Unit'
        verbose_name_plural = 'Shop Unit`s'

    def __str__(self):
        return f"ShopUnit<{self.name}>"
