import uuid
from typing import Union
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

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

    def calculate_price(self) -> Union[int, None]:
        if self.type == ShopUnitTypes.CATEGORY.name:
            children = self.get_all_children()
            count = len(children)
            if count:
                total_price = sum(child.price for child in children)
                return int(total_price / count)
            return None
        else:
            return self.price

    def get_all_children(self, visited=None) -> set:
        """
        Returns all children of category. For Offer children is None

        Args:
            visited (set, optional): set() that contains added children of category.
            Defaults to None.

        Returns:
            set: set of all children of this category
        """

        if visited is None:
            visited = set()

        for child in self.children.all():
            if child.type == ShopUnitTypes.CATEGORY.name:
                child.get_all_children(visited)
            else:
                visited.add(child)

        return visited

    def clean(self):
        try:
            self._validate_all()

        except Exception as e:
            raise ValidationError(f"Validation failed: {e}")

    def _validate_all(self) -> None:
        self._validate_price()
        self._validate_parent()

    def _validate_parent(self) -> None:
        if self.parent:
            assert self.parent.type == ShopUnitTypes.CATEGORY.name, 'Only category can be a parent'
        assert self.parent != self, 'Category cannot be a parent of itself'

    def _validate_price(self) -> None:
        if self.type == ShopUnitTypes.OFFER.name:
            assert self.price and self.price > 0, 'Offer must have price greater than 0'
        if self.type == ShopUnitTypes.CATEGORY.name:
            assert self.price is None, 'Category price must be None(null) by default'

    class Meta:
        verbose_name = 'Shop Unit'
        verbose_name_plural = 'Shop Unit`s'

    def __str__(self):
        return f"ShopUnit<{self.name}>"


@receiver(post_save, sender=ShopUnit)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    # update price
    parent = instance.parent
    if parent:
        parent.price = parent.calculate_price()
        # update date
        parent.date = instance.date
        parent.save()
