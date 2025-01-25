from datetime import datetime

from tqdm import tqdm

from IR import Searcher
from IR_Reretrieval.Indexer.Indexer_RE import Indexer_RE
from IR_Reretrieval.Searcher.Searcher_RE import Searcher_RE
from Utils.IO import JSON_File_IO, CSV_File_IO
from flair.embeddings import TransformerDocumentEmbeddings
from flair.data import Sentence


def load_dataframe(file_path):
    return JSON_File_IO.load_JSON_to_Dataframe(file_path)

def extract_unique_params(df):
    ng_left = set()
    ng_right = set()
    stop_words = set()
    nr_candidates = set()
    top_N = set()


    for index, row in df.iterrows():

        ng_left.add(row['n_gram_left'])
        ng_right.add(row['n_gram_right'])
        stop_words.add(row['stop_words'])
        nr_candidates.add(row['nr_candidates'])
        top_N.add(row['top_n'])


    return ng_left, ng_right, stop_words, nr_candidates, top_N


def get_best_query_dict(row, recommended_keyphrase):
    project = row['project']
    sub_project = row['sub_project']
    version = row['version']
    fixed_files = row['fixed_files']

    if project == None or sub_project == None or version == None or fixed_files == None:
        print('None value found')

    best_query_dict = {'project': project, 'sub_project': sub_project, 'version': version, 'fixed_files': fixed_files,
                       'query': recommended_keyphrase}

    return best_query_dict


def getOnlyFileUrlsAsList(results_dictionary_reranked):
    results = []
    for result in results_dictionary_reranked:
        results.append(result['file_url'])

    return results

def index_with_embedding(df, top_K_to_SEARCH=50):

    searcher = Searcher()
    indexer_re = Indexer_RE()


    already_indexed = set()

    # for index, row in df.iterrows():
    for index, row in tqdm(df.iterrows(), total=len(df), desc="Processing"):


        bug_title_description = row['bug_title'] + ' . ' + row['bug_description']


        results_dictionary = searcher.search_Extended(project=row['project'],
                                                      sub_project=row['sub_project'],
                                                      version=row['version'],
                                                      query=bug_title_description,
                                                      top_K_results=top_K_to_SEARCH,
                                                      field_to_return=['project',
                                                                       'sub_project',
                                                                       'version',
                                                                       'source_code',
                                                                       'file_url'])

        for result in results_dictionary:
        # for result in tqdm(results_dictionary, desc="Processing"):
            # check if the file is already indexed
            unique_ = str(row['bug_id']) + '_' + result['project'] + '_' + result['sub_project'] + '_' + result['version'] + '_' + result['file_url']
            if unique_ in already_indexed:
                continue
            else:
                # time = datetime.now()
                already_indexed.add(unique_)


                # indexer_re.index(project=result['project'],
                #                       sub_project=result['sub_project'],
                #                       version=result['version'],
                #                       source_code=result['source_code'],
                #                       file_url=result['file_url'],
                #                       bug_id=row['bug_id'])

                indexer_re.bulk_index(project=result['project'],
                                 sub_project=result['sub_project'],
                                 version=result['version'],
                                 source_code=result['source_code'],
                                 file_url=result['file_url'],
                                 bug_id=row['bug_id'])

                # print('Time taken for index: ', datetime.now() - time)

        # results = searcher.search(project=row['project'], sub_project=row['sub_project'], version=row['version'], query=recommended_keyphrases, top_K_results=top_K_results)
    indexer_re.refresh()





# def save_best_query_list_as_json(best_query_list, file_path, file_name):
#     JSON_File_IO.save_Dict_to_JSON(best_query_list, file_path=file_path, file_name=file_name)

def main():
    input_file_path = "D:\Research\Coding\Replication_Package\TransLocator\data\\bug_report_ds_refined_B4BL.json"

    df = load_dataframe(input_file_path)

    index_with_embedding(df, top_K_to_SEARCH=50)


    print('Done')



if __name__ == "__main__":
    main()
