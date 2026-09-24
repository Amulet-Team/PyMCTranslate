import unittest
import logging

import amulet_nbt

import PyMCTranslate
from PyMCTranslate.py3.api import Block

from is_invalid_state import is_invalid_state

log = logging.getLogger("PyMCTranslate")


class DefaultToUniversalTestCase(unittest.TestCase):
    def test_in_and_out(self) -> None:
        translations = PyMCTranslate.new_translation_manager()

        for platform_name in translations.platforms():
            for version_number in reversed(translations.version_numbers(platform_name)):
                if version_number < (1, 13, 0):
                    # TODO: Fix issue in numerical formats and remove this.
                    continue
                version = translations.get_version(platform_name, version_number)
                log.info(f"Checking version {platform_name} {version_number}")
                for namespace_str in version.block.namespaces(True):
                    for base_name in version.block.base_names(namespace_str, True):
                        with self.subTest(
                            platform_name=platform_name,
                            version_number=version_number,
                            block=(namespace_str, base_name),
                        ):
                            full_block = Block(
                                namespace_str,
                                base_name,
                                {
                                    key: amulet_nbt.from_snbt(value)
                                    for key, value in version.block.get_specification(
                                        namespace_str, base_name
                                    )
                                    .get("defaults", {})
                                    .items()
                                },
                            )
                            if is_invalid_state(
                                platform_name, version_number, version, full_block
                            ):
                                # TODO: Fix default states and convert this to assertFalse
                                continue
                            universal_output, extra_output, extra_needed = (
                                version.block.to_universal(
                                    Block(namespace_str, base_name)
                                )
                            )
                            output, extra, extra_needed = version.block.from_universal(
                                universal_output
                            )
                            self.assertEqual(full_block, output)


if __name__ == "__main__":
    unittest.main()
