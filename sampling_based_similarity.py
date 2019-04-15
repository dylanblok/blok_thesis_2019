import networkx as nx
import numpy
from scipy.interpolate import interp1d, PchipInterpolator, CubicSpline
from datetime import date, timedelta
import monthdelta as md
import math

# TIME CONSTANTS
MIN_DATE = date(2014,1,1)
MAX_DATE = date(2017,3,1)
TIME_DELTA = md.monthdelta(1)
NUM_DELTAS = 38

def sampling_based_similarity_predict(data,GAMMA=0.6,C=.95,EPSILON=0.3,L=15,DELTA=0.3):
	sub_data = data[(data['TIMESTAMP'] >= MIN_DATE.isoformat())]
	nodes = list(set(sub_data["SOURCE_SUBREDDIT"].tolist() + sub_data["TARGET_SUBREDDIT"].tolist()))

	adj_matrices, solutionMatrix = create_temporal_network(data,nodes,GAMMA)

	x = ts_vlp(adj_matrices,nodes,C,EPSILON,L,DELTA)

	# Normalize similarity scores
	final_month = adj_matrices[MAX_DATE-md.monthdelta(1)]
	max_degree = 0
	for i in range(len(x)):
		for j in range(len(x)):
			max_degree = max(max_degree,2*(1+final_month[i][j]+final_month[j][i]))

	norm = interp1d([0,numpy.amax(x)],[0,max_degree])
	x = norm(x)


	# Distribute directed edges
	for i in range(len(x)):
		for j in range(len(x)):
			ij = final_month[i][j]
			ji = final_month[j][i]
			if ij+ji > 0:
				x[i][j] = x[i][j] * ij/(ij+ji)
				x[j][i] = x[j][i] * ji/(ij+ji)
			else:
				x[i][j] = x[i][j]
				x[j][i] = x[j][i]

	D = numpy.sum(x, axis=1)
	solution_D = numpy.sum(solutionMatrix, axis=1)
	avg_dist, exact_guess_pct = calculate_score(D,solution_D,nodes)
	return avg_dist, exact_guess_pct

def calculate_score(D,solution_D,nodes):
	scores =[]
	guesses=[]

	exact_guesses = 0

	for i in range(len(D)):
		scores.append(abs(int(D[i])-int(solution_D[i])))
		guesses.append(int(D[i]))
		if int(D[i]) == int(solution_D[i]):
			exact_guesses += 1

	avg_dist = sum(scores)/len(nodes)
	exact_guess_pct = 100*exact_guesses/len(nodes)
	return avg_dist, exact_guess_pct


### CREATE TEMPORAL NETWORK ###
def create_temporal_network(data,nodes,GAMMA):
	graphs = {}
	adj_matrices = {}
	currentDate = MIN_DATE
	delta_num = 1
	solutionMatrix = numpy.zeros([len(nodes),len(nodes)])

	while(currentDate <= MAX_DATE):
		sub_data = data[(data['TIMESTAMP'] >= currentDate.isoformat()) & (data['TIMESTAMP'] < (currentDate+TIME_DELTA).isoformat())]

		# create graph
		G = nx.MultiDiGraph()
		for node in nodes:
			G.add_node(node)

		for index, row in sub_data.iterrows():
			G.add_edge(row['SOURCE_SUBREDDIT'],row['TARGET_SUBREDDIT'],t=row['TIMESTAMP'])
		graphs[currentDate] = G

		A = nx.adj_matrix(G)
		A = A.todense()
		A = numpy.array(A, dtype = numpy.float64)
		if currentDate < MAX_DATE:
			A *= (GAMMA**(NUM_DELTAS-delta_num))
			adj_matrices[currentDate] = A
		else:
			solutionMatrix = A

		delta_num += 1
		currentDate += TIME_DELTA

	return adj_matrices, solutionMatrix


### ALGORITHM IMPLEMENTATION ###

def ts_vlp(adj_matrices,nodes,C,EPSILON,L,DELTA):

	A = sum(adj_matrices.values())

	T_prime = numpy.zeros([len(nodes),len(nodes)])
	for x in range(len(A)):
		print(x+1,"/",len(A),end="\r")
		T_prime_x = vlp(x,A,nodes,C,EPSILON,L,DELTA)
		T_prime[x] = T_prime_x
	print()
	# calculate degree of each node
	D = numpy.sum(A, axis=1)
	# calculate q values (initial configuration for probability calculations)
	q = D / (numpy.sum(A,axis=None)/2)
	i = T_prime.shape[0]
	j = T_prime.shape[1]
	S = numpy.zeros([len(nodes),len(nodes)])
	# calculate similarity scores based on q and T-prime values
	for x in range(0,i):
		for y in range(0,j):
			S[x][y] = q[x]*T_prime[x][y] + q[y]*T_prime[y][x]
	return S
	

def vlp(x,A,nodes,C,EPSILON,L,DELTA):

	T_prime = numpy.zeros(len(nodes))
	R = 1/(EPSILON**2 * C) * ((math.log(L,2)+1)*math.log(1/C) + math.log(1/DELTA))
	Q_L = Generating_Paths(x,R,A,L,nodes)
	for p in Q_L:
		for i in range(1,L):
			u = p[i]
			T_prime[u] += 1/R
	return T_prime

def Generating_Paths(x,R,A,L,nodes):
	N = sum_neighbors(x,A)
	T = 0
	if N > 0:
		T = A/N
	Q_L = []

	# do walk  
	for k in range(int(R)):
		start = numpy.zeros(len(nodes))
		start[x] = 1
		p = numpy.array(start).reshape(-1,1)
		visited = []
		for j in range(1,L+1):
			p = numpy.dot(T,p)
			step = 0
			p_1d = p[:,0]
			if numpy.sum(p_1d) > 0:
				probs = p_1d/sum(p_1d)
				step = numpy.random.choice(range(len(p_1d)),p=probs,replace=False)
			else:
				step = numpy.random.choice(range(len(p_1d)),replace=False)

			visited.append(step)
		Q_L.append(visited)
	return Q_L


def sum_neighbors(x,A):
	neighbors = []
	for index, y in enumerate(A[x]):
		if y > 0:
			neighbors.append(index)
	return sum([A[x][i] for i in neighbors])
