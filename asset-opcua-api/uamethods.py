
from asyncua.common.methods import uamethod
from random import randint

def get_processed_item_count():
    # print("item count!!!")
    return randint(1, 5)

@uamethod
def pickup(parent, x, y):
    print("pickup!!!")
    return f"x is {x} and y is {y}"