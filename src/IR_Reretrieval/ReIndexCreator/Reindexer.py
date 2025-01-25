from datetime import datetime

from tqdm import tqdm

from src import TextPreprocessor
from src.IR import Searcher
from src.IR_Reretrieval.Indexer.Indexer_RE import Indexer_RE
from src.IR_Reretrieval.Searcher.Searcher_RE import Searcher_RE
from src.Utils.IO import JSON_File_IO, CSV_File_IO
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

def index_with_embedding(df, top_K_to_SEARCH=100):

    searcher = Searcher()
    indexer_re = Indexer_RE()

    # model_codebert = TransformerDocumentEmbeddings('microsoft/codebert-base')
    # model_codet5 = TransformerDocumentEmbeddings('Salesforce/codet5-small')
    # model_codet5base = TransformerDocumentEmbeddings('Salesforce/codeT5-base')
    model_codebert = TransformerDocumentEmbeddings('microsoft/codebert-base')
    model_codet5 = TransformerDocumentEmbeddings('F:\\Models\\Pretrained_bugreport_2')
    model_codet5base = TransformerDocumentEmbeddings('Salesforce/codeT5-base')

    preprocessor = TextPreprocessor(remove_stopwords=False)

    already_indexed = set()

    # for index, row in df.iterrows():
    for index, row in tqdm(df.iterrows(), total=len(df), desc="Processing"):


        project = row['project'] # for testing summary
        sub_project = row['sub_project']# for testing summary
        version = row['version']# for testing summary

        if project != 'Previous' and sub_project != 'AspectJ':# for testing summary
            continue# for testing summary
        else:
            sub_project = 'AspectJ_2'# for testing summary

        # recommended_keyphrases = row['keywords']
        # recommended_keyphrases = row['keywords_limited_.6']

        bug_title_description = row['bug_title'] + ' . ' + row['bug_description']



        results_dictionary = searcher.search_Extended(project=project,
                                                      sub_project=sub_project,
                                                      version=version,
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
            unique_ = result['project'] + '_' + result['sub_project'] + '_' + result['version'] + '_' + result['file_url']

            project = result['project']
            sub_project = result['sub_project']
            version = result['version']
            file_url = result['file_url']
            source_code = result['source_code']

            if unique_ in already_indexed:
                continue
            else:
                # time = datetime.now()
                already_indexed.add(unique_)

                source = result['source_code']
                preprocessed = preprocessor.preprocess(source)
                # source = ' '.join(preprocessed)
                unique_preprocesssed = set(preprocessed)
                source = ' '.join(unique_preprocesssed)

                sentence = Sentence(source)
                model_codet5.embed(sentence)
                codet5s_embedding = sentence.get_embedding().tolist()


                sentence = Sentence(source)
                model_codebert.embed(sentence)
                codebert_embedding = sentence.get_embedding().tolist()

                sentence = Sentence(source)
                model_codet5base.embed(sentence)
                codet5base_embedding = sentence.get_embedding().tolist()

                # results_dictionary['embedding_codet5s'] = codet5s_embedding
                # results_dictionary['embedding_codebert'] = codebert_embedding

                indexer_re.index(project=project,
                                      sub_project=sub_project,
                                      version=version,
                                      source_code=source_code,
                                      file_url=file_url,
                                      embedding_codet5s=codet5s_embedding,
                                      embedding_codebert=codebert_embedding,
                                      embedding_codet5base=codet5base_embedding)

                # print('Time taken for index: ', datetime.now() - time)

        # results = searcher.search(project=row['project'], sub_project=row['sub_project'], version=row['version'], query=recommended_keyphrases, top_K_results=top_K_results)
    indexer_re.refresh()





# def save_best_query_list_as_json(best_query_list, file_path, file_name):
#     JSON_File_IO.save_Dict_to_JSON(best_query_list, file_path=file_path, file_name=file_name)

def main():
    input_file_path = 'D:\Research\Coding\QueryReformulation_MAIN\QueryReformulation_LLM\Output\Generation\KeyBert_codet5small_mmr_ALL_DATA_BEST_ALL_34_tf_3Ext.json'

    df = load_dataframe(input_file_path)

    index_with_embedding(df, top_K_to_SEARCH=100)


    print('Done')



if __name__ == "__main__":
    main()
