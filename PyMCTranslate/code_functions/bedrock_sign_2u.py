from amulet_nbt import CompoundTag, StringTag


def main(nbt):
    if isinstance(nbt, CompoundTag):
        text = nbt.get("Text")
        if isinstance(text, StringTag):
            return [
                [
                    "",
                    "compound",
                    [
                        ("utags", "compound"),
                        ("front_text", "compound"),
                    ],
                    "bedrock_string",
                    text,
                ]
            ]
    return []
