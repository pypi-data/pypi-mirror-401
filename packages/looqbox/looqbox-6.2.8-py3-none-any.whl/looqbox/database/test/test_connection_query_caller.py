import json
import unittest
from os.path import dirname, join
from pandas import DataFrame, read_csv, Float64Dtype, Int64Dtype, StringDtype, BooleanDtype

from looqbox.database.connections.connection_jdbc_query_caller import QueryCallerJDBCConnection


class TestQueryCaller(unittest.TestCase):

    def setUp(self):

        with open(join(dirname(__file__), "resources", "queryCallerMockedData-metadata.json"), "r") as metadata_file:
            self.raw_metadata = json.load(metadata_file)
            metadata_file.close()
        self.raw_data = read_csv(join(dirname(__file__), "resources", "queryCallerMockedData.csv"))

        self.connection = QueryCallerJDBCConnection("MockedName")

        self.connection.result_file = join(dirname(__file__), "resources", "queryCallerMockedData")

    def test_query_metadata_reading(self):

        self.connection._set_query_metadata()
        self.assertEqual(self.connection.query_metadata, self.raw_metadata)

    def test_query_data_reading(self):
        self.connection._get_query_result()
        comparison_data = self.connection.retrieved_data == self.raw_data
        self.assertTrue(all(comparison_data.dropna(axis=1).values.tolist()))

    def test_typing_result(self):
        self.connection._get_query_result()
        self.assertTrue(isinstance(self.connection.retrieved_data.dtypes["COMPANY_ID"], Int64Dtype))
        self.assertTrue(isinstance(self.connection.retrieved_data.dtypes["USED_WORDS_PERCENTAGE"], Float64Dtype))
        self.assertTrue(isinstance(self.connection.retrieved_data.dtypes["PROCESS_FLOW"], StringDtype))
        self.assertTrue(isinstance(self.connection.retrieved_data.dtypes["USER_ADMIN"], BooleanDtype))

if __name__ == '__main__':
    unittest.main()
