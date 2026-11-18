from __builtins__ import (
    Drone,
    East,
    Entities,
    Grounds,
    Hats,
    Items,
    North,
    South,
    Unlocks,
    West,
    can_harvest,
    can_move,
    change_hat,
    get_ground_type,
    get_pos_x,
    get_pos_y,
    get_world_size,
    harvest,
    max_drones,
    measure,
    move,
    num_unlocked,
    plant,
    quick_print,
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
    sleep,
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
    "full_dinosaur",
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
        # if measure() == 15:
        #     while not can_harvest():
        #         pass
        #     harvest()
        #     _f()

    wait_all(for_all(_f))
    for_all(harvest)


def old_full_pumpkin() -> None:
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


def full_pumpkin():
    wait_all(for_all(plant_pumpkin))

    def sep_do() -> bool:
        if not can_harvest():
            plant(Entities.Pumpkin)
            sleep(5)
            return False
        return True

    while True:
        r = True
        rl: list[list[bool]] = wait_all(for_all(sep_do))
        for rll in rl:
            for rllv in rll:
                r = r and rllv
        if r:
            break
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


def old_full_dinosaur() -> None:
    change_hat(Hats.Dinosaur_Hat)
    m: tuple[int, int] = measure()  # ty: ignore[invalid-assignment]
    while True:
        n = True
        # check y
        for v in [North, South]:
            while can_move(v) and n:
                # y is apple y
                if m[1] == get_pos_y():
                    n = False
                    continue
                move(v)
        n = True
        # check x
        for v in [West, East]:
            while can_move(v) and n:
                # x is apple x
                if m[0] == get_pos_x():
                    n = False
                    continue
                move(v)

        # now (x,y)=m
        # get next apple
        m: tuple[int, int] = measure()  # ty: ignore[invalid-assignment]


# by deepseek
def full_dinosaur() -> None:
    # 戴上恐龙帽，当前位置生成苹果
    change_hat(Hats.Dinosaur_Hat)
    # 吃到脚下的苹果，并测量下一个苹果的位置
    m: tuple[int, int] = measure()  # ty: ignore[invalid-assignment]

    while True:
        # 如果测量结果异常（出现 None），直接报错退出
        if m == None or m[0] == None or m[1] == None:
            quick_print("测不到下一个苹果，退出。当前测量值:", m)
            return

        tx = m[0]
        ty = m[1]
        moved = False

        # 1. 优先移动 Y 轴
        if get_pos_y() != ty:
            if ty > get_pos_y() and can_move(North):
                move(North)
                moved = True
            elif ty < get_pos_y() and can_move(South):
                move(South)
                moved = True

        # 2. 然后移动 X 轴
        if not moved and get_pos_x() != tx:
            if tx > get_pos_x() and can_move(East):
                move(East)
                moved = True
            elif tx < get_pos_x() and can_move(West):
                move(West)
                moved = True

        # 3. 核心：如果直线被自己的身体挡住，尝试绕路！
        if not moved:
            for d in [North, South, East, West]:
                if can_move(d):
                    move(d)
                    moved = True
                    break

        if not moved:
            break

        # 5. 检查是否到达目标位置（吃到了苹果）
        if get_pos_x() == tx and get_pos_y() == ty:
            m: tuple[int, int] = measure()  # 获取下一个苹果  # ty: ignore[invalid-assignment]
            # quick_print("吃到了！下一个目标:", m)
    change_hat(Hats.Gold_Hat)
