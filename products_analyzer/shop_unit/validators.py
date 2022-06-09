from datetime import datetime

from shop_unit.helpers import is_valid_uuid, remove_timezone_suffix
from shop_unit.models import ShopUnit
from shop_unit.types import ShopUnitTypes


def validate_type(unit_type: str) -> None:
    assert any(unit_type == tp.name for tp in ShopUnitTypes), 'Incorrect or empty ShopUnit type'


def validate_name(name: str) -> None:
    assert name.strip(), 'Incorrect or empty ShopUnit name'


def validate_id(unit_id: str) -> None:
    assert is_valid_uuid(unit_id), 'Incorrect or empty ShopUnit id'


def validate_date(date: str) -> None:
    try:
        clear_date = remove_timezone_suffix(date.strip())
        datetime.fromisoformat(clear_date)
    except Exception as e:
        raise AssertionError(f'Incorrect or empty ShopUnit update date: {e}')


def validate_parent(parent: ShopUnit) -> None:
    assert parent.type != ShopUnitTypes.CATEGORY.name, 'Only category can be a parent'


def validate_price(unit: ShopUnit) -> None:
    if unit.type == ShopUnitTypes.OFFER.name:
        assert unit.price and unit.price > 0, 'Offer must have price greater than 0'


def validate_shop_unit(unit: ShopUnit):
    validate_type(unit.get('type', ''))
    validate_name(unit.get('name', ''))
    validate_id(unit.get('id', ''))
    validate_price(unit)
