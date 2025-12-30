from amulet_nbt import CompoundTag, StringTag

from PyMCTranslate.py3.util.raw_text import raw_text_to_section_string


def main(nbt):
    text = ""

    if isinstance(nbt, CompoundTag):
        utags = nbt.get("utags")
        if isinstance(utags, CompoundTag):
            custom_name = utags.get("CustomName")
            if isinstance(custom_name, StringTag):
                text = raw_text_to_section_string(custom_name.py_str)
    return [["", "compound", [], "CustomName", StringTag(text)]]
