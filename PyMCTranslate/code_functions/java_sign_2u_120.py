from amulet_nbt import CompoundTag, StringTag, ListTag


def main(nbt):
    if isinstance(nbt, CompoundTag):
        out = []
        for group_name in ("front_text", "back_text"):
            group = nbt.get(group_name)
            if isinstance(group, CompoundTag):
                lines = group.get("messages")
                if isinstance(lines, ListTag):
                    for i in range(4):
                        if i < len(lines):
                            tag = lines[i]
                            if isinstance(tag, StringTag):
                                line = tag
                            else:
                                line = StringTag(r"\"\"")
                        else:
                            line = StringTag(r"\"\"")

                        out.append(
                            [
                                "",
                                "compound",
                                [
                                    ("utags", "compound"),
                                    (group_name, "compound"),
                                    ("java_json", "list"),
                                ],
                                i,
                                line,
                            ]
                        )
    return []
