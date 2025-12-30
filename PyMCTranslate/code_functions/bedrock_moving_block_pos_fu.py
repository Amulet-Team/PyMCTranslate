from amulet_nbt import CompoundTag, IntTag

def main(nbt, location):
    if not isinstance(nbt, CompoundTag):
        return []
    utags = nbt.get("utags")
    if not isinstance(utags, CompoundTag):
        return []
    piston_pos_dx = utags.get("pistonPosdX")
    piston_pos_dy = utags.get("pistonPosdY")
    piston_pos_dz = utags.get("pistonPosdZ")
    if not (isinstance(piston_pos_dx, IntTag) and isinstance(piston_pos_dy, IntTag) and isinstance(piston_pos_dz, IntTag)):
        return []
    return [
        [
            "",
            "compound",
            [],
            "pistonPosX",
            IntTag(piston_pos_dx.py_int + location[0]),
        ],
        [
            "",
            "compound",
            [],
            "pistonPosY",
            IntTag(piston_pos_dy.py_int + location[1]),
        ],
        [
            "",
            "compound",
            [],
            "pistonPosZ",
            IntTag(piston_pos_dz.py_int + location[2]),
        ],
    ]
