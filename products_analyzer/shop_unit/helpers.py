import datetime

from enum import Enum, unique


@unique
class ShopUnitTypes(Enum):
    OFFER = 0
    CATEGORY = 1

    @staticmethod
    def to_choices():
        return tuple((unit_type.name, unit_type.name) for unit_type in ShopUnitTypes)


def format_date(date: str) -> datetime.datetime:
    return datetime.datetime.fromisoformat(date[:-1])
