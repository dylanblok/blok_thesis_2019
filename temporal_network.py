import networkx as nx
import pandas as pd
from datetime import date, timedelta
import monthdelta as md

# global vars
MIN_DATE = date(2014,1,1)
MAX_DATE = date(2017,3,1)
# TIME_DELTA = timedelta(years = 3, weeks = 8)
TIME_DELTA_STRING = "months"

path = "soc-redditHyperlinks-title.tsv"
fields = ["SOURCE_SUBREDDIT","TARGET_SUBREDDIT","TIMESTAMP"]
data = pd.read_csv(path, sep="\t",usecols=fields)

print(len(data))
d_5 = []
d_10 = []
d_20 = []
d_25 = []
d_50 = []
d_100 = []
d_200 = []
d_500 = []
d_1000 = []
d_2500 = []
d_5000 = []
d_7500 = []
d_10000 = []
d_15000 = []
d_20000 = []
source_count = data["SOURCE_SUBREDDIT"].value_counts()
target_count = data["TARGET_SUBREDDIT"].value_counts()
for index, row in data.iterrows():
	if not (source_count[row["SOURCE_SUBREDDIT"]] > 5 and target_count[row["TARGET_SUBREDDIT"]] > 5):
		d_5.append(index)
	if not (source_count[row["SOURCE_SUBREDDIT"]] > 10 and target_count[row["TARGET_SUBREDDIT"]] > 10):
		d_10.append(index)
	if not (source_count[row["SOURCE_SUBREDDIT"]] > 20 and target_count[row["TARGET_SUBREDDIT"]] > 20):
		d_20.append(index)
	if not (source_count[row["SOURCE_SUBREDDIT"]] > 25 and target_count[row["TARGET_SUBREDDIT"]] > 25):
		d_25.append(index)
	if not (source_count[row["SOURCE_SUBREDDIT"]] > 50 and target_count[row["TARGET_SUBREDDIT"]] > 50):
		d_50.append(index)
	if not (source_count[row["SOURCE_SUBREDDIT"]] > 100 and target_count[row["TARGET_SUBREDDIT"]] > 100):
		d_100.append(index)
	if not (source_count[row["SOURCE_SUBREDDIT"]] > 200 and target_count[row["TARGET_SUBREDDIT"]] > 200):
		d_200.append(index)
	if not (source_count[row["SOURCE_SUBREDDIT"]] > 500 and target_count[row["TARGET_SUBREDDIT"]] > 500):
		d_500.append(index)
	if not (source_count[row["SOURCE_SUBREDDIT"]] > 1000 and target_count[row["TARGET_SUBREDDIT"]] > 1000):
		d_1000.append(index)
	if not (source_count[row["SOURCE_SUBREDDIT"]] > 2500 and target_count[row["TARGET_SUBREDDIT"]] > 2500):
		d_2500.append(index)
	if not (source_count[row["SOURCE_SUBREDDIT"]] > 5000 and target_count[row["TARGET_SUBREDDIT"]] > 5000):
		d_5000.append(index)
	if not (source_count[row["SOURCE_SUBREDDIT"]] > 7500 and target_count[row["TARGET_SUBREDDIT"]] > 7500):
		d_7500.append(index)
	if not (source_count[row["SOURCE_SUBREDDIT"]] > 10000 and target_count[row["TARGET_SUBREDDIT"]] > 10000):
		d_10000.append(index)
	if not (source_count[row["SOURCE_SUBREDDIT"]] > 15000 and target_count[row["TARGET_SUBREDDIT"]] > 15000):
		d_15000.append(index)
	if not (source_count[row["SOURCE_SUBREDDIT"]] > 20000 and target_count[row["TARGET_SUBREDDIT"]] > 20000):
		d_20000.append(index)
	
	print(index,"/",len(data), end="\r")

deleted = [d_5,d_10,d_20,d_25,d_50,d_100,d_200,d_500,d_1000,d_2500,d_5000,d_7500,d_10000,d_15000,d_20000]
file_names = ["5","10","20","25","50","100","200","500","1000","2500","5000","7500","10000","15000","20000"]
for d in zip(deleted,file_names):
	reduced_data = data.drop(d[0])
	print(d[1],len(reduced_data),len(reduced_data["SOURCE_SUBREDDIT"].value_counts()),len(reduced_data["TARGET_SUBREDDIT"].value_counts()),sep="\t")
	reduced_data.to_csv(index=False,path_or_buf="tsvs/and/" + d[1] + ".tsv",sep="\t")
print()
# print(len(data))

# data.to_csv(index=False,path_or_buf="500.tsv",sep="\t")

# graphs = {}
# adj_matrices = {}
# currentDate = MIN_DATE
# # while(currentDate < MAX_DATE):
# # sub_data = data[(data['TIMESTAMP'] >= currentDate.isoformat()) & (data['TIMESTAMP'] < (currentDate+TIME_DELTA).isoformat())]

# # create subgraph
# G = nx.DiGraph()
# for index, row in data.iterrows():
# 	print(index,'/',len(data), end = "\r")
# 	G.add_edge(row['SOURCE_SUBREDDIT'],row['TARGET_SUBREDDIT'],t=row['TIMESTAMP'])

# # graphs[currentDate] = G

# # filename = "graphs/" + TIME_DELTA_STRING + "/" + currentDate.isoformat() + ".gexf"
# # filename = "graphs/bigboy.gexf"
# # nx.readwrite.gexf.write_gexf(G,filename)
# # currentDate += TIME_DELTA

# for g in graphs:
# 	print(g,'\t',max([nx.degree(graphs[g],n) for n in nx.nodes(graphs[g])]))

# nx.readwrite.gexf.write_gexf(G,"tn_test.gexf")
