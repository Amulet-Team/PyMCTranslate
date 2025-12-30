from amulet_nbt import CompoundTag, StringTag

from PyMCTranslate.py3.util.raw_text import section_string_to_raw_text_list


def main(nbt):
    if not isinstance(nbt, CompoundTag):
        return []
    text = nbt.get("Text")
    if not isinstance(text, StringTag):
        return []
    out = []

    if text:
        for line_num, line in enumerate(section_string_to_raw_text_list(text.py_str)):
            out.append(
                [
                    "",
                    "compound",
                    [
                        ("utags", "compound"),
                        ("front_text", "compound"),
                        ("messages", "list"),
                    ],
                    line_num,
                    StringTag(line),
                ]
            )

    return out
