import json

from tqdm import tqdm

from Utils import JavaSourceParser
from Utils.IO import JSON_File_IO
from IR import Searcher
from Utils.Parser import SourceRefiner


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


        json_result = java_py4j_ast_parser.processJavaFileContent(source_code)

        if json_result is None or json_result == '':
            # parse the source code if py4j fails
            javaParser = JavaSourceParser(data=source_code)
            parsed_methods = javaParser.parse_methods()

        else:
            loaded_json = json.loads(json_result)
            parsed_methods = {}

            poly_morphism = 1
            # iterate over the parsed methods and get the method names and the method bodies
            for method in loaded_json:

                method_name = method['member_name']
                method_body = method['member_body']
                class_name = method['class_name']

                # clear the formatting of the method body for tokenization
                method_body = SourceRefiner.clear_formatting(method_body)

                # check if the method name is already in the parsed_methods
                if method_name in parsed_methods:
                    # append the method body to the existing method name
                    parsed_methods[method_name+'!P'+str(poly_morphism)] = 'Class: '+ class_name + ' \n Method: ' + method_body
                    poly_morphism += 1
                else:
                    parsed_methods[method_name] = 'Class: '+ class_name + ' \n Method: ' + method_body



        # create a json object with file_url and parsed_methods
        json_object = {
            'file_url': file_url,
            'methods': parsed_methods,
            'bm25_score': bm25_score
        }

        processed_results.append(json_object)

    return processed_results



from py4j.java_gateway import JavaGateway

gateway = JavaGateway()  # connect to the JVM
java_py4j_ast_parser = gateway.entry_point.getJavaMethodParser()  # get the HelloWorld instance
# print(hello_world.sayHello("World"))  # call the sayHello method
#
#
# sum_result = hello_world.addNumbers(10, 20)
if __name__ == '__main__':
    # sample_path = "D:\Research\Coding\QueryReformulation_MAIN\Output\Expansion_Query\ob\\responses_hbase_ob_what_2.json"
    sample_path = "D:\Research\Coding\QueryReformulation_MAIN\Output\Expansion_Query\\refined_dataset\\bug_report_ds_refined_B4BL.json"
    # load the json to dictionary
    df = load_dataframe(sample_path)

    # convert this to json string
    json_string = JSON_File_IO.convert_Dataframe_to_JSON_string(df)

    # iterate over the json string
    json_bugs = json.loads(json_string)

    # create multiple json files for each project and sub_project
    json_bugs_project = {}

    for bug in json_bugs:
        project = bug['project']
        sub_project = bug['sub_project']
        proj_sub_proj = project + '_' + sub_project


        if proj_sub_proj in json_bugs_project:
            json_bugs_project[proj_sub_proj].append(bug)
        else:
            json_bugs_project[proj_sub_proj] = [bug]

    # iterate over the json_bugs_project. after processing the json, save the json to a file as a cache project_subproject.json
    for proj_sub_proj in tqdm(json_bugs_project, desc="Processing Project SubProject"):
        json_bugs = json_bugs_project[proj_sub_proj]
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
        json_save_path = "D:\Research\Coding\QueryReformulation_MAIN\Output\Expansion_Query\cached_methods\\20_results"
        JSON_File_IO.save_Dict_to_JSON(json_bugs, json_save_path, proj_sub_proj+"_Cached_Method_20.json")


    # # iterate over the json array
    # for bug in tqdm(json_bugs, desc="Processing JSON Bugs"):
    # # for bug in json_bugs:
    #     bug_title = bug['bug_title']
    #     bug_description = bug['bug_description']
    #     project = bug['project']
    #     sub_project = bug['sub_project']
    #     version = bug['version']
    #
    #     # now search for the query in a method
    #     search_results = perform_search(project, sub_project, version, bug_title, bug_description, top_K_results=20)
    #
    #     # now, perform ops in the search results
    #     processed_results = search_result_ops(search_results)
    #
    #     # add processed results to the json as a new key
    #     bug['es_results'] = processed_results
    #
    # # save the json to a file
    # json_save_path = "D:\Research\Coding\QueryReformulation_MAIN\Output\Expansion_Query\cached_methods"
    # JSON_File_IO.save_Dict_to_JSON(json_bugs, json_save_path, "ES_results_cache_combined_20.json")
