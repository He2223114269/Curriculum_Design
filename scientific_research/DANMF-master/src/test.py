"""
import pandas as pd
from sklearn.metrics import adjusted_rand_score
file = "Email/email-Eu-core"
kind = "csv"
labels_true = pd.read_csv("../input/Email/email-Eu-core-department-labels.csv",header=None)
labels_pred = pd.read_csv("../output/"+file+"membership."+kind,header=None)
labels_true = list(labels_true[1])
labels_pred = list(labels_pred[1])
ARI = adjusted_rand_score(labels_true, labels_pred)
print("ARI: %f"%(ARI))
"""

"""
# 处理数据
import pandas as pd


from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()
A = pd.read_csv("../input/Citeseer/citeseer.content",sep = '\t',header = None)
# A = A[:,1:2]
# A.to_csv("../input/cora/cora_content.csv",header = None,index = None)
print(A.shape)
a = A[3704]
print(a)

# labels = []
# for i in a:
#     if i not in labels:
#         labels.append(i)
# print(labels)

a=le.fit_transform(a)
print(a)
A[3705] = a
print(A.shape)

A.to_csv("../input/Citeseer/citeseer_content.csv",header = None,index = None)
"""

"""
A = pd.read_csv("../input/Citeseer/citeseer.cites",sep = '\t',header = None)
A.to_csv("../input/Citeseer/citeseer_cites.csv",header = None,index = None)
"""

"""import pandas as pd
import numpy as np
# 导入数据：分隔符为空格
raw_data = pd.read_csv('../input/cora/cora.content',sep = '\t',header = None)
num = raw_data.shape[0] # 样本点数2708
# 将论文的编号转[0,2707]
a = list(raw_data.index)
b = list(raw_data[0])
c = zip(b,a)
map = dict(c)
# 将词向量提取为特征,第二行到倒数第二行
features =raw_data.iloc[:,1:-1]
 # 检查特征：共1433个特征，2708个样本点
print(features.shape)
labels = pd.get_dummies(raw_data[1434])
print(labels.head(3))
raw_data_cites = pd.read_csv('../input/cora/cora.cites',sep = '\t',header = None)
# 创建一个规模和邻接矩阵一样大小的矩阵
matrix = np.zeros((num,num))
# 创建邻接矩阵
for i ,j in zip(raw_data_cites[0],raw_data_cites[1]):
    x = map[i] ; y = map[j]  #替换论文编号为[0,2707]
    matrix[x][y] = matrix[y][x] = 1 #有引用关系的样本点之间取1
# 查看邻接矩阵的元素和（按每列汇总）
print(sum(matrix))
"""

"""import numpy as np
import pandas as pd

file = "Citeseer/citeseer_cites"
kind = "csv"
labels_true = pd.read_csv("../input/Citeseer/citeseer_content.csv", header=None)
labels_pred = pd.read_csv("../output/" + file + "membership." + kind, header=None)
labels_true = list(labels_true[3705])
labels_pred = list(labels_pred[1])
labels_pred = labels_pred[0:3312]
print(len(labels_true))
print(len(labels_pred))
a = [1,1]
a[0] = labels_true
a[1] = labels_pred
a = pd.DataFrame(a)
a.to_csv('1.csv')
print(a)
"""

