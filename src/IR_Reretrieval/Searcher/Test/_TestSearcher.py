import unittest
from src.IR.Searcher import Searcher

class TestSearcher(unittest.TestCase):
    searcher = None
    @classmethod
    def setUpClass(cls) -> None:
        cls.searcher = Searcher()

    @classmethod
    def tearDown(self) -> None:
        self.searcher.es_client.close()

    # @classmethod
    # def setUp(self):
    #     self.searcher = Searcher()

    def test_search(self):
        # Search for a query
        top_K_results = 10
        search_results = self.searcher.search("Apache", "CAMEL", "camel-1.3.0",
                                         "propagated endpoint property propagated settings", top_K_results)
        self.assertEqual(len(search_results), top_K_results)



if __name__ == '__main__':
    unittest.main()
