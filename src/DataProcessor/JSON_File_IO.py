import json
import os

import pandas as pd

def load_JSON_to_Dataframe(file_path):
    with open(file_path) as f:
        combined_dict = json.load(f)
        df = pd.DataFrame(combined_dict)
        return df

def load_JSON_Dataframe_from_string(json_string):
    combined_dict = json.loads(json_string)
    df = pd.DataFrame(combined_dict)
    return df

def load_JSON_Dataframe_from_dict(combined_dict):
    df = pd.DataFrame(combined_dict)
    return df

def save_Dataframe_to_JSON(df, file_path):
    df_dict = df.to_dict(orient='records')
    with open(file_path, 'w') as f:
        json.dump(df_dict, f)

def save_Dict_to_JSON(dict, file_path, file_name):
    # check if the path exists, if not create it
    __create_folder_if_not_exists(file_path)

    file_path = os.path.join(file_path, file_name)

    with open(file_path, 'w') as f:
        json.dump(dict, f)


def load_JSON_to_Dict(file_path):
    # check if the path exists, if not throw an error
    if not os.path.exists(file_path):
        raise Exception('The file path does not exist')

    with open(file_path) as f:
        dict = json.load(f)
        return dict

def convert_Dataframe_to_JSON_string(df):
    df_dict = df.to_dict(orient='records')
    json_string = json.dumps(df_dict)
    return json_string

def __create_folder_if_not_exists(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

