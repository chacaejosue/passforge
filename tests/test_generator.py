import string
import unittest

from src.generator import MAX_LENGTH, MIN_LENGTH, generate_password


class TestGeneratePassword(unittest.TestCase):

    def test_returns_string(self):
        password = generate_password(16)

        self.assertIsInstance(password, str)

    def test_respects_requested_length(self):
        password = generate_password(16)

        self.assertEqual(len(password), 16)

    def test_applies_minimum_length(self):
        password = generate_password(MIN_LENGTH - 1)

        self.assertEqual(len(password), MIN_LENGTH)

    def test_includes_lowercase_letter(self):
        password = generate_password(16)

        self.assertTrue(
            any(character in string.ascii_lowercase for character in password)
        )

    def test_includes_uppercase_letter(self):
        password = generate_password(16)

        self.assertTrue(
            any(character in string.ascii_uppercase for character in password)
        )

    def test_includes_digit(self):
        password = generate_password(16)

        self.assertTrue(
            any(character in string.digits for character in password)
        )

    def test_includes_symbol(self):
        password = generate_password(16)

        self.assertTrue(
            any(character in string.punctuation for character in password)
        )

    def test_rejects_length_above_maximum(self):
        with self.assertRaises(ValueError):
            generate_password(MAX_LENGTH + 1)

    def test_rejects_boolean_length(self):
        with self.assertRaises(TypeError):
            generate_password(True)

    def test_rejects_no_character_sets_enabled(self):
        with self.assertRaises(ValueError):
            generate_password(
                16,
                lowercase=False,
                uppercase=False,
                digits=False,
                symbols=False,
            )

    def test_respects_single_character_set_selection(self):
        password = generate_password(
            20,
            lowercase=False,
            uppercase=False,
            digits=True,
            symbols=False,
        )
        self.assertTrue(all(ch in string.digits for ch in password))


if __name__ == "__main__":
    unittest.main()
