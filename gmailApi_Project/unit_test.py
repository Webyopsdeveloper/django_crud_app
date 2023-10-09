import unittest
from unittest.mock import patch
import psycopg2
from googleapiclient.discovery import Resource
from noHardcode import GmailExtractor, main

class TestDatabaseConnection(unittest.TestCase):
    @patch('psycopg2.connect')
    @patch('googleapiclient.discovery.build')
    def test_database_connection(self, mock_build, mock_connect):
        mock_build.return_value = Resource

        # Call the main function
        main()

        # Check if psycopg2.connect is called with the correct parameters
        mock_connect.assert_called_once_with(
            host='::1',
            database='etl',
            user='postgres',
            password='postgres'
        )

        # Additional assertions to check the database connection
        self.assertTrue(mock_connect.called, "psycopg2.connect should be called")
        self.assertTrue(mock_connect.return_value.cursor.called, "psycopg2.connect should return a cursor")
        self.assertTrue(mock_connect.return_value.cursor.return_value.execute.called, "Cursor execute should be called")

if __name__ == '__main__':
    unittest.main()
