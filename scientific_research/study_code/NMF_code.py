from sklearn.decomposition import NMF
import numpy as np

# 创建一个测试矩阵
X = np.array([[1, 1, 0], [2, 0, 1], [3, 0, 2], [4, 1, 2]])

# 创建NMF对象，并设置分量数目
n_components = 2
nmf = NMF(n_components=n_components)

# 拟合模型并进行矩阵分解
W = nmf.fit_transform(X)
H = nmf.components_

# 打印结果
print("X矩阵:")
print(X)
print("W矩阵:")
print(W)
print("\nH矩阵:")
print(H)