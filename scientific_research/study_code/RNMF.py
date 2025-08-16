import numpy as np

def rnmtf(X, rank, max_iter=100, tol=1e-4):
    # 随机初始化矩阵 W 和 H
    n, m = X.shape
    W = np.random.rand(n, rank)
    H = np.random.rand(rank, m)

    it = 0
    prev_loss = np.inf
    while it < max_iter:
        # 更新 W 矩阵
        WH = W @ H
        W = W * ((X / WH) @ H.T)

        # 更新 H 矩阵
        WH = W @ H
        H = H * (W.T @ (X / WH))

        # 计算损失函数
        loss = np.linalg.norm(X - WH, 'fro')

        # 判断收敛
        if np.abs(prev_loss - loss) < tol:
            break

        prev_loss = loss
        it += 1

    return W, H

# 创建一个测试矩阵
X = np.array([[1, 1, 0],
              [2, 0, 1],
              [3, 0, 2],
              [4, 1, 2]])

# 进行 RNMF 分解
rank = 2
W, H = rnmtf(X, rank)

# 打印结果
print("X矩阵:")
print(X)
print("W矩阵:")
print(W)
print("\nH矩阵:")
print(H)