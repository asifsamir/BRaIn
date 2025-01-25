import yaml
import os

class Elasic_Config_Loader:
    def __init__(self, config_file_name="IR_config_2.yaml"):
        # Define the configuration file path within the class
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.config_file_path = os.path.join(current_dir, config_file_name)
        self.config = self.load_config()

    def load_config(self):
        with open(self.config_file_path, "r") as config_file:
            config_data = yaml.safe_load(config_file)
        return config_data

    def get_elastic_search_host(self):
        return self.config["elasticsearch"]["host"]

    def get_elastic_search_port(self):
        return self.config["elasticsearch"]["port"]

    def get_index_name(self):
        return self.config["elasticsearch"]["index_name"]

    def get_index_fields(self):
        return self.config["Fields"]


if __name__ == "__main__":
    # Create an instance of ConfigLoader (config file will be loaded automatically)
    config_loader = Elasic_Config_Loader()

    # Accessing configuration parameters using class methods
    elastic_search_host = config_loader.get_elastic_search_host()
    elastic_search_port = config_loader.get_elastic_search_port()

    print(f"Elastic Search Host: {elastic_search_host}")
    print(f"Elastic Search Port: {elastic_search_port}")