import nltk
import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer


class TextPreprocessor:
    def __init__(self, use_stemmer=False, use_lemmatizer=False, remove_stopwords=True, return_tokens=True, remove_only_digits=True, remove_single_char=True, remove_SE_stop_words=False, lowercase=True):
        # Download NLTK resources if not already downloaded
        # nltk.download('punkt')
        # nltk.download('stopwords')
        self.stop_words = set(stopwords.words('english'))
        self.use_stemmer = use_stemmer
        self.use_lemmatizer = use_lemmatizer
        self.remove_stopwords = remove_stopwords
        self.is_return_tokens = return_tokens
        self.remove_only_digits = remove_only_digits
        self.remove_single_char = remove_single_char
        self.remove_SE_stop_words = remove_SE_stop_words
        self.lowercase = lowercase

        if self.use_stemmer:
            self.stemmer = PorterStemmer()
        if self.use_lemmatizer:
            # nltk.download('wordnet')
            self.lemmatizer = WordNetLemmatizer()

        if self.remove_SE_stop_words:
            # load java stop words from file to a list
            path_stop = 'D:\Research\Coding\QueryReformulation_MAIN\QueryReformulation_LLM\src\\Utils\StopWords\java_stops.txt'
            with open(path_stop, 'r') as file:
                self.java_stop_words = file.read().split('\n')

    def preprocess(self, text):
        # Tokenize the text
        # tokens = word_tokenize(text)
        # use re to tokenize the text

        # tokens = re.findall(r'\w+', text)
        # tokens = re.findall(r'\b(?!\.)[a-zA-Z0-9.]+\b', text)
        tokens = re.findall(r'\b(?:\w+\.)*\w+\b', text)

        # Remove punctuation and normalize
        # tokens = [self.normalize_token(token) for token in tokens]
        #
        # # Remove empty tokens
        # tokens = [token for token in tokens if token]
        #
        # # Remove stopwords
        # if self.remove_stopwords:
        #     tokens = [token for token in tokens if token not in self.stop_words]
        #
        # # Apply stemmer or lemmatizer if specified
        # if self.use_stemmer:
        #     tokens = [self.stemmer.stem(token) for token in tokens]
        # if self.use_lemmatizer:
        #     tokens = [self.lemmatizer.lemmatize(token) for token in tokens]

        # Initialize a list to store preprocessed tokens
        preprocessed_tokens = []

        for token in tokens:
            # Normalize and remove punctuation
            # normalized_token = self.normalize_token(token)

            # Remove only digits
            if self.remove_only_digits and token.isdigit():
                continue

            # Remove single character tokens
            if self.remove_single_char and len(token) == 1:
                continue

            # Skip empty tokens
            if token.strip() == '':
                continue

            # Optionally remove stopwords
            if self.remove_stopwords and token in self.stop_words:
                continue  # Skip stopwords

            # Optionally remove SE stopwords
            if self.remove_SE_stop_words and token in self.java_stop_words:
                continue

            # Optionally apply stemmer or lemmatizer
            if self.use_stemmer:
                token = self.stemmer.stem(token)
            if self.use_lemmatizer:
                token = self.lemmatizer.lemmatize(token)
            if(self.lowercase):
                token = token.lower()
            else:
                token = token
            preprocessed_tokens.append(token)

        if not self.is_return_tokens:
            return ' '.join(preprocessed_tokens)

        return preprocessed_tokens

    def normalize_token(self, token):
        # Remove punctuation and convert to lowercase
        token = re.sub(r'[^\w\s]', '', token)
        token = token.lower()
        return token


if __name__ == '__main__':
    # text = "public_static void main(String[] args) { System.out.println(\"Hello World\"); \n System.out.println(\"Hello World\"); }"
    # preprocessor = TextPreprocessor(use_stemmer=False, use_lemmatizer=True)
    # tokenized_text = preprocessor.preprocess(text)
    # print(tokenized_text)
    import re

    text = "This is a sample text. It includes words and some dots. But not a single dot.or like.this.  hconstants.hbase_rpc_timeout_key"

    # Find all tokens excluding single dots
    # tokens = re.findall(r'\b(?!\.)[a-zA-Z0-9.]+\b', text)
    tokens = re.findall(r'\b(?:\w+\.)*\w+\b', text)
    tokens = [token for token in tokens if token != '.']
    print(tokens)

