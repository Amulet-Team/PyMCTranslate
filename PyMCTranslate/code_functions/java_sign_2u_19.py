from amulet_nbt import CompoundTag, StringTag


def main(nbt):
    if isinstance(nbt, CompoundTag):
        out = []
        for i in range(1, 5):
            key = f"Text{i}"
            tag = nbt.get(key)
            if isinstance(tag, StringTag):
                line = tag
            else:
                line = StringTag(r"\"\"")
            out.append(
                [
                    "",
                    "compound",
                    [
                        ("utags", "compound"),
                        ("front_text", "compound"),
                        ("java_json", "list"),
                    ],
                    i,
                    line,
                ]
            )
    return []
