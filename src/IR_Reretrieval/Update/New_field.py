from elasticsearch import Elasticsearch
from elasticsearch.helpers import reindex

# Connect to your Elasticsearch cluster
es = Elasticsearch('http://' + 'localhost' + ':' + str(9200),
                                       verify_certs=False)

# Define the new index mapping with a dense vector field
index_mapping = {
    "mappings": {
        "properties": {
            "embedding_codet5_S": {
                "type": "dense_vector",
                "dims": 512,
                "index": True,
                "similarity": "cosine",
            }
        }
    }
}

new_index_name = "bench4bl_emb"
index_exists = es.indices.exists(index=new_index_name)

if index_exists:
    response = es.indices.delete(index=new_index_name)

# Create the new index with the specified mapping
# es.indices.create(index=new_index_name, mappings=index_mapping["mappings"])
#
# # Reindex data from the old index to the new index
# reindex(es, source_index="bench4bl", target_index=new_index_name)

# Delete or alias indices (optional)
# To delete the old index:
# es.indices.delete(index="your_old_index")
# To create an alias for the new index:
# es.indices.put_alias(index="new_index", name="your_index_alias")
