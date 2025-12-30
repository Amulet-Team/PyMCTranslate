from amulet_nbt import CompoundTag, StringTag


def main(nbt):
    if isinstance(nbt, CompoundTag):
        out = []
        for group_1, group_2 in (
            ("FrontText", "front_text"),
            ("BackText", "back_text"),
        ):
            text_compound = nbt.get(group_1)
            if isinstance(text_compound, CompoundTag):
                text = text_compound.get("Text")
                if isinstance(text, StringTag):
                    out.append(
                        [
                            "",
                            "compound",
                            [
                                ("utags", "compound"),
                                (group_2, "compound"),
                            ],
                            "bedrock_string",
                            text,
                        ]
                    )
    return []
