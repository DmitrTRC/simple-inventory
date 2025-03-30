import unittest

from model.todo_model import Category


class TestCategory(unittest.TestCase):
    def test_enum_values(self):
        self.assertEqual(Category.BACKLOG.value, 1)
        self.assertEqual(Category.MAINTENANCE.value, 2)
        self.assertEqual(Category.BIRTHDAY.value, 3)
        self.assertEqual(Category.READING.value, 4)
        self.assertEqual(Category.WATCHING.value, 5)
        self.assertEqual(Category.SHOPPING.value, 6)

    def test_enum_names(self):
        self.assertEqual(Category.BACKLOG.name, 'BACKLOG')
        self.assertEqual(Category.MAINTENANCE.name, 'MAINTENANCE')
        self.assertEqual(Category.BIRTHDAY.name, 'BIRTHDAY')
        self.assertEqual(Category.READING.name, 'READING')
        self.assertEqual(Category.WATCHING.name, 'WATCHING')
        self.assertEqual(Category.SHOPPING.name, 'SHOPPING')


if __name__ == '__main__':
    unittest.main()
