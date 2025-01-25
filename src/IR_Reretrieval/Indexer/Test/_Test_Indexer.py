# import unittest
# from my_module.document_indexer import DocumentIndexer
#
# class _Test_Indexer(unittest.TestCase):
#     def setUp(self):
#         self.index_name = "test-index"
#         self.indexer = DocumentIndexer(index_name=self.index_name)
#
#     def test_index_creation(self):
#         document = {
#             "id": "1",
#             "title": "Example Title",
#             "text": "Example Text",
#             "embeddings": [0.2, 0.4, 0.1]
#         }
#         self.indexer.index(**document)
#
#         result = self.indexer.es_client.count(index=self.index_name)
#         total_documents = result.get("count", 0)
#
#         self.assertEqual(total_documents, 1)
#
# if __name__ == '__main__':
#     unittest.main()
