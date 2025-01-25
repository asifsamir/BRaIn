from elasticsearch import Elasticsearch

# Connect to Elasticsearch on localhost
es = Elasticsearch(hosts=['http://localhost:9200/'])
