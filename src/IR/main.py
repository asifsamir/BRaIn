from elasticsearch import Elasticsearch

# Connect to Elasticsearch on localhost
es = Elasticsearch(hosts=['http://localhost:9200/'])

# Get the document count for the specified index
# try:
#     response = es.count(index='bench4blsum')
#     document_count = response['count']
#     print(f"Number of documents in the index : {document_count}")
#
# except Exception as e:
#     print(f"Error: {e}")


# Define the query to count documents with specific field values
query = {
    "query": {
        "bool": {
            "must": [
                {"match": {"project": "Previous"}},
                {"match": {"sub_project": "AspectJ"}},
            ]
        }
    }
}

# Get the count of documents matching the query
try:
    response = es.count(index='bench4bl', query=query['query'])
    document_count = response['count']
    print(f"Number of documents with project='a' and sub_project='b': {document_count}")

except Exception as e:
    print(f"Error: {e}")