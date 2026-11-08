from lib import *
from plant import *
from tools import *

word_size = get_world_size()


clear()
while True:
    if (
        while_unit(Items.Hay, 3000, full_hay)
        or while_unit(Items.Wood, 3000, full_tree)
        or while_unit(Items.Carrot, 3000, full_carrot)
        or while_unit(Items.Power, 5000, full_sunflower)
        or while_unit(Items.Pumpkin, 3000, full_pumpkin)
        or while_unit(Items.Weird_Substance, 1000, full_weird_substance)
        or while_unit(Items.Gold, 5000, full_gold)
        or while_unit(Items.Cactus, 5000, full_cactus)
    ):
        continue

    full_hay()
    full_tree()
    full_carrot()
    # full_sunflower()
    full_pumpkin()
    full_weird_substance()
    full_gold(300)
    full_cactus()
