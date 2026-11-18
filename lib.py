from __builtins__ import (
    Drone,
    East,
    Entities,
    Entity,
    Grounds,
    Item,
    Items,
    North,
    South,
    West,
    can_harvest,
    can_move,
    get_cost,
    get_ground_type,
    get_pos_x,
    get_pos_y,
    get_water,
    get_world_size,
    measure,
    move,
    num_items,
    plant,
    quick_print,
    spawn_drone,
    swap,
    till,
    use_item,
    wait_for,
)

__all__ = [
    "for_all",
    "for_each_input",
    "for_each_input_xy",
    "for_each_xy",
    "for_wordsize",
    "get_xy",
    "goto",
    "is_even",
    "sort_cactus_x",
    "sort_cactus_y",
    "wait_all",
    "while_unit",
]


def item2entities(item: Item) -> Entity | None:
    rd = {
        Items.Power: Entities.Sunflower,
        Items.Pumpkin: Entities.Pumpkin,
        Items.Carrot: Entities.Carrot,
    }
    if item in rd:
        return rd[item]


def goto(x: int | None, y: int | None):
    ws = get_world_size()

    if ((x or 0) >= ws) or ((y or 0) >= ws):
        quick_print("WARN: x or y >= world size", (x, y), ws)
        return

    max_steps = ws * 4  # 防止死循环
    for _ in range(max_steps):
        nx = get_pos_x()
        ny = get_pos_y()

        # quick_print(nx, ny, x, y)

        if (nx == x or x == None) and (ny == y or y == None):
            return

        # X 轴
        if (x != None) and (nx != x):
            dx: int = x - nx
            if dx > ws / 2:
                dx -= ws
            elif dx < -ws / 2:
                dx += ws

            d = None
            if dx > 0:
                d = East
            elif dx < 0:
                d = West

            if d != None:
                if can_move(d):
                    move(d)
                else:
                    quick_print("X方向被挡住", d, "当前", (nx, ny), "目标", (x, y))
                    return

        # Y 轴
        if (y != None) and (ny != y):
            dy: int = y - ny
            if dy > ws / 2:
                dy -= ws
            elif dy < -ws / 2:
                dy += ws

            d = None
            if dy > 0:
                d = North
            elif dy < 0:
                d = South

            if d != None:
                if can_move(d):
                    move(d)
                else:
                    quick_print("Y方向被挡住", d, "当前", (nx, ny), "目标", (x, y))
                    quick_print(
                        "North可走?", can_move(North), "South可走?", can_move(South)
                    )
                    return

    quick_print("goto 超过最大步数", (get_pos_x(), get_pos_y()), (x, y))


# time: 201 tick or 1
def hook_ground_soil() -> None:
    if get_ground_type() != Grounds.Soil:
        till()


def _plant(entity: Entity, req_soil: bool, req_water: bool) -> None:
    if req_soil:
        hook_ground_soil()

    plant(entity)

    if req_water:
        hook_water()


def is_even(n):
    return n % 2 == 0


# time: 1 or 201
def hook_water(lim: float = 0.7):
    if get_water() < lim:
        use_item(Items.Water)


def for_wordsize(do, force_not_spawn: bool = False) -> list[Drone]:
    return for_each_input(range(get_world_size()), do, force_not_spawn)


def for_each_input(input, do, force_not_spawn: bool = False) -> list[Drone]:
    dl = []
    for i in input:
        if not force_not_spawn:
            d: Drone | None = spawn_drone(do, i)
            if d == None:
                do(i)
            else:
                dl.append(d)
        else:
            do(i)
    return dl


# for each input xy goto there and run `do`
def for_each_input_xy(input_xy, do, force_not_spawn: bool = False) -> list[Drone]:
    def _f(xy: tuple[int, int]):
        x, y = xy
        goto(x, y)
        do()

    return for_each_input(input_xy, _f, force_not_spawn)


def for_each_xy(do, force_not_spawn: bool = False) -> list[Drone]:
    def _f():
        x, y = get_xy()
        do(x, y)

    return for_all(_f, force_not_spawn)


def enough_cons(cons: dict[Item, int]) -> bool:
    for k in cons:  # noqa: PLC0206
        if not num_items(k) > cons[k]:
            return False
    return True


def while_unit(item: Item, unit: int, do) -> bool:
    is_run = False

    cons = None
    entities = item2entities(item)
    if entities != None:
        cons = get_cost(entities)
    enou_cons = True
    if cons != None:
        enou_cons = enough_cons(cons)
    while (num_items(item)) < unit and enou_cons:
        is_run = True
        do()
    return is_run


def for_all(f, force_not_spawn: bool = False) -> list[Drone]:
    def row(x) -> list:
        goto(x, None)
        rl = []
        for y in range(get_world_size()):
            goto(None, y)
            rl.append(f())
        return rl

    return for_wordsize(row, force_not_spawn)


# time: 2
def get_xy() -> tuple[int, int]:
    return (get_pos_x(), get_pos_y())


def wait_all(dl: list[Drone]) -> list:
    r = []
    for d in dl:
        r.append(wait_for(d))
    return r


def sort_cactus_x(y=0) -> None:
    if y >= get_world_size():
        return

    goto(None, y)
    now_size: int = measure()  # ty: ignore[invalid-assignment]
    next_size: int = measure(North)  # ty: ignore[invalid-assignment]

    if (next_size < now_size) and not (y >= (get_world_size() - 1)):
        swap(North)
    # elif (up_size > now_size) and not (y == 0):
    #     swap(South)
    return sort_cactus_x(y + 1)


def sort_cactus_y(x=0) -> None:
    if x >= get_world_size():
        return

    goto(x, None)
    now_size: int = measure()  # ty: ignore[invalid-assignment]
    next_size: int = measure(East)  # ty: ignore[invalid-assignment]

    if (next_size < now_size) and not (x == (get_world_size() - 1)):
        swap(East)
    # elif (up_size > now_size) and not (y == 0):
    #     swap(South)
    return sort_cactus_y(x + 1)


def sleep(t: int) -> None:
    for _ in range(t):
        can_harvest()
