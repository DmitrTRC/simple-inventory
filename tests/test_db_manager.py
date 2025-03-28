import os
import unittest
from unittest.mock import Mock, patch

from lazy_orm import db_manager


class TestDatabaseManager(unittest.TestCase):
    def setUp(self):
        self.manager = db_manager.DatabaseManager('test_db', 'test_dir')
        self.create_test_db()

    def create_test_db(self):
        db_path = os.path.join('test_dir', 'test_db.sqlite')
        os.makedirs('test_dir', exist_ok=True)

        with open('sql/create_test_db.sql', 'w') as script_file:
            script_file.write("""
                CREATE TABLE IF NOT EXISTS table (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL
                );

                INSERT INTO table (id, name) VALUES (1, 'test'), (2, 'example');
            """)

        connection = self.manager._connect_to_db()
        with connection:
            with open('test_dir/create_test_db.sql', 'r') as script_file:
                connection.executescript(script_file.read())

    @patch.object(db_manager.os.path, 'join')
    def test_init(self, mock_join):
        self.assertEqual(self.manager.__db_name, 'test_db')

    @patch.object(db_manager.sqlite3, 'connect')
    def test_connect_to_db(self, mock_connect):
        mock_connect.return_value = Mock()
        self.assertEqual(self.manager._connect_to_db(), mock_connect.return_value)

    def test_row_to_dict(self):
        row = (1, 'test')
        columns = ['id', 'name']
        expected_result = {'id': 1, 'name': 'test'}
        self.assertEqual(self.manager._row_to_dict(row, columns), expected_result)

    @patch.object(db_manager.DatabaseManager, '_row_to_dict')
    @patch.object(db_manager.sqlite3.Cursor, 'fetchall')
    def test_fetch_all(self, mock_fetchall, mock_row_to_dict):
        mock_fetchall.return_value = [(1, 'test'), (2, 'example')]
        mock_row_to_dict.side_effect = [{'id': 1, 'name': 'test'}, {'id': 2, 'name': 'example'}]
        result = self.manager.fetch_all('table', ['id', 'name'])
        self.assertEqual(result, [{'id': 1, 'name': 'test'}, {'id': 2, 'name': 'example'}])

    # Apply similar approach to test other methods

    def tearDown(self):
        del self.manager
        db_path = os.path.join('test_dir', 'test_db.sqlite')
        if os.path.exists(db_path):
            os.remove(db_path)
        script_path = os.path.join('test_dir', 'create_test_db.sql')
        if os.path.exists(script_path):
            os.remove(script_path)
        if os.path.exists('test_dir'):
            os.rmdir('test_dir')


if __name__ == '__main__':
    unittest.main()
