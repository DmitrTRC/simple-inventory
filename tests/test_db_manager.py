import asyncio
import sqlite3
import unittest
from collections import OrderedDict

from lazy_orm import db_manager


class TestDatabaseManager(unittest.TestCase):
    def setUp(self):
        self.db_manager = db_manager.DatabaseManager('test_db')

    def tearDown(self):
        del self.db_manager

    def test_initialization(self):
        self.assertIsNotNone(self.db_manager)

    # def test_insert_row(self):
    #     test_table_name = "test_table"
    #     test_values = OrderedDict([('name', 'John'), ('age', 30)])
    #     self.db_manager.insert_row(test_table_name, test_values)
    #
    # def test_fetch_all_rows(self):
    #     test_table_name = "test_table"
    #     test_columns_name = ['name', 'age']
    #     loop = asyncio.get_event_loop()
    #     rows = loop.run_until_complete(self.db_manager.fetch_all_rows(test_table_name, test_columns_name))
    #     self.assertIsInstance(rows, list)
    #
    # def test_fetch_rows_if(self):
    #     test_table_name = "test_table"
    #     test_columns_name = ['name', 'age']
    #     test_condition = "age > 25"
    #     rows = self.db_manager.fetch_rows_if(test_table_name, test_condition, test_columns_name)
    #     self.assertIsInstance(rows, list)
    #
    # def test_delete_row(self):
    #     test_table_name = "test_table"
    #     test_row_id = 1
    #     self.db_manager.delete_row(test_table_name, test_row_id)
    #
    # def test_update_rows(self):
    #     test_table_name = "test_table"
    #     test_values = OrderedDict([('name', 'Jane'), ('age', 32)])
    #     test_condition = "age > 30"
    #     self.db_manager.update_rows(test_table_name, test_values, test_condition)
    #
    # def test_get_row_count(self):
    #     test_table_name = "test_table"
    #     count = self.db_manager.get_row_count(test_table_name)
    #     self.assertIsInstance(count, int)


if __name__ == '__main__':
    unittest.main()
