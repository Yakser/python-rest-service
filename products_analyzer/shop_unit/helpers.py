import uuid

from shop_unit.models import ShopUnit
from shop_unit.types import ShopUnitTypes


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


def is_valid_uuid(value: str) -> bool:
    try:
        uuid.UUID(str(value))
        return True
    except ValueError:
        return False
