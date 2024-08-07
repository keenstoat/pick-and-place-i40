from time import sleep

_is_module_busy = False
target_position = {
    "x": 0, "y": 0, "z": 0
}

real_position = {
    "x": 0, "y": 0, "z": 0
}

def set_target_position_cart(x:float=None, y:float=None, z:float=None):
    if x is not None:
        target_position["x"] = x

    if y is not None:
        target_position["y"] = y

    if z is not None:
        target_position["z"] = z

def get_target_position_cart():
    return real_position["x"], real_position["y"], real_position["z"]

def move_cartesian(x:float=None, y:float=None, z:float=None):
    global _is_module_busy
    _is_module_busy = True
    
    set_target_position_cart(x, y, z)
    delta_x = (target_position["x"] - real_position["x"])/10
    delta_y = (target_position["y"] - real_position["y"])/10
    delta_z = (target_position["z"] - real_position["z"])/10
    for _ in range(10):
        real_position["x"] += delta_x
        real_position["y"] += delta_y
        real_position["z"] += delta_z
        sleep(1)
    
    _is_module_busy = False
