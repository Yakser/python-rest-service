from shop_unit.models import ShopUnit
from shop_unit.types import ShopUnitTypes


def calculate_category_price(category: ShopUnit) -> int:
    children = get_all_children(category)
    count = len(children)
    total_price = sum(child.price for child in children)
    return int(total_price / count)


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
