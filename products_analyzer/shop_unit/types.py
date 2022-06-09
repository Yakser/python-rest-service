from enum import Enum, unique


@unique
class ShopUnitTypes(Enum):
    OFFER = 0
    CATEGORY = 1

    @staticmethod
    def to_choices():
        return tuple((unit_type.name, unit_type.name) for unit_type in ShopUnitTypes)
