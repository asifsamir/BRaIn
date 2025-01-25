import json

from tqdm import tqdm

from Utils import JavaSourceParser
from Utils.IO import JSON_File_IO
from IR import Searcher


def load_dataframe(file_path):
    return JSON_File_IO.load_JSON_to_Dataframe(file_path)


def load_json_to_dict(file_path):
    return JSON_File_IO.load_JSON_to_Dict(file_path)


def perform_search(project, sub_project, version, bug_title, bug_description, top_K_results=10):
    searcher = Searcher('bench4bl')
    search_results = searcher.search_Extended(
        project=project,
        sub_project=sub_project,
        version=version,
        query=bug_title + '. ' + bug_description,
        top_K_results=top_K_results,
        field_to_return=["file_url", "source_code"]
    )

    # print(search_results)
    return search_results


def search_result_ops(search_results):
    processed_results = []
    for result in search_results:
        file_url = result['file_url']
        source_code = result['source_code']
        bm25_score = result['bm25_score']

        # parse the source code
        javaParser = JavaSourceParser(data=source_code)
        parsed_methods = javaParser.parse_methods()

        # create a json object with file_url and parsed_methods
        json_object = {
            'file_url': file_url,
            'methods': parsed_methods,
            'bm25_score': bm25_score
        }

        processed_results.append(json_object)

    return processed_results




if __name__ == '__main__':
    sample_path = "D:\Research\Coding\QueryReformulation_MAIN\Output\Expansion_Query\ob\\responses_hbase_ob_what_2.json"
    # load the json to dictionary
    df = load_dataframe(sample_path)

    # convert this to json string
    json_string = JSON_File_IO.convert_Dataframe_to_JSON_string(df)

    # iterate over the json string
    json_bugs = json.loads(json_string)

    # iterate over the json array
    for bug in tqdm(json_bugs, desc="Processing JSON Bugs"):
    # for bug in json_bugs:
        bug_title = bug['bug_title']
        bug_description = bug['bug_description']
        project = bug['project']
        sub_project = bug['sub_project']
        version = bug['version']

        # now search for the query in a method
        search_results = perform_search(project, sub_project, version, bug_title, bug_description, top_K_results=20)

        # now, perform ops in the search results
        processed_results = search_result_ops(search_results)

        # add processed results to the json as a new key
        bug['es_results'] = processed_results

    # save the json to a file
    json_save_path = "D:\Research\Coding\QueryReformulation_MAIN\Output\Expansion_Query\cached_methods"
    JSON_File_IO.save_Dict_to_JSON(json_bugs, json_save_path, "ES_results_cache_combined.json")
