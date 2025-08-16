from nimfa import Nmf
import numpy as np

# 创建一个测试矩阵
X = np.array([[1, 1, 0],
              [2, 0, 1],
              [3, 0, 2],
              [4, 1, 2]])

# 创建 DNMF 对象，并设置参数
rank = 2
dnmf = Nmf(X, rank=rank, update='divergence', objective='div')

# 进行 DNMF 分解
fit = dnmf()

# 获取分解后的矩阵
W = fit.basis()
H = fit.coef()

# 打印结果
print("X矩阵:")
print(X)
print("W矩阵:")
print(W)
print("\nH矩阵:")
print(H)