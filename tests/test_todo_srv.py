import unittest
from unittest.mock import Mock, MagicMock

from service import todo_srv


class TestTodoSrv(unittest.TestCase):

    def setUp(self) -> None:
        self.db_manager = Mock()
        self.task_name = 'grocery shopping'
        self.category = 'home'
        self.db_manager.fetch_rows_if = MagicMock()

    def test_is_todo_exists_true(self):
        """
        Test `is_todo_exists` when todo exists in the database.
        """
        # set up mock object behavior
        self.db_manager.fetch_rows_if.return_value = [(1, self.task_name, self.category)]

        # call the function
        result = todo_srv.is_todo_exists(self.db_manager, self.task_name, self.category)

        # asserts
        self.db_manager.fetch_rows_if.assert_called_once()
        self.assertTrue(result)

    def test_is_todo_exists_false(self):
        """
        Test `is_todo_exists` when todo does not exist in the database.
        """
        # set up mock object behavior
        self.db_manager.fetch_rows_if.return_value = []

        # call the function
        result = todo_srv.is_todo_exists(self.db_manager, self.task_name, self.category)

        # asserts
        self.db_manager.fetch_rows_if.assert_called_once()
        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()
