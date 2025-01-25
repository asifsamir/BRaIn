from Utils.Vectorizers import TFIDFAnalyzer


class TfIDF_Analyzer_manager:
    def __init__(self):
        self.analyzer = TFIDFAnalyzer(
            'D:\Research\Coding\QueryReformulation_MAIN\QueryReformulation_LLM\Output\Vectorized_Data\\tfidf_vectorizer_3_4.pkl')
        # sample_bug_report = 'problem with the code. the code is not working . getting nullpointer exception . when I run java code'


    def get_top_keywords(self, bugreport, keywords, top_n=15):
        top_n_grams = self.analyzer.analyze_text(bugreport)

        top_n_grams = ' '.join(top_n_grams)
        top_n_grams = top_n_grams.split(' ')

        keywords = keywords.split(' ')
        keywords_to_return = []

        # return only top_n keywords that are in the keywords list
        for keyword in top_n_grams:
            if keyword in keywords:
                keywords_to_return.append(keyword)
                if len(keywords_to_return) == top_n:
                    break

        return keywords_to_return


