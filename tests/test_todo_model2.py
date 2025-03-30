import datetime
import unittest

from model.todo_model import Todo, Category, Status


class TodoTest(unittest.TestCase):

    def test_todo_initialization(self):
        test_todo = Todo(task='Go to gym')
        self.assertEqual(test_todo.task, 'Go to gym')
        self.assertIs(test_todo.category, Category.BACKLOG)
        assert isinstance(test_todo.date_added, str)
        self.assertIsNone(test_todo.date_completed)
        self.assertIs(test_todo.status, Status.UNDONE)
        self.assertIsNone(test_todo._id)

    def test_get_id(self):
        test_todo = Todo(task='Go to gym', _id=100)
        self.assertEqual(test_todo.get_id(), 100)

    def test_repr(self):
        date_now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
        test_todo = Todo(task='Go to gym', _id=100)
        self.assertEqual(repr(test_todo), 'Go to gym, Category.BACKLOG, {}, None, Status.UNDONE, 100'.format(date_now))


if __name__ == '__main__':
    unittest.main()
