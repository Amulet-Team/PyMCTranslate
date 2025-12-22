import unittest
import copy


from amulet_nbt import CompoundTag, ListTag, StringTag, ByteTag

from PyMCTranslate.py3.util.raw_text.java_nbt import from_java_nbt, to_java_nbt
from PyMCTranslate.py3.util.raw_text.bedrock_section_string import (
    from_bedrock_section_string,
    to_bedrock_section_string,
)
from PyMCTranslate.py3.util.raw_text.java_section_string import (
    from_java_section_string,
    to_java_section_string,
)

HelloWorldStr = StringTag("Hello World")
JavaHelloWorldListStr = ListTag([StringTag("Hello "), StringTag("World")])
JavaFormattingList = ListTag(
    [
        CompoundTag(
            {
                "text": StringTag("H"),
                "color": StringTag("black"),
                "italic": ByteTag(1),
            }
        ),
        CompoundTag({"text": StringTag("e"), "color": StringTag("dark_blue")}),
        CompoundTag(
            {
                "text": StringTag("l"),
                "color": StringTag("dark_green"),
                "underlined": ByteTag(1),
            }
        ),
        CompoundTag({"text": StringTag("l"), "color": StringTag("dark_aqua")}),
        CompoundTag(
            {"text": StringTag("o"), "color": StringTag("dark_red"), "bold": ByteTag(1)}
        ),
        CompoundTag({"text": StringTag("W"), "color": StringTag("dark_purple")}),
        CompoundTag(
            {
                "text": StringTag("o"),
                "color": StringTag("gold"),
                "strikethrough": ByteTag(1),
            }
        ),
        CompoundTag({"text": StringTag("r"), "color": StringTag("gray")}),
        CompoundTag(
            {
                "text": StringTag("l"),
                "color": StringTag("dark_gray"),
                "obfuscated": ByteTag(1),
            }
        ),
        CompoundTag({"text": StringTag("d"), "color": StringTag("blue")}),
    ]
)
JavaFormattingCompound = CompoundTag(
    {
        "text": StringTag("H"),
        "color": StringTag("black"),
        "italic": ByteTag(1),
        "extra": ListTag(
            [
                CompoundTag({"text": StringTag("e"), "color": StringTag("dark_blue")}),
                CompoundTag(
                    {
                        "text": StringTag("l"),
                        "color": StringTag("dark_green"),
                        "underlined": ByteTag(1),
                    }
                ),
                CompoundTag({"text": StringTag("l"), "color": StringTag("dark_aqua")}),
                CompoundTag(
                    {
                        "text": StringTag("o"),
                        "color": StringTag("dark_red"),
                        "bold": ByteTag(1),
                    }
                ),
                CompoundTag(
                    {"text": StringTag("W"), "color": StringTag("dark_purple")}
                ),
                CompoundTag(
                    {
                        "text": StringTag("o"),
                        "color": StringTag("gold"),
                        "strikethrough": ByteTag(1),
                    }
                ),
                CompoundTag({"text": StringTag("r"), "color": StringTag("gray")}),
                CompoundTag(
                    {
                        "text": StringTag("l"),
                        "color": StringTag("dark_gray"),
                        "obfuscated": ByteTag(1),
                    }
                ),
                CompoundTag({"text": StringTag("d"), "color": StringTag("blue")}),
            ]
        ),
    }
)


class RawTextTestCase(unittest.TestCase):
    def test_java_nbt_to_java_nbt(self) -> None:
        self.assertEqual(HelloWorldStr, to_java_nbt(from_java_nbt(HelloWorldStr)))
        self.assertEqual(
            JavaHelloWorldListStr,
            to_java_nbt(from_java_nbt(copy.deepcopy(JavaHelloWorldListStr))),
        )
        self.assertEqual(
            JavaFormattingList,
            to_java_nbt(from_java_nbt(copy.deepcopy(JavaFormattingList))),
        )
        self.assertEqual(
            JavaFormattingCompound,
            to_java_nbt(from_java_nbt(copy.deepcopy(JavaFormattingCompound))),
        )

    def test_java_nbt_to_bedrock_section_string(self) -> None:
        self.assertEqual(
            "Hello World", to_bedrock_section_string(from_java_nbt(HelloWorldStr))
        )
        self.assertEqual(
            "Hello World",
            to_bedrock_section_string(
                from_java_nbt(copy.deepcopy(JavaHelloWorldListStr))
            ),
        )
        self.assertEqual(
            "§oH§1e§2l§3l§4§lo§r§5§oW§6o§7r§8§kl§r§9§od",
            to_bedrock_section_string(from_java_nbt(copy.deepcopy(JavaFormattingList))),
        )
        self.assertEqual(
            "§oH§1e§2l§3l§4§lo§r§5§oW§6o§7r§8§kl§r§9§od",
            to_bedrock_section_string(
                from_java_nbt(copy.deepcopy(JavaFormattingCompound))
            ),
        )

    def test_java_nbt_to_java_section_string(self) -> None:
        self.assertEqual(
            "Hello World", to_java_section_string(from_java_nbt(HelloWorldStr))
        )
        self.assertEqual(
            "Hello World",
            to_java_section_string(from_java_nbt(copy.deepcopy(JavaHelloWorldListStr))),
        )
        self.assertEqual(
            "§oH§1e§2§nl§r§3§ol§4§lo§r§5§oW§6§mo§r§7§or§8§kl§r§9§od",
            to_java_section_string(from_java_nbt(copy.deepcopy(JavaFormattingList))),
        )
        self.assertEqual(
            "§oH§1e§2§nl§r§3§ol§4§lo§r§5§oW§6§mo§r§7§or§8§kl§r§9§od",
            to_java_section_string(
                from_java_nbt(copy.deepcopy(JavaFormattingCompound))
            ),
        )

    def test_bedrock_section_string_to_bedrock_section_string(self) -> None:
        self.assertEqual(
            "Hello World",
            to_bedrock_section_string(from_bedrock_section_string("Hello World")),
        )
        self.assertEqual(
            "§oH§1e§2l§3l§4§lo§r§5§oW§6o§7r§8§kl§r§9§od",
            to_bedrock_section_string(
                from_bedrock_section_string(
                    "§oH§1e§2l§3l§4§lo§r§5§oW§6o§7r§8§kl§r§9§od"
                )
            ),
        )
        self.assertEqual(
            "§oH§1e§2l§3l§4§lo§r§5§oW§6o§7r§8§kl§r§9§od",
            to_bedrock_section_string(
                from_bedrock_section_string(
                    "§oH§1e§2l§r§3§ol§4§lo§r§5§oW§6o§r§7§or§8§kl§r§9§od"
                )
            ),
        )

    def test_from_java_section_string(self) -> None:
        component = from_java_section_string("")
        self.assertEqual("", to_bedrock_section_string(copy.deepcopy(component)))
        self.assertEqual("", to_java_section_string(copy.deepcopy(component)))
        self.assertEqual(StringTag(""), to_java_nbt(copy.deepcopy(component)))

        component = from_java_section_string("Hello World")
        self.assertEqual(
            "Hello World", to_bedrock_section_string(copy.deepcopy(component))
        )
        self.assertEqual(
            "Hello World", to_java_section_string(copy.deepcopy(component))
        )
        self.assertEqual(
            StringTag("Hello World"), to_java_nbt(copy.deepcopy(component))
        )

        component = from_java_section_string("§4Hello§1World")
        self.assertEqual(
            "§4Hello§1World", to_bedrock_section_string(copy.deepcopy(component))
        )
        self.assertEqual(
            "§4Hello§1World", to_java_section_string(copy.deepcopy(component))
        )
        self.assertEqual(
            CompoundTag(
                {
                    "extra": ListTag(
                        [
                            CompoundTag(
                                {
                                    "text": StringTag("Hello"),
                                    "color": StringTag("dark_red"),
                                }
                            ),
                            CompoundTag(
                                {
                                    "text": StringTag("World"),
                                    "color": StringTag("dark_blue"),
                                }
                            ),
                        ]
                    )
                }
            ),
            to_java_nbt(copy.deepcopy(component)),
        )

        component = from_java_section_string(
            "§oH§1e§2§nl§r§3§ol§4§lo§r§5§oW§6§mo§r§7§or§8§kl§r§9§od"
        )
        self.assertEqual(
            "§oH§1e§2l§3l§4§lo§r§5§oW§6o§7r§8§kl§r§9§od",
            to_bedrock_section_string(copy.deepcopy(component)),
        )
        self.assertEqual(
            "§oH§1e§2§nl§r§3§ol§4§lo§r§5§oW§6§mo§r§7§or§8§kl§r§9§od",
            to_java_section_string(copy.deepcopy(component)),
        )
        self.assertEqual(
            CompoundTag(
                {
                    "extra": ListTag(
                        [
                            CompoundTag({"text": StringTag("H"), "italic": ByteTag(1)}),
                            CompoundTag(
                                {
                                    "text": StringTag("e"),
                                    "color": StringTag("dark_blue"),
                                    "italic": ByteTag(1),
                                }
                            ),
                            CompoundTag(
                                {
                                    "text": StringTag("l"),
                                    "color": StringTag("dark_green"),
                                    "italic": ByteTag(1),
                                    "underlined": ByteTag(1),
                                }
                            ),
                            CompoundTag(
                                {
                                    "text": StringTag("l"),
                                    "color": StringTag("dark_aqua"),
                                    "italic": ByteTag(1),
                                }
                            ),
                            CompoundTag(
                                {
                                    "text": StringTag("o"),
                                    "color": StringTag("dark_red"),
                                    "bold": ByteTag(1),
                                    "italic": ByteTag(1),
                                }
                            ),
                            CompoundTag(
                                {
                                    "text": StringTag("W"),
                                    "color": StringTag("dark_purple"),
                                    "italic": ByteTag(1),
                                }
                            ),
                            CompoundTag(
                                {
                                    "text": StringTag("o"),
                                    "color": StringTag("gold"),
                                    "italic": ByteTag(1),
                                    "strikethrough": ByteTag(1),
                                }
                            ),
                            CompoundTag(
                                {
                                    "text": StringTag("r"),
                                    "color": StringTag("gray"),
                                    "italic": ByteTag(1),
                                }
                            ),
                            CompoundTag(
                                {
                                    "text": StringTag("l"),
                                    "color": StringTag("dark_gray"),
                                    "italic": ByteTag(1),
                                    "obfuscated": ByteTag(1),
                                }
                            ),
                            CompoundTag(
                                {
                                    "text": StringTag("d"),
                                    "color": StringTag("blue"),
                                    "italic": ByteTag(1),
                                }
                            ),
                        ]
                    )
                }
            ),
            to_java_nbt(copy.deepcopy(component)),
        )


if __name__ == "__main__":
    unittest.main()
