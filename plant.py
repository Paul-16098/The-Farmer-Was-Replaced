from __builtins__ import Entities
from lib import _plant

__all__ = [
    "plant_bush",
    "plant_cactus",
    "plant_carrot",
    "plant_pumpkin",
    "plant_sunflower",
    "plant_tree",
]


def plant_carrot() -> None:
    _plant(Entities.Carrot, True, True)


def plant_tree() -> None:
    _plant(Entities.Tree, True, True)


def plant_bush() -> None:
    _plant(Entities.Bush, False, False)


def plant_sunflower() -> None:
    _plant(Entities.Sunflower, True, True)


def plant_pumpkin() -> None:
    _plant(Entities.Pumpkin, True, True)


def plant_cactus() -> None:
    _plant(Entities.Cactus, True, True)
