from unittest import TestCase

from itglue.util import kebab_to_snake


class TestSnake(TestCase):
    def test_kebab_to_snake(self):
        test_strings = (
            ("kebab-case", "kebab_case"),
            ("beef-kababs-please", "beef_kababs_please"),
            ("trailing-hyphen-", "trailing_hyphen_"),
            ("-initial-hyphen", "_initial_hyphen"),
            ("oneword", "oneword"),
            ("has-UPPER-case", "has_upper_case"),
            ("Title-Case", "title_case"),
            ("please-Dont-SHOUT", "please_dont_shout"),
            ("jUsT-wHy", "just_why"),
        )
        for kebab, snake in test_strings:
            self.assertEqual(kebab_to_snake(kebab), snake)
