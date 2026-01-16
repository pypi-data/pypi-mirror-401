import unittest
from unittest.mock import MagicMock
from sage_x3_requests import SageX3Requester, SageX3Config, SageX3QueryBuilder
from pydantic import SecretStr

class TestSageX3CountParam(unittest.TestCase):
    def setUp(self):
        self.config = SageX3Config(
            base_url="http://test.com",
            username="user",
            password="password",
            folder="TEST"
        )
        self.client = SageX3Requester(self.config)
        self.builder = SageX3QueryBuilder(self.client, "TEST_ENDPOINT", "TEST_REP")

    def test_count_as_bool_true(self):
        self.builder.count(True)
        params = self.builder._build_params()
        self.assertEqual(params.get("count"), 1)

    def test_count_as_bool_false(self):
        self.builder.count(False)
        params = self.builder._build_params()
        self.assertIsNone(params.get("count"))

    def test_count_as_int(self):
        self.builder.count(5)
        params = self.builder._build_params()
        self.assertEqual(params.get("count"), 5)

    def test_top_still_works(self):
        self.builder.top(10)
        params = self.builder._build_params()
        self.assertEqual(params.get("$top"), 10)

    def test_both_top_and_count(self):
        self.builder.top(10).count(5)
        params = self.builder._build_params()
        self.assertEqual(params.get("$top"), 10)
        self.assertEqual(params.get("count"), 5)

if __name__ == '__main__':
    unittest.main()
