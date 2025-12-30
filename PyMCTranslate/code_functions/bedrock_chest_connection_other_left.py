from typing import Union

from amulet_nbt import CompoundTag, ByteTag, ShortTag, IntTag, LongTag, StringTag


def main(
    nbt,
    properties: dict[str, Union[ByteTag, ShortTag, IntTag, LongTag, StringTag]],
    location: tuple[int, int, int],
) -> dict[str, str]:
    if not isinstance(nbt, CompoundTag):
        return {}
    facing_direction = properties.get("facing_direction")
    if not isinstance(facing_direction, IntTag):
        return {}
    pairlead = nbt.get("pairlead")
    if isinstance(pairlead, ByteTag) and pairlead.py_int == 1:
        pair_x = nbt.get("pairx")
        if not isinstance(pair_x, IntTag):
            return {}
        pair_z = nbt.get("pairz")
        if not isinstance(pair_z, IntTag):
            return {}

        dx = pair_x.py_int - location[0]
        dz = pair_z.py_int - location[2]
        if facing_direction.py_int == 2:  # north
            if dz == 0 and dx == -1:
                return {"connection": "left"}
        elif facing_direction.py_int == 3:  # south
            if dz == 0 and dx == 1:
                return {"connection": "left"}
        elif facing_direction.py_int == 4:  # west
            if dx == 0 and dz == 1:
                return {"connection": "left"}
        elif facing_direction.py_int == 5:  # east
            if dx == 0 and dz == -1:
                return {"connection": "left"}
    return {}
