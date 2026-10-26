from amulet_nbt import CompoundTag, FloatTag


def main(nbt):
    if isinstance(nbt, CompoundTag):
        rotation = nbt.get("Rotation")
        if isinstance(rotation, FloatTag):
            return {"rotation": f'"{int(rotation.py_float // 22.5) % 16}"'}
    return {"rotation": '"0"'}
