from amulet_nbt import CompoundTag

def main(nbt):
    if isinstance(nbt, CompoundTag):
        rotation = nbt.get("Rotation")
        if isinstance(rotation, float):
            return {"rotation": f"\"{int(rotation // 22.5) % 16}\""}
    return {"rotation": '"0"'}
