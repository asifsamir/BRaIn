'''Vectorize the text using TF-IDF vectorizer using sklearn and save it to a file'''
import os.path
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer

from Utils.IO import JSON_File_IO


class TfidfVectorizerWithPersistence:
    def __init__(self, vectorizer=None):
        if vectorizer is None:
            self.vectorizer = TfidfVectorizer(max_df=0.6, use_idf=True, smooth_idf=True, norm='l2', ngram_range=(3, 4))
        else:
            self.vectorizer = vectorizer

    def fit_and_return(self):
        input_file_path = 'D:\Research\Coding\QueryReformulation_MAIN\QueryReformulation_LLM\Dataset\Combined_queries.json'

        # load the dataframe from the file and iterate over it and create a corpus
        df = JSON_File_IO.load_JSON_to_Dataframe(input_file_path)

        corpus = []

        for index, row in df.iterrows():
            corpus.append(row['bug_description'] + ' . ' + row['bug_title'])

        self.vectorizer.fit(corpus)

        return self.vectorizer

    def fit_and_save(self, corpus, filename):
        self.vectorizer.fit(corpus)
        with open(filename, 'wb') as file:
            pickle.dump(self.vectorizer, file)

    def load_and_transform(self, filename, new_data):
        with open(filename, 'rb') as file:
            self.vectorizer = pickle.load(file)
        return self.vectorizer.transform(new_data)


if __name__ == '__main__':
    input_file_path = 'D:\Research\Coding\QueryReformulation_MAIN\Output\QueryReformulation_Files\Output\Generation\KeyBert_codet5small_mmr_ALL_DATA_34.json'
    output_dir = 'D:\Research\Coding\QueryReformulation_MAIN\QueryReformulation_LLM\Output\Vectorized_Data\\'

    # load the dataframe from the file and iterate over it and create a corpus
    df = JSON_File_IO.load_JSON_to_Dataframe(input_file_path)

    corpus = []

    for index, row in df.iterrows():
        corpus.append(row['bug_description'] + ' . ' + row['bug_title'])


    # Example usage:
    # # Instantiate the custom TfidfVectorizerWithPersistence class
    tfidf_persistence = TfidfVectorizerWithPersistence()


    tfidf_persistence.fit_and_save(corpus, os.path.join(output_dir, 'tfidf_vectorizer_3_4.pkl'))

    # Load the vectorizer from a file and transform new data
    # new_data = ["A new document for testing.", "Another test document. java lang"]
    # transformed_data = tfidf_persistence.load_and_transform(os.path.join(output_dir, 'tfidf_vectorizer.pkl'), new_data)
    # print("Transformed Data:")
    # print(transformed_data.toarray())
    # print(sum(transformed_data))
    #
    # # check if there is any value other than 0
    # for i in range(len(transformed_data.toarray())):
    #
    #         if sum(transformed_data.toarray()[i]) > 0:
    #             print(new_data[i])
    #             print(transformed_data.toarray()[i])
    #             print(sum(transformed_data.toarray()[i]))
    #             print('------------------')

