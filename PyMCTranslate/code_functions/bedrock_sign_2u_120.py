from amulet_nbt import CompoundTag, StringTag

from PyMCTranslate.py3.util.raw_text import section_string_to_raw_text_list


def main(nbt):
    if not isinstance(nbt, CompoundTag):
        return []

    out = []

    for group_1, group_2 in (("FrontText", "front_text"), ("BackText", "back_text")):
        text_compound = nbt.get(group_1)
        if isinstance(text_compound, CompoundTag):
            text = text_compound.get("Text")
            if isinstance(text, StringTag):
                for line_num, line in enumerate(
                    section_string_to_raw_text_list(text.py_str)
                ):
                    out.append(
                        [
                            "",
                            "compound",
                            [
                                ("utags", "compound"),
                                (group_2, "compound"),
                                ("messages", "list"),
                            ],
                            line_num,
                            StringTag(line),
                        ]
                    )

    return out
