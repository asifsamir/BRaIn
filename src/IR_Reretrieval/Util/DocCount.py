from elasticsearch import Elasticsearch

es = Elasticsearch('http://' + 'localhost' + ':' + str(9200),
                                       verify_certs=False)
index_name = "bench4bl"  # Replace with the name of your index

# Use the count method to get the number of documents in the index
doc_count = es.count(index=index_name)['count']

print(f"Number of documents in index '{index_name}': {doc_count}")
