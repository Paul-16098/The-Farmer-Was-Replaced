from __builtins__ import (
    Drone,
    Grounds,
    Items,
    North,
    Unlocks,
    can_harvest,
    get_ground_type,
    get_world_size,
    harvest,
    max_drones,
    measure,
    move,
    num_unlocked,
    spawn_drone,
    till,
    use_item,
)
from lib import (
    for_all,
    for_each_input_xy,
    for_each_xy,
    for_wordsize,
    get_xy,
    goto,
    is_even,
    sort_cactus_x,
    sort_cactus_y,
    wait_all,
)
from plant import (
    plant_bush,
    plant_cactus,
    plant_carrot,
    plant_pumpkin,
    plant_sunflower,
    plant_tree,
)

__all__ = [
    "full_cactus",
    "full_carrot",
    "full_gold",
    "full_hay",
    "full_pumpkin",
    "full_sunflower",
    "full_tree",
    "full_weird_substance",
]


def full_sunflower() -> None:
    def _f():
        plant_sunflower()
        if measure() == 15:
            while not can_harvest():
                pass
            harvest()
            _f()

    wait_all(for_all(_f))
    for_all(harvest)


def full_pumpkin() -> None:
    wait_all(for_all(plant_pumpkin))

    def check_pumpkin() -> set[tuple[int, int]]:
        bad_pumpkin: set[tuple[int, int]] = set()

        def _f(x, y) -> bool:
            if not can_harvest():
                bad_pumpkin.add((x, y))
                return False
            return True

        wait_all(for_each_xy(_f, True))
        return bad_pumpkin

    def fix_pumpkin(bad: set[tuple[int, int]]) -> list[Drone]:
        return for_each_input_xy(bad, plant_pumpkin)

    while True:
        bad_pumpkin = check_pumpkin()
        if len(bad_pumpkin) == 0:  # ty: ignore[invalid-argument-type]
            break
        wait_all(fix_pumpkin(bad_pumpkin))

    harvest()


def full_tree() -> None:
    def _f():
        x, y = get_xy()
        if is_even(x) and is_even(y) or (not is_even(x) and not is_even(y)):
            plant_tree()
        else:
            plant_bush()

    for_all(_f)
    for_all(harvest)


def full_carrot() -> None:
    for_all(plant_carrot)
    for_all(harvest)


def full_hay() -> None:
    def _f():
        if get_ground_type() != Grounds.Grassland:
            till()

    for_all(_f)
    for_all(harvest)


def full_weird_substance() -> None:
    def _f():
        if get_ground_type() != Grounds.Grassland:
            till()
        use_item(Items.Fertilizer)

    for_all(_f)
    for_all(harvest)


def full_gold(i=350) -> None:
    def _f():
        for _ in range(i / max_drones()):
            plant_bush()
            use_item(
                Items.Weird_Substance,
                1 * 2 ** (num_unlocked(Unlocks.Mazes) - 1),
            )
            harvest()

    for _ in range(max_drones()):
        spawn_drone(_f)
        move(North)
    _f()


def full_cactus() -> None:
    wait_all(for_all(plant_cactus))

    def sort_x(i):
        goto(i, None)
        for _y in range(get_world_size()):
            sort_cactus_x()

    def sort_y(i):
        goto(None, i)
        for _x in range(get_world_size()):
            sort_cactus_y()

    wait_all(for_wordsize(sort_x))
    wait_all(for_wordsize(sort_y))
    goto(0, 0)
    harvest()
