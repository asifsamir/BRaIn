from elasticsearch import Elasticsearch

es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

index_name = "bench4bl_emb"
doc_type = "_doc"  # Elasticsearch 7.x and later use "_doc" as the doc type

# Define your search query
query = {
    "query": {
        "match_all": {}
    }
}

# Initialize the scroll
scroll = es.search(index=index_name, doc_type=doc_type, body=query, scroll=scroll_time)

# Retrieve and process documents in batches
while len(scroll['hits']['hits']) > 0:
    for hit in scroll['hits']['hits']:
        source_code = hit['_source']['source_code']
        # Embed source_code
        new_embedding = generate_embedding(source_code)  # Replace with your embedding logic

        # Update the document with the new embedding
        update_request = {
            "doc": {
                "embedding_codet5s": new_embedding
            }
        }

        es.update(index=index_name, id=hit['_id'], body=update_request)

    # Continue scrolling for the next batch of results
    scroll = es.scroll(scroll_id=scroll['_scroll_id'], scroll=scroll_time)

# Clear the scroll context when done
es.clear_scroll(scroll_id=scroll['_scroll_id'])
