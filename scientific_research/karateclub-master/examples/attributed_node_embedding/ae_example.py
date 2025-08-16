"""AE Example."""

import random
import numpy as np
import networkx as nx
from scipy.sparse import coo_matrix
from karateclub.node_embedding.attributed import AE

g = nx.newman_watts_strogatz_graph(50, 10, 0.2)

X = {i: random.sample(range(150),50) for i in range(50)}

row = np.array([k for k, v in X.items() for val in v])
col = np.array([val for k, v in X.items() for val in v])
data = np.ones(50*50)
shape = (50, 150)

X = coo_matrix((data, (row, col)), shape=shape)

model = AE()

model.fit(g, X)

a = model.get_embedding()
# print(a)

#使用liuvain算法

from community import community_louvain

# 使用Louvain算法自动发现社区
partition = community_louvain.best_partition(g)

# 输出社区划分结果
for i in set(partition.values()):
    nodes = [j for j in partition.keys() if partition[j] == i]
    print(f'Community {i}: {nodes}')



#使用谱聚类算法
"""from sklearn.cluster import SpectralClustering
# 获取邻接矩阵
adj_matrix = nx.adjacency_matrix(g)

# 执行谱聚类
model = SpectralClustering(n_clusters=2, affinity='precomputed', n_init=100)
labels = model.fit_predict(adj_matrix)

# 输出聚类结果
for i, label in enumerate(labels):
    print(f"Node {i} is in cluster {label}")"""

# import community
# # Get node embeddings
# embeddings = model.get_embedding()
#
# # Convert embeddings to dictionary format
# emb_dict = {}
# for i, emb in enumerate(embeddings):
#     emb_dict[i] = emb.tolist()
#
# # Perform Louvain community detection on node embeddings
# partition = community.best_partition(emb_dict)
#
# # Print out community assignments
# for node, community_id in partition.items():
#     print(f"Node {node} belongs to community {community_id}")