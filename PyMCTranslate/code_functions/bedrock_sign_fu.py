from amulet_nbt import CompoundTag, ListTag, StringTag

from PyMCTranslate.py3.util.raw_text import raw_text_list_to_section_string


def pack_text(messages: ListTag) -> str:
    lines = []
    for line_number, tag in enumerate(messages):
        if isinstance(tag, StringTag):
            lines.append(tag.py_str)
        else:
            lines.append('{"text":""}')

    return raw_text_list_to_section_string(lines)


def main(nbt):
    front_text = ""

    if isinstance(nbt, CompoundTag):
        utags = nbt.get("utags")
        if isinstance(utags, CompoundTag):
            front_text_tag = utags.get("front_text")
            if isinstance(front_text_tag, CompoundTag):
                messages = front_text_tag.get("messages")
                if isinstance(messages, ListTag):
                    front_text = pack_text(messages)

    return [["", "compound", [], "Text", StringTag(front_text)]]
