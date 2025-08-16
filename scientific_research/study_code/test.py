import numpy as np

# 设置参数和数据
X = np.random.rand(100, 100)  # 输入矩阵 X，大小为 100x100
n_layers = 2  # 层数
n_components = 10  # 每层的因子数量
Q = [np.random.random((n_components,))[:, np.newaxis] * np.identity(n_components) / np.linalg.norm(np.random.random((n_components,))) for _ in range(n_layers)]# Q 矩阵
H = [np.diag(1 / np.linalg.norm(np.random.uniform(0, 1, (n_components,)))) for _ in range(n_layers)]  # H矩阵 # H矩阵  # H矩阵  # H 矩阵
L = np.random.rand(n_components, n_components)  # L 矩阵
lambd = 0.1  # 正则化参数
n_iter = 100  # 迭代次数

# 定义非负双奇异值分解 (NNDSVD)函数
def nndsvd_init(X, n_components):
    U, S, V = np.linalg.svd(X)
    U, V = U[:, :n_components], V[:n_components, :]
    U[U < 0] = 0
    V[V < 0] = 0
    return U, V

# 预训练函数
def nmf_pretraining(X, n_layers, n_components):
    U = []
    V = []
    W = X.copy()
    for i in range(n_layers):
        Ui, Vi = nndsvd_init(W, n_components)
        U.append(Ui)
        V.append(Vi)
        W = np.dot(Ui, Vi)
        W[W < 0] = 0
    return U, V

# 微调函数
def nmf_finetuning(X, U, V, Q, H, L, lambd, n_iter):
    n_layers = len(U)
    n_components = U[0].shape[1]
    W = X.copy()
    for _ in range(n_iter):
        for i in range(n_layers):
            Ui = U[i]
            Vi = V[i]
            Qi = Q[i]
            Hi = H[i]
            Ui_new = np.dot(np.dot(W, Vi.T), np.dot(Vi, Qi))
            Ui_new[Ui_new < 0] = 0
            Vi_new = np.dot(np.dot(np.dot(W.T, Ui.T), Hi), np.dot(Hi, Vi))
            Vi_new[Vi_new < 0] = 0
            U[i] = Ui_new
            V[i] = Vi_new
        W = X.copy()
        for i in range(n_layers):
            W = np.dot(U[i], V[i])
            W[W < 0] = 0
    return U, V

# 预训练
U, V = nmf_pretraining(X, n_layers, n_components)

# 微调
U, V = nmf_finetuning(X, U, V, Q, H, L, lambd, n_iter)

# 打印结果
print("预训练结果：")
for i in range(n_layers):
    print(f"U{i+1}:\n{U[i]}")
    print(f"V{i+1}:\n{V[i]}")
    print()