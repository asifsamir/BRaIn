# we retrieve 50 documents using elasticsearch. now i want to search again to rerank with a different  query on this initally retrieved document using elasticsearch. is it possible?

from elasticsearch import Elasticsearch

# Initialize the Elasticsearch client
es = Elasticsearch("http://localhost:9200")

# Perform the initial search to retrieve the top 50 documents
initial_search = es.search(
    index="your_index",
    body={
        "query": {
            "match": {
                "your_field": "initial query"
            }
        },
        "size": 50
    }
)

# Extract the document IDs from the initial search results
doc_ids = [hit['_id'] for hit in initial_search['hits']['hits']]

# Perform the rescore query to rerank the documents
rescore_search = es.search(
    index="your_index",
    body={
        "query": {
            "ids": {
                "values": doc_ids
            }
        },
        "rescore": {
            "window_size": 50,
            "query": {
                "rescore_query": {
                    "match": {
                        "your_field": "new query"
                    }
                },
                "query_weight": 0.7,
                "rescore_query_weight": 1.2
            }
        }
    }
)

# Print the reranked search results
for hit in rescore_search['hits']['hits']:
    print(hit['_source'])
