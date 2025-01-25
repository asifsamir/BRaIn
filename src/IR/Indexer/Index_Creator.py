from elasticsearch import Elasticsearch

from IR.config.Elasic_Config_Loader import Elasic_Config_Loader

'''
    CAUTION:
    This is used to create an index in elastic search. This needs to be run only once. running it again will delete the index and create a new one.
    Before running this, make sure to update the config file and fields. 
    
    Before running this, make sure elastic search is running. See readme for more details.
'''


class Index_Creator:
    def __init__(self):
        # Create an instance of ConfigLoader (config file will be loaded automatically)
        self.config_loader = Elasic_Config_Loader("../config/IR_config.yaml")
        # self.general_config_loader = ConfigLoader("../config/IR_config.yaml")

        # Accessing configuration parameters using class methods
        self.elastic_search_host = self.config_loader.get_elastic_search_host()
        self.elastic_search_port = self.config_loader.get_elastic_search_port()
        elastic_search_index = self.config_loader.get_index_name()
        # self.embedding_dimension = self.general_config_loader.get_value("Embedding", "dimension")

        self.index_name = elastic_search_index

        self.fields = self.config_loader.get_index_fields()

        # get the name of the fields as a list
        self.fields_names = list(self.fields.keys())

        # Create an instance of Elasticsearch client
        self.es_client = Elasticsearch(
            'http://' + self.elastic_search_host + ':' + str(self.elastic_search_port),
            verify_certs=False
        )

    def create_index(self, delete_if_exists=False):
        config = {
            "mappings": {
                "properties": {
                    field_name: {"type": field_type}
                    for field_name, field_type in self.fields.items()
                }
            },
            "settings": {
                "index": {
                    "number_of_shards": 3,
                    "number_of_replicas": 0,
                    "refresh_interval": "30s",
                    # 'index_buffer_size': '512mb',
                }
            }
        }

        index_exists = self.es_client.indices.exists(index=self.index_name)

        # Print the result
        if index_exists:
            print(f"Index '{self.index_name}' already exists.")

            if delete_if_exists:
                print(f"Deleting index '{self.index_name}'.")
                response = self.es_client.indices.delete(index=self.index_name)
                # Check if the deletion was successful
                if response['acknowledged']:
                    print(f"The index '{self.index_name}' was successfully deleted.")
                else:
                    print(f"Failed to delete the index '{self.index_name}'.")
            else:
                print(f"Index '{self.index_name}' will not be deleted.")
                return
        else:
            print(f"Index '{self.index_name}' does not exist.")

        self.es_client.indices.create(
            index=self.index_name,
            mappings=config["mappings"],
            settings=config["settings"]
        )

        # Check if the index has been created successfully
        if self.es_client.indices.exists(index=self.index_name):
            print(f"The index '{self.index_name}' was created successfully.")
        else:
            print(f"Failed to create the index '{self.index_name}'.")


if __name__ == '__main__':
    index_creator = Index_Creator()
    index_creator.create_index(delete_if_exists=True)
