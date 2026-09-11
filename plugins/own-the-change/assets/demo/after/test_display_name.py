import unittest

from display_name import display_name


class DisplayNameTests(unittest.TestCase):
    def test_surrounding_whitespace_is_removed(self):
        self.assertEqual(display_name("  Ada  "), "Ada")

    def test_internal_whitespace_is_collapsed(self):
        self.assertEqual(display_name("Ada\t  Lovelace"), "Ada Lovelace")

    def test_whitespace_only_input_is_empty(self):
        self.assertEqual(display_name(" \t "), "")

    def test_nonbreaking_space_is_normalized(self):
        self.assertEqual(display_name("Ada\u00a0Lovelace"), "Ada Lovelace")


if __name__ == "__main__":
    unittest.main()
