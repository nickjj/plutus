"""Regression tests for the ANSI color constants in src/plutus.

The constants are read with ast (no script execution) so the tests run
without a config file, CSV profile, or terminal.
"""

import ast
import os
import unittest

SCRIPT_PATH = os.path.normpath(
    os.path.join(os.path.dirname(__file__), "..", "..", "src", "plutus")
)


def load_color_constants():
    with open(SCRIPT_PATH, encoding="utf-8") as file:
        tree = ast.parse(file.read())
    colors = {}
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Assign)
            and len(node.targets) == 1
            and isinstance(node.targets[0], ast.Name)
            and node.targets[0].id.startswith("COLOR_")
            and node.targets[0].id != "COLOR_RESET"
        ):
            colors[node.targets[0].id] = ast.literal_eval(node.value)
    return colors


class TestColorCodes(unittest.TestCase):
    def test_each_color_has_distinct_code(self):
        colors = load_color_constants()
        self.assertIn("COLOR_YELLOW", colors)
        self.assertEqual(len(set(colors.values())), len(colors))

    def test_yellow_is_yellow(self):
        self.assertEqual(load_color_constants()["COLOR_YELLOW"], "\033[33m")


if __name__ == "__main__":
    unittest.main()
