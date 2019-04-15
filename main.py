# Imports
import sampling_based_similarity
import KDD_strategy
import csv
import pandas as pd


# K-Nearest Neighbors Parameter Sets
THRESHOLD_T = [0,5]
THRESHOLD_D = [10,20]
NEIGHBORS_K = [20,30]

# Random Walk Parameter Sets
GAMMA = [.3,.6]
EPSILON = [.3,.6]
LENGTH = [5,15]
DELTA = [.3,.6]

# Other Parameters
TEST_FILES = ["tsvs/and/200.tsv","tsvs/and/500.tsv","tsvs/and/1000.tsv",
              "tsvs/or/100.tsv","tsvs/or/200.tsv","tsvs/or/500.tsv","tsvs/or/1000.tsv"]


with open("results.csv", mode="w") as results_file:
	results_writer = csv.writer(results_file)
	for file in TEST_FILES:
		print("for file",file)
		fields = ["SOURCE_SUBREDDIT","TARGET_SUBREDDIT","TIMESTAMP"]
		data = pd.read_csv(file, sep="\t",usecols=fields)
		# test knn with different parameters
		knn_params = [(T,D,K) for T in THRESHOLD_T for D in THRESHOLD_D for K in NEIGHBORS_K]
		for param_set in knn_params:
			print("\tfor knn-params",param_set)
			T,D,K = param_set
			avg_score, exact_guess_pct = KDD_strategy.knn_predict(data,T,D,K)
			alg_name = "knn_T=" + str(T) + "_D=" + str(D) + "_K=" + str(K)
			results_writer.writerow([alg_name,file,avg_score,exact_guess_pct])

		ts_vlp_params = [(G,E,L,D) for G in GAMMA for E in EPSILON for L in LENGTH for D in DELTA]
		for param_set in ts_vlp_params:
			print("\tfor tsvlp-params",param_set)
			G,E,L,D = param_set
			avg_score, exact_guess_pct = sampling_based_similarity.sampling_based_similarity_predict(data,G,.95,E,L,D)
			alg_name = "tsvlp_G=" + str(G) + "_E=" + str(E) + "_L=" + str(L) + "_D=" + str(D)
			results_writer.writerow([alg_name,file,avg_score,exact_guess_pct])

