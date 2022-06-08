import uuid
from datetime import datetime
from shop_unit.types import ShopUnitTypes


def validate_type(unit_type: str) -> None:
    assert any(unit_type == tp.name for tp in ShopUnitTypes), 'Incorrect or empty ShopUnit type'


def validate_name(name: str) -> None:
    assert name.strip(), 'Incorrect or empty ShopUnit name'


def validate_id(unit_id: str) -> None:
    assert is_valid_uuid(unit_id), 'Incorrect or empty ShopUnit id'


def is_valid_uuid(value: str) -> bool:
    try:
        uuid.UUID(str(value))
        return True
    except ValueError:
        return False


def validate_date(date: str) -> None:
    try:
        clear_date = remove_timezone_suffix(date.strip())
        datetime.fromisoformat(clear_date)
    except Exception as e:
        raise AssertionError(f'Incorrect or empty ShopUnit update date: {e}')


def remove_timezone_suffix(date: str) -> str:
    if date.endswith('Z'):
        return date[:-1]
    return date
