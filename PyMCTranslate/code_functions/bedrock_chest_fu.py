from amulet_nbt import ByteTag, IntTag, StringTag


def main(properties, location):
    x, _, z = location
    facing = properties.get("facing")
    if not isinstance(facing, StringTag):
        return []
    if facing.py_str == "north":  # north
        return [
            ["", "compound", [], "pairlead", ByteTag(1)],
            ["", "compound", [], "pairx", IntTag(x - 1)],
            ["", "compound", [], "pairz", IntTag(z)],
        ]
    elif facing.py_str == "south":  # south
        return [
            ["", "compound", [], "pairlead", ByteTag(1)],
            ["", "compound", [], "pairx", IntTag(x + 1)],
            ["", "compound", [], "pairz", IntTag(z)],
        ]
    elif facing.py_str == "west":  # west
        return [
            ["", "compound", [], "pairlead", ByteTag(1)],
            ["", "compound", [], "pairx", IntTag(x)],
            ["", "compound", [], "pairz", IntTag(z + 1)],
        ]
    elif facing.py_str == "east":  # east
        return [
            ["", "compound", [], "pairlead", ByteTag(1)],
            ["", "compound", [], "pairx", IntTag(x)],
            ["", "compound", [], "pairz", IntTag(z - 1)],
        ]
    return []
