import networkx as nx
import pandas as pd
import csv


# # Export the edges to a csv file
# with open("edges.csv", "w") as f:
#     writer = csv.writer(f)
#     for edge in g.edges():
#         writer.writerow(edge)
#
## Export the node attributes to a csv file
# with open("nodes.csv", "w") as f:
#     writer = csv.writer(f)
#     writer.writerow(["node", "attribute"])
#     for node, attribute in g.nodes(data=True):
#         writer.writerow([node, attribute])

from karateclub.community_detection.overlapping import DANMF
# 读取csv文件
df = pd.read_csv('Email/email-Eu-core.csv')
g = nx.from_pandas_edgelist(df, 'from', 'to')
model = DANMF()
model.fit(g)
abel = model.get_memberships()
result_dict = {'node_id': list(abel.keys()), 'community_id': list(abel.values())}
df = pd.DataFrame.from_dict(result_dict)
print(df)
label = pd.read_csv('Email/email-Eu-core-department-labels.csv',header=None)
print(label)