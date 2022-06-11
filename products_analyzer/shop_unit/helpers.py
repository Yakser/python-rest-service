import uuid

from shop_unit.models import ShopUnit
from shop_unit.serializers import ShopUnitSerializer
from shop_unit.types import ShopUnitTypes
from datetime import datetime


def calculate_category_price(category: ShopUnit) -> int | None:
    children = get_all_children(category)
    count = len(children)
    if count:
        total_price = sum(child.price for child in children)
        return int(total_price / count)
    return None


def get_all_children(unit: ShopUnit, visited=None) -> set:
    """
    Returns all children of this category

    Args:
        unit (ShopUnit): ShopUnit instance
        visited (set, optional): set() that contains added children of category. Defaults to None.

    Returns:
        set: set of all children of this category
    """

    if visited is None:
        visited = set()

    for child in unit.children.all():
        if child.type == ShopUnitTypes.CATEGORY.name:
            get_all_children(child, visited)
        else:
            visited.add(child)

    return visited


def remove_timezone_suffix(date: str) -> str:
    if date.strip().endswith('Z'):
        return date[:-1]
    return date


def format_date(date):
    if date.endswith('Z'):
        date = date.replace('Z', '.000Z')
    return date


def is_valid_uuid(value: str) -> bool:
    try:
        uuid.UUID(str(value))
        return True
    except ValueError:
        return False


def format_shop_unit_data(shop_unit: ShopUnit, data):
    data['date'] = format_date(data['date'])
    data['parentId'] = None
    if shop_unit.parent:
        data['parentId'] = str(shop_unit.parent.id)

    del data['parent']
    return data


def get_cleaned_data(shop_unit, request):
    data = ShopUnitSerializer(shop_unit, context={'request': request}).data
    return format_shop_unit_data(shop_unit, data)


def build_tree(shop_unit: ShopUnit, request, tree=None):
    if tree is None:
        tree = []
    for child in shop_unit.children.all():
        if child.type == ShopUnitTypes.CATEGORY.name:
            data = get_cleaned_data(child, request)
            tree.append(data)
            tree[-1]['children'] = build_tree(child, request, [])
        else:
            data = get_cleaned_data(child, request)
            data['children'] = None
            tree.append(data)
    return tree
