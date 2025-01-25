import math
from collections import Counter

class Custom_BM25:

    def __init__(self, k1=1.5, b=0.75):
        """
        Initialize the BM25 object.

        :param idf_dict: Dictionary where keys are words and values are their IDF scores.
        :param k1: BM25 parameter, usually between 1.2 and 2.0 (default 1.5).
        :param b: BM25 parameter, usually between 0.75 and 1.0 (default 0.75).
        """
        self.idf_dict = {}
        self.loadIDF()
        self.k1 = k1
        self.b = b


    def loadIDF(self):
        file_path = "D:\Research\Data\idf_bench4bl.txt"
        # load the idf values from the file to a dictionary by splitting on tab
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                key, value = line.split('\t')
                self.idf_dict[key] = float(value)

    def compute_score(self, query, document):
        """
        Compute the BM25 score for a single document against a query.

        :param query: List of words representing the search query.
        :param document: List of words representing the document.
        :return: BM25 score for the document.
        """
        doc_len = len(document)
        doc_counter = Counter(document)
        avg_doc_len = sum(len(doc) for doc in documents) / len(documents)
        score = 0

        for term in query:
            # condition =  or
            if term in doc_counter and term in self.idf_dict:
                idf = self.idf_dict[term]
                term_freq = doc_counter[term]
                numerator = term_freq * (self.k1 + 1)
                denominator = term_freq + self.k1 * (1 - self.b + self.b * (doc_len / avg_doc_len))
                score += idf * (numerator / denominator)
            elif term.lower() in doc_counter and term.lower() in self.idf_dict:
                idf = self.idf_dict[term.lower()]
                term_freq = doc_counter[term.lower()]
                numerator = term_freq * (self.k1 + 1)
                denominator = term_freq + self.k1 * (1 - self.b + self.b * (doc_len / avg_doc_len))
                score += idf * (numerator / denominator)

        return score

    def compute_scores(self, query, documents):
        """
        Compute the BM25 scores for all documents in the collection against a query.

        :param query: List of words representing the search query.
        :return: List of BM25 scores corresponding to each document.
        """
        return [self.compute_score(query, doc) for doc in documents]

# Example usage:

# List of documents (each document is a list of words)
documents = [
    ["this", "is", "a", "sample", "document"],
    ["this", "document", "is", "another", "example", "document"],
    ["bm25", "is", "a", "ranking", "function", "for", "information", "retrieval"]
]



if __name__ == '__main__':
    # Initialize BM25 with documents and IDF dictionary
    bm25 = Custom_BM25()

    # Query
    query = ["document", "example"]

    # Compute BM25 scores for all documents
    bm25_scores = bm25.compute_scores(query, documents)
    print(bm25_scores)
