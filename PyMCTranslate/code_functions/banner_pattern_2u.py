from amulet_nbt import CompoundTag, ListTag, IntTag

def main(nbt):
    if not isinstance(nbt, CompoundTag):
        return []
    patterns = nbt.get("Patterns")
    if not isinstance(patterns, ListTag):
        return []

    tags = []
    index = 0
    for pattern in patterns:
        if not isinstance(pattern, CompoundTag):
            continue
        colour = pattern.get("Color")
        if not isinstance(colour, IntTag):
            continue
        tags.append([
            "",
            "compound",
            [("utags", "compound"), ("Patterns", "list"), (index, "compound")],
            "Color",
            IntTag(15 - colour.py_int),
        ])
        index += 1
    return tags
