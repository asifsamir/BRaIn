from Utils.IR_Evaluation_Metrics.Metrics.Evaluation_Metrics import AverageHit_At_K, \
    AverageRecall_At_K, MRR, MAP, AverageNDCG


class Performance_Evaluator:

    def __init__(self):
        self.map_metric = MAP()
        self.mrr_metric = MRR()
        self.recall_at_k = AverageRecall_At_K()
        self.hit_at_k = AverageHit_At_K()
        self.ndcg_at_k = AverageNDCG()

    '''Takes in a list of ground truths and a list of search results and returns a dictionary of performance metrics. 
    a search result should have the same index of the related ground truth.

    ground_truths: list of lists of ground truths
    search_results: list of lists of search results
    K: the K in recall@K and hit@K

    returns: dictionary of performance metrics

    Example:
    ground_truths = [[1, 2, 3], [4, 5, 6]]
    search_results = [[1, 2, 3], [4, 5, 6]]
    K = 3'''

    def evaluate(self, ground_truths, search_results, at_K):
        map_score = self.map_metric.calculate(ground_truths, search_results)
        mrr_score = self.mrr_metric.calculate(ground_truths, search_results)
        recall_score = self.recall_at_k.calculate(ground_truths, search_results, at_K)
        hit_score = self.hit_at_k.calculate(ground_truths, search_results, at_K)

        # ndcg_score = self.ndcg_at_k.calculate(ground_truths, search_results, at_K)

        # return them as a dictionary
        return {
            "map": map_score,
            "mrr": mrr_score,
            f"recall@{at_K}": recall_score,
            f"hit@{at_K}": hit_score,
            # f"ndcg@{at_K}": ndcg_score
        }

    def evaluate_several(self, ground_truths, search_results, at_Ks=[]):
        map_score = self.map_metric.calculate(ground_truths, search_results)
        mrr_score = self.mrr_metric.calculate(ground_truths, search_results)

        eval_performance_dict = {
            "map": map_score,
            "mrr": mrr_score,
        }
        for at_K in at_Ks:
            # recall_score = self.recall_at_k.calculate(ground_truths, search_results, at_K)
            hit_score = self.hit_at_k.calculate(ground_truths, search_results, at_K)
            # ndcg_score = self.ndcg_at_k.calculate(ground_truths, search_results, at_K)

            # eval_performance_dict[f"recall@{at_K}"] = recall_score
            eval_performance_dict[f"hit@{at_K}"] = hit_score
            # eval_performance_dict[f"ndcg@{at_K}"] = ndcg_score

        # return them as a dictionary
        return eval_performance_dict

        # print(f"MAP: {map_score:.4f}")
        # print(f"MRR: {mrr_score:.4f}")
        # print(f"Recall@{K}: {recall_score:.4f}")
        # print(f"Hit@{K}: {hit_score:.4f}")
        # print(f"Precision@{K}: {precision_score:.4f}")
        # # print(f"NDCG@{K}: {np.mean(ndcg_score):.4f}")

    def effective_query_at_k(self, ground_truths, bugreport_results, search_results, k):
        bugreport_results_best_rank_first = []
        search_results_best_rank_first = []

        for gt, bugreport_result, search_result in zip(ground_truths, bugreport_results, search_results):

            for index, file_url in enumerate(bugreport_result):
                if file_url in gt:
                    bugreport_results_best_rank_first.append(index + 1)
                    break

            for index, file_url in enumerate(search_result):
                if file_url in gt:
                    search_results_best_rank_first.append(index + 1)
                    break

        # now zip the two lists together to get the effective query at 1
        improved = 0
        worsened = 0
        preserved = 0

        # zip the two lists together
        for bugreport_result_rank, search_result_rank in zip(bugreport_results_best_rank_first, search_results_best_rank_first):
            if bugreport_result_rank < search_result_rank:
                worsened += 1
            elif bugreport_result_rank > search_result_rank:
                improved += 1
            else:
                preserved += 1



        # check percentage of improved, worsened and preserved
        total = improved + worsened + preserved
        improved_percentage = improved / total
        worsened_percentage = worsened / total
        preserved_percentage = preserved / total

        # create a dictionary to return
        effective_query_at_k_dict = {'improved_percentage': improved_percentage,
                                     'worsened_percentage': worsened_percentage,
                                     'preserved_percentage': preserved_percentage}

        return effective_query_at_k_dict