import os
import yaml

class ConfigLoader:
    def __init__(self, config_file_name="config.yaml"):
        # Define the configuration file path within the class
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.config_file_path = os.path.join(current_dir, config_file_name)
        self.config = self.load_config()

    def load_config(self):
        with open(self.config_file_path, "r") as config_file:
            config_data = yaml.safe_load(config_file)
        return config_data

    # return the value of the domain and key which are passed as parameter
    def get_value(self, domain, key):
        return self.config[domain][key]

    # get all the keys of a domain
    def get_keys(self, domain):
        return self.config[domain].keys()