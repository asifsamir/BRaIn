from elasticsearch import Elasticsearch
import json

from IR_Reretrieval.config.Elasic_Config_Loader import Elasic_Config_Loader


class Searcher_RE:
    def __init__(self, index_name=None):
        """
        Initialize the searcher. Make sure the elastic search is running.
        :param index_name: No need to pass this parameter unless some particular reason. It will be loaded from config file.
        """

        # Create an instance of ConfigLoader (config file will be loaded automatically)
        config_loader = Elasic_Config_Loader()

        # Accessing configuration parameters using class methods
        elastic_search_host = config_loader.get_elastic_search_host()
        elastic_search_port = config_loader.get_elastic_search_port()
        elastic_search_index = config_loader.get_index_name()

        if index_name is None:
            self.index_name = elastic_search_index
        else:
            self.index_name = index_name

        # Create an instance of Elasticsearch client
        self.es_client = Elasticsearch('http://' + elastic_search_host + ':' + str(elastic_search_port),
                                       # http_auth=("username", "password"),
                                       verify_certs=False, timeout=30)

    # def search(self, query, top_K_results=10):
    #     search_query = {
    #         "query": {
    #             "multi_match": {
    #                 "query": query,
    #                 "fields": ["source_code"]
    #             }
    #         },
    #         "size": top_K_results,
    #         "_source": ["file_url"]
    #     }
    #
    #     search_results = self.es_client.search(index=self.index_name, body=search_query)
    #
    #     ground_truths = self.compiled_search_results(search_results)
    #
    #     return ground_truths

    def search(self, bug_id, project, sub_project, version, query, top_K_results=10):
        search_query = {
                "bool": {
                    "must": [
                        {
                            "match": {
                                "project": project
                            }
                        },
                        {
                            "match": {
                                "sub_project": sub_project
                            }
                        },
                        {
                            "match": {
                                "version": version
                            }
                        },
                        {
                            "match": {
                                "bug_id": bug_id
                            }
                        }
                    ],
                    "should": [
                        {
                            # we are not searching in multiple fields. only in source_code
                            # "multi_match": {
                            #     "query": query,
                            #     "fields": ["source_code"]
                            # }
                            "match": {
                                "source_code": query
                            }
                            # "match": {
                            #     "source_code": {
                            #         "query": query,
                            #         "analyzer": "stop"  # Specify the custom analyzer here
                            #     }
                            # }
                        }
                        # You can add more "should" clauses here if needed.
                    ]
                }
            }

        # search_results = self.es_client.search(index=self.index_name, body=search_query)
        search_results = self.es_client.search(index=self.index_name, query=search_query, size=top_K_results, _source=["file_url"])

        results_file_urls = self.compiled_search_results(search_results)

        return results_file_urls


    def search_Extended(self, bug_id, project, sub_project, version, query, top_K_results=10, field_to_return=["file_url"]):
        search_query = {
                "bool": {
                    "must": [
                        {
                            "match": {
                                "project": project
                            }
                        },
                        {
                            "match": {
                                "sub_project": sub_project
                            }
                        },
                        {
                            "match": {
                                "version": version
                            }
                        },
                        {
                            "match": {
                                "bug_id": bug_id
                            }
                        }
                    ],
                    "should": [
                        {
                            # we are not searching in multiple fields. only in source_code
                            # "multi_match": {
                            #     "query": query,
                            #     "fields": ["source_code"]
                            # }
                            "match": {
                                "source_code": query
                            }
                        }
                        # You can add more "should" clauses here if needed.
                    ]
                }
            }

        # search_results = self.es_client.search(index=self.index_name, body=search_query)
        search_results = self.es_client.search(index=self.index_name, query=search_query, size=top_K_results, _source=field_to_return)

        result_dict = []

        for hit in search_results["hits"]["hits"]:
            score = hit['_score']
            source = hit.get("_source", {})

            temp_dict = {}
            temp_dict['bm25_score'] = score

            for field in field_to_return:
                temp_dict[field] = source.get(field)
            # project = source.get("project")
            # sub_project = source.get("sub_project")
            # version = source.get("version")
            # source_code = source.get("source_code")
            # file_url = source.get("file_url")
            # embedding_codet5s = source.get("embedding_codet5s")
            # embedding_codebert = source.get("embedding_codebert")
            # embedding_codet5base = source.get("embedding_codet5base")

            # result_dict.append({"project": project, "sub_project": sub_project, "version": version,
            #                     "source_code": source_code, "file_url": file_url,
            #                     "embedding_codet5s": embedding_codet5s,
            #                     "embedding_codebert": embedding_codebert})

            result_dict.append(temp_dict)
        return result_dict


    # def search_Extended(self, project, sub_project, version, query, top_K_results=10, field_to_return=["file_url"]):
    #     search_query = {
    #             "bool": {
    #                 "must": [
    #                     {
    #                         "match": {
    #                             "project": project
    #                         }
    #                     },
    #                     {
    #                         "match": {
    #                             "sub_project": sub_project
    #                         }
    #                     },
    #                     {
    #                         "match": {
    #                             "version": version
    #                         }
    #                     }
    #                 ],
    #                 "should": [
    #                     {
    #                         # we are not searching in multiple fields. only in source_code
    #                         # "multi_match": {
    #                         #     "query": query,
    #                         #     "fields": ["source_code"]
    #                         # }
    #                         "match": {
    #                             "source_code": query
    #                         }
    #                     }
    #                     # You can add more "should" clauses here if needed.
    #                 ]
    #             }
    #         }
    #
    #     # search_results = self.es_client.search(index=self.index_name, body=search_query)
    #     search_results = self.es_client.search(index=self.index_name, query=search_query, size=top_K_results, _source=field_to_return)
    #
    #     result_dict = []
    #
    #     for hit in search_results["hits"]["hits"]:
    #         score = hit['_score']
    #         source = hit.get("_source", {})
    #
    #         temp_dict = {}
    #         temp_dict['bm25_score'] = score
    #
    #         for field in field_to_return:
    #             temp_dict[field] = source.get(field)
    #         # project = source.get("project")
    #         # sub_project = source.get("sub_project")
    #         # version = source.get("version")
    #         # source_code = source.get("source_code")
    #         # file_url = source.get("file_url")
    #         # embedding_codet5s = source.get("embedding_codet5s")
    #         # embedding_codebert = source.get("embedding_codebert")
    #         # embedding_codet5base = source.get("embedding_codet5base")
    #
    #         # result_dict.append({"project": project, "sub_project": sub_project, "version": version,
    #         #                     "source_code": source_code, "file_url": file_url,
    #         #                     "embedding_codet5s": embedding_codet5s,
    #         #                     "embedding_codebert": embedding_codebert})
    #
    #         result_dict.append(temp_dict)
    #     return result_dict



    def if_exists(self, project, sub_project, version, file_url, top_K_results=10):
        search_query = {
                "bool": {
                    "must": [
                        {
                            "match": {
                                "project": project
                            }
                        },
                        {
                            "match": {
                                "sub_project": sub_project
                            }
                        },
                        {
                            "match": {
                                "version": version
                            }
                        },
                        {
                            "match": {
                                "file_url": file_url
                            }
                        }
                    ]
                }
            }

        # search_results = self.es_client.search(index=self.index_name, body=search_query)
        search_results = self.es_client.search(index=self.index_name, query=search_query, size=top_K_results, _source=["file_url"])

        results_file_urls = self.compiled_search_results(search_results)

        if len(results_file_urls) > 0:
            return True
        else:
            return False

    def compiled_search_results(self, search_results):

        suggested_all_source_files = []

        for hit in search_results["hits"]["hits"]:
            source = hit.get("_source", {})
            suggested_source_file = source.get("file_url")

            suggested_all_source_files.append(suggested_source_file)

        return suggested_all_source_files


# if __name__ == '__main__':
#     # Create an instance of Searcher
#     searcher = Searcher_RE()
#
#     # Search for a query
#     top_K_results = 10
#     search_results = searcher.search("Apache", "CAMEL", "camel-1.3.0", "propagated endpoint property propagated settings", 20)
#     # search_results = searcher.search_Extended("Apache", "CAMEL", "camel-1.3.0", "propagated endpoint property propagated settings", 20, field_to_return=['project', 'sub_project', 'version', 'source_code', 'file_url'])
#
#     # Print the search results
#     print(search_results)