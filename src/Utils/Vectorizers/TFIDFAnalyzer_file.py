import pickle
from Utils.NLP.TextPreprocessor import TextPreprocessor

class TFIDFAnalyzer:
    def __init__(self, tfidf_vectorizer_path):
        # Load the pre-trained TF-IDF vectorizer from the provided path
        with open(tfidf_vectorizer_path, 'rb') as file:
            self.tfidf_vectorizer = pickle.load(file)

        # Create a text preprocessor with your desired settings
        self.preprocessor = TextPreprocessor(
            remove_stopwords=True,
            remove_only_digits=True,
            remove_single_char=True,
            use_stemmer=False,
            use_lemmatizer=False
        )

    def analyze_text(self, text, top_n=3, preprocessed=False):
        # Preprocess the input text
        if preprocessed:
            preprocessed = self.preprocessor.preprocess(text)
            preprocessed_text = ' '.join(preprocessed)
        else:
            preprocessed_text = text

        # Transform the preprocessed text using the pre-trained vectorizer
        tfidf_vectors = self.tfidf_vectorizer.transform([preprocessed_text])

        # Convert the TF-IDF vectors to a dense matrix
        dense_matrix = tfidf_vectors.todense()

        # Get the feature names (n-grams) from the vectorizer
        feature_names = self.tfidf_vectorizer.get_feature_names_out()

        # Calculate the TF-IDF scores for each n-gram in the new text
        tfidf_scores = dense_matrix[0].tolist()[0]

        # Create a list of (feature_name, tfidf_score) pairs
        feature_tfidf_pairs = list(zip(feature_names, tfidf_scores))

        # Sort the n-grams by TF-IDF score in descending order
        sorted_feature_tfidf_pairs = sorted(feature_tfidf_pairs, key=lambda x: x[1], reverse=True)

        # Get the top 3 n-grams with the highest TF-IDF scores
        top_3_grams = sorted_feature_tfidf_pairs[:top_n]

        # Return the top 3 n-grams with their TF-IDF scores
        return top_3_grams

# Usage:
if __name__ == "__main__":
    analyzer = TFIDFAnalyzer('D:\Research\Coding\QueryReformulation_MAIN\QueryReformulation_LLM\Output\Vectorized_Data\\tfidf_vectorizer_3_4.pkl')
    sample_bug_report = 'problem with the code. the code is not working . getting nullpointer exception . when I run java code'
    top_3_grams = analyzer.analyze_text(sample_bug_report)
    print(top_3_grams)
