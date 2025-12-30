from amulet_nbt import CompoundTag, StringTag

from PyMCTranslate.py3.util.raw_text import section_string_to_raw_text


def main(nbt):
    raw_text = '""'

    if isinstance(nbt, CompoundTag):
        custom_name = nbt.get("CustomName")
        if isinstance(custom_name, StringTag):
            raw_text = section_string_to_raw_text(custom_name.py_str)

    return [
        ["", "compound", [("utags", "compound")], "CustomName", StringTag(raw_text)]
    ]
