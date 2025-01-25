import csv
import pandas as pd
import os

def save_Dictionary_List_to_CSV(dictionary, file_path, file_name='test.csv'):
    # check the file path exists. if not, create the file path
    if not os.path.exists(file_path):
        os.makedirs(file_path)

    full_file_path = os.path.join(file_path, file_name)
    # convert the dictionary to a dataframe
    df = pd.DataFrame.from_dict(dictionary)
    df.to_csv(full_file_path, index=False)

def load_CSV_to_Dataframe(file_path, file_name):
    full_file_path = os.path.join(file_path, file_name)
    try:
        df = pd.read_csv(full_file_path)
    except Exception as e:
        print('Error loading the CSV file')
        print(e)
        return None
    return df


if __name__ == '__main__':
    save_Dictionary_List_to_CSV([{'a': 1, 'b': 2}, {'a': 2, 'b': 1}], 'D:/temp/', 'test.csv')