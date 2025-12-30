from amulet_nbt import CompoundTag, ListTag


def main(nbt):
    if isinstance(nbt, CompoundTag):
        out = []
        for group_name in ("front_text", "back_text"):
            group = nbt.get(group_name)
            if isinstance(group, CompoundTag):
                lines = group.get("messages")
                if isinstance(lines, ListTag):
                    for i, line in enumerate(lines):
                        out.append(
                            [
                                "",
                                "compound",
                                [
                                    ("utags", "compound"),
                                    (group_name, "compound"),
                                    ("java_nbt", "list"),
                                ],
                                i,
                                line,
                            ]
                        )
    return []
