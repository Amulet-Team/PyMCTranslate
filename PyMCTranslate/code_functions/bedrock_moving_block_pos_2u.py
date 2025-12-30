from amulet_nbt import CompoundTag, IntTag

def main(nbt, location):
    if not isinstance(nbt, CompoundTag):
        return []
    piston_pos_x = nbt.get("pistonPosX")
    piston_pos_y = nbt.get("pistonPosY")
    piston_pos_z = nbt.get("pistonPosZ")
    if not (isinstance(piston_pos_x, IntTag) and isinstance(piston_pos_y, IntTag) and isinstance(piston_pos_z, IntTag)):
        return []

    return [
        [
            "",
            "compound",
            [("utags", "compound")],
            "pistonPosdX",
            IntTag(piston_pos_x.py_int - location[0]),
        ],
        [
            "",
            "compound",
            [("utags", "compound")],
            "pistonPosdY",
            IntTag(piston_pos_y.py_int - location[1]),
        ],
        [
            "",
            "compound",
            [("utags", "compound")],
            "pistonPosdZ",
            IntTag(piston_pos_z.py_int - location[2]),
        ],
    ]
