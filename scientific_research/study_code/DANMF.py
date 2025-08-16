import numpy as np
from scipy.sparse import diags


def danmf(X, A, rank, max_iter=100, alpha=0.1, beta=0.1, tol=1e-4):
    # 初始化矩阵 U 和 V
    n, _ = X.shape
    U = np.random.rand(n, rank)
    V = np.random.rand(rank, n)

    # 计算对角矩阵 D
    D = diags(np.squeeze(np.asarray(A.sum(axis=1))), 0, shape=(n, n))

    it = 0
    prev_loss = np.inf
    while it < max_iter:
        # 更新 U 矩阵
        inv_D_U = np.linalg.pinv(D) @ U
        update_U = ((X @ V.T) + (alpha * A @ inv_D_U)) / ((U @ V @ V.T) + (alpha * U @ A @ inv_D_U) + beta * U)
        U = U * np.sqrt(update_U)

        # 更新 V 矩阵
        inv_D_V = np.linalg.pinv(D) @ V
        update_V = (U.T @ X) / (U.T @ U @ V + beta * V @ inv_D_V)
        V = V * np.sqrt(update_V)

        # 计算损失函数
        loss = np.linalg.norm(X - U @ V, 'fro')

        # 判断收敛
        if np.abs(prev_loss - loss) < tol:
            break

        prev_loss = loss
        it += 1

    return U, V


# 创建一个测试矩阵 X 和邻接矩阵 A
X = np.array([[1, 1, 0],
              [2, 0, 1],
              [3, 0, 2],
              [4, 1, 2]])

A = np.array([[0, 1, 0, 1],
              [1, 0, 1, 0],
              [0, 1, 0, 0],
              [1, 0, 0, 0]])

# 进行 DANMF 分解
rank = 2
U, V = danmf(X, A, rank)

# 打印结果
print("U 矩阵:")
print(U)
print("\nV 矩阵:")
print(V)