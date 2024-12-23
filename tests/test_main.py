import re
import unittest

from main import is_email_correct


class TestMain(unittest.TestCase):

    def test_is_email_correct_valid_email(self):
        email = "test@example.com"
        expected_email = "test@example.com"
        actual_email = is_email_correct(email)
        self.assertEqual(expected_email, actual_email)

    def test_is_email_correct_invalid_email_misplaced_at(self):
        email = "test.example.com"
        with self.assertRaises(ValueError):
            is_email_correct(email)

    def test_is_email_correct_invalid_email_no_tld(self):
        email = "test@example"
        with self.assertRaises(ValueError):
            is_email_correct(email)

    def test_is_email_correct_invalid_email_no_username(self):
        email = "@example.com"
        with self.assertRaises(ValueError):
            is_email_correct(email)

    def test_is_email_correct_invalid_email_special_characters(self):
        email = "test$%^@example.com"
        with self.assertRaises(ValueError):
            is_email_correct(email)


if __name__ == "__main__":
    unittest.main()
