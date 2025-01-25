import hashlib
import os
import json
from tqdm import tqdm
from scipy.special import softmax

from IR import Searcher
from IR_Reretrieval import Searcher_RE
from Utils import Performance_Evaluator
from Utils.IO import JSON_File_IO
from TextRank_KW_Search import TextRank

# Initialize TextRank
textRank = TextRank()


def re_search(bug_id, bug_title, bug_description, top_keywords, project, sub_project, version, responses=None,
              top_k=50):
    """Search and rerank the results based on the bug description and title."""
    url_score_dict = {}

    # Initialize the searcher
    searcher = Searcher_RE()

    # Perform the search
    score_dict = searcher.search_Extended(
        bug_id=bug_id,
        query=f"{bug_title} . {bug_description} . {top_keywords}",
        project=project,
        sub_project=sub_project,
        version=version,
        top_K_results=top_k,
        field_to_return=['file_url']
    )

    # Create a dictionary of file URLs and their BM25 scores
    for temp_dict in score_dict:
        file_url = temp_dict['file_url']
        bm25_score = temp_dict['bm25_score']
        url_score_dict[file_url] = bm25_score

    return url_score_dict


if __name__ == '__main__':
    json_path = "../../Output/Intelligent_Feedback/Mistral_ZERO_combined.json"
    with_test = True

    # Load JSON data into a dictionary
    json_bugs = JSON_File_IO.load_JSON_to_Dict(json_path)
    json_bugs_refined = []

    for bug in tqdm(json_bugs, desc="Processing JSON Bugs"):
        bug_id = bug['bug_id']
        bug_title = bug['bug_title']
        bug_description = bug['bug_description']
        project = bug['project']
        sub_project = bug['sub_project']
        version = bug['version']
        responses = None

        ground_truths = bug['fixed_files']
        es_results = bug['es_results']
        documents = []
        track_results = []
        continued_score = []
        bm25_scores = []

        # Initialize the source searcher
        source_searcher = Searcher()

        # Process search results
        for result in es_results:
            methods = result['methods']

            for method in methods:
                if methods[method] == 'yes':
                    file_url = result['file_url']
                    # Get the source code for relevant files
                    sr = source_searcher.search_field(
                        project=project,
                        sub_project=sub_project,
                        version=version,
                        field_to_search=file_url,
                        field_to_return=['source_code'],
                        top_K_results=1
                    )

                    try:
                        code_content = sr[0]['source_code']
                        documents.append(code_content)
                        break
                    except:
                        print(f"Error in getting source code for: {file_url}")
                        continue

        # Get top keywords based on documents
        top_keywords = ''
        if documents:
            query = f"{bug_title} . {bug_description}"
            top_keywords = textRank.get_keywords_CodeRank_3(query, documents, no_of_keywords=20, window_size=15)
            top_keywords = ' '.join(top_keywords)

        # Rerank the search results
        score_dict_re = re_search(bug_id, bug_title, bug_description, top_keywords, project, sub_project, version,
                                  responses)

        for result in es_results:
            file_url = result['file_url']
            track_results.append(file_url)
            bm25_score = result['bm25_score']
            bm25_scores.append(bm25_score)

            methods = result['methods']
            yes = any(methods[method] == 'yes' for method in methods)

            continued_score.append(1 if yes else 0.0)

        # Filter reranked results based on tracked results
        score_dict_re = {k: v for k, v in score_dict_re.items() if k in track_results}

        # Apply softmax to the reranked scores
        try:
            bm25_re_scores = softmax(list(score_dict_re.values()))
            score_dict_re = dict(zip(score_dict_re.keys(), bm25_re_scores))
        except Exception as e:
            print("Error in softmax:", e)
            continue

        # Calculate normalized scores
        scores = softmax(bm25_scores)
        score_dict = {}

        for index, file in enumerate(track_results):
            score_dict[file] = scores[index] * continued_score[index]

        # Sort the results based on the scores
        sorted_score_dict = dict(sorted(score_dict.items(), key=lambda item: item[1], reverse=True))
        search_results = list(sorted_score_dict.keys())

        # Update ground truths and ES results
        if not with_test:
            ground_truths = [file for file in ground_truths if 'test' not in file.split('.')[-2].lower()]

        if len(ground_truths) == 0:
            continue

        bug['fixed_files'] = ground_truths

        # Update ES results with new scores
        for result in es_results:
            file_url = result['file_url']
            result['bm25_score'] = sorted_score_dict.get(file_url, 0)

        # Sort ES results by BM25 score
        bug['es_results'] = sorted(es_results, key=lambda x: x['bm25_score'], reverse=True)
        json_bugs_refined.append(bug)

    # Save the refined JSON data
    save_file_path = "../../Output/Cache/"
    JSON_File_IO.save_Dict_to_JSON(json_bugs_refined, save_file_path, "Mistral_ZERO_sorted_cache.json", with_indent=True)
