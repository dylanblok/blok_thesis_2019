import datetime
from datetime import date
from monthdelta import *
from sklearn.neighbors import KNeighborsRegressor
from pathlib import Path
from enum import Enum

# TIME CONSTANTS
MIN_DATE = date(2014,1,1)
MAX_DATE = date(2017,3,1)
TOTAL_MONTHS = 38
DELTA = monthdelta(1)

def knn_predict(data, T=0, D=10, K=20):
	links_per_month, solutions = refs_per_month(data)
	dif = dif_per_month(links_per_month)
	guesses_per_subreddit = predict_with_knn(links_per_month,dif,T,D,K)
	avg_dist, exact_guess_pct = calculate_score(links_per_month,guesses_per_subreddit,solutions)
	return avg_dist, exact_guess_pct

def refs_per_month(data):
	links_per_month = {}
	solutions = {}
	for i in range(len(data)):
		source = data.values[i][0]
		target = data.values[i][1]
		y,m,d = map(int,data.values[i][2].split(" ")[0].split("-"))
		hl_month = date(y,m,1)
		if hl_month < MAX_DATE:
			if target in links_per_month:
				if hl_month in links_per_month[target]:
					links_per_month[target][hl_month] += 1
				else:
					links_per_month[target][hl_month] = 1
			else:
				links_per_month[target] = {hl_month: 1}
		elif hl_month == MAX_DATE:
			if target in solutions:
				solutions[target] += 1
			else:
				solutions[target] = 1
	return links_per_month, solutions

def dif_per_month(links_per_month):
	dif = {}
	for subreddit in links_per_month:
		if subreddit not in dif:
			dif[subreddit] = {}
		for month in links_per_month[subreddit]:
			if month - monthdelta(1) in links_per_month[subreddit]:
				dif[subreddit][month] = links_per_month[subreddit][month] - links_per_month[subreddit][month-monthdelta(1)]
			else:
				dif[subreddit][month] = links_per_month[subreddit][month]
	return dif


def predict_with_knn(links_per_month,dif,T=0,D=10,K=20):
	knn_train_data = []
	knn_train_targets = []
	knn_test_data = []
	tested = []
	for subreddit in links_per_month:
		tested.append(subreddit)
		for month in links_per_month[subreddit]:
			if links_per_month[subreddit][month] > T:
				knn_train_targets.append(dif[subreddit][month])
				training_data = []
				for i in range(D,0,-1):
					if month - monthdelta(i) in dif[subreddit]:
						training_data.append(dif[subreddit][month - monthdelta(i)])
					else:
						training_data.append(0)
				knn_train_data.append(training_data)
		testing_data = []
		for j in range(D,0,-1):
			if MAX_DATE - monthdelta(j) in dif[subreddit]:
				testing_data.append(dif[subreddit][MAX_DATE - monthdelta(j)])
			else:
				testing_data.append(0)
		knn_test_data.append(testing_data)

	# knn regression
	neigh = KNeighborsRegressor(n_neighbors = K)
	neigh.fit(knn_train_data,knn_train_targets)
	guesses = neigh.predict(knn_test_data)

	return dict(zip(tested,guesses))


def calculate_score(links_per_month,guesses_per_subreddit, solutions):
	scores = []

	exact_guesses = 0
	for subreddit in solutions:
		if subreddit in guesses_per_subreddit:
			if MAX_DATE-monthdelta(1) not in links_per_month[subreddit]:
				final_guess = int(round(guesses_per_subreddit[subreddit]))
			else:
				final_guess = links_per_month[subreddit][MAX_DATE-monthdelta(1)] + int(round(guesses_per_subreddit[subreddit]))
			scores.append(abs(int(round(solutions[subreddit])) - final_guess))
			if int(round(solutions[subreddit])) == final_guess:
				exact_guesses += 1
		else:
			scores.append(int(round(solutions[subreddit])))
			if int(round(solutions[subreddit])) == 0:
				exact_guesses += 1
	avg_dist = sum(scores)/len(solutions)
	exact_guess_pct = 100*exact_guesses/len(solutions)
	return avg_dist, exact_guess_pct




# avg = 0
# if subreddit in links_per_month:
# 	if MAX_DATE-monthdelta(1) not in links_per_month[subreddit]:
# 		prevs_score += solutions[subreddit]
# 	else:
# 		prevs_score += abs(solutions[subreddit] - links_per_month[subreddit][MAX_DATE-monthdelta(1)])
# 	for mo in links_per_month[subreddit]:
# 		avg += links_per_month[subreddit][mo]
# 	avgs_score += abs(solutions[subreddit] - (avg//TOTAL_MONTHS))
# else:
# 	prevs_score += solutions[subreddit]
# 	avgs_score += solutions[subreddit]



