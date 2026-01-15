import unittest

from looqbox.database.connections.connection_jdbc_query_executor import QueryExecutorJDBCConnection


class TestQueryCaller(unittest.TestCase):

    def setUp(self):

        self.connection = QueryExecutorJDBCConnection("MockedName")

    def test_query_metadata_reading(self):
        #TODO Implement test when QueryExecutor deploy the metadata feature
        self.assertTrue(True)