"""DANMF class."""

import json
import os
import numpy as np
import pandas as pd
from tqdm import tqdm
import networkx as nx
from sklearn.decomposition import NMF
from scipy.optimize import linear_sum_assignment

from sklearn.metrics import normalized_mutual_info_score, adjusted_rand_score
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

class HDANMF(object):
    """
    Deep autoencoder-like non-negative matrix factorization class.
    深度类自动编码器非负矩阵分解类
    """
    def __init__(self, graph, args):
        """
        Initializing a DANMF object.
        :param graph: Networkx graph.
        :param args: Arguments object.
        初始化 DANMF 对象。:param 图：Networkx 图。:param args： Arguments 对象。
        """
        self.graph = graph  # 传入 NetworkX 图
        self.A = nx.adjacency_matrix(self.graph)  # 计算邻接矩阵 A
        self.L = nx.laplacian_matrix(self.graph)  # 计算拉普拉斯矩阵 L
        self.D = self.L + self.A  # 计算度矩阵 D = L + A
        self.args = args  # 解析命令行参数
        self.p = len(self.args.layers)  # 计算 NMF 分解层数
        # self.args.lamb = self.args.lamb+self.args.cigma+self.args.alpha

        # 读取 true_labels 并保存为属性
        self.true_labels = None
        if args.true_labels_path:
            try:
                df = pd.read_csv(args.true_labels_path)
                # 假设你的标签在第一列
                self.true_labels = df.iloc[:, 1].values
            except Exception as e:
                print(f"读取 true labels 失败：{e}")

    def setup_z(self, i):
        """
        Setup target matrix for pre-training process.
        为预训练过程设置目标矩阵。
        """
        if i == 0:
            self.Z = self.A
        else:
            self.Z = self.V_s[i-1]

    def sklearn_pretrain(self, i):
        """
        Pretraining a single layer of the model with sklearn.
        :param i: Layer index.
        使用 sklearn 预训练模型的单个层。:param i：图层索引。
        """
        nmf_model = NMF(n_components=self.args.layers[i],
                        init="random",
                        random_state=self.args.seed,
                        max_iter=self.args.pre_iterations)

        U = nmf_model.fit_transform(self.Z)
        V = nmf_model.components_
        return U, V

    def pre_training(self):
        """
        Pre-training each NMF layer.
        预训练每个 NMF 层。
        """
        print("\nLayer pre-training started. \n")
        self.U_s = []
        self.V_s = []
        for i in tqdm(range(self.p), desc="Layers trained: ", leave=True):
            self.setup_z(i)
            U, V = self.sklearn_pretrain(i)
            self.U_s.append(U)
            self.V_s.append(V)

    def setup_Q(self):
        """
        Setting up Q matrices.
        设置 Q 矩阵。
        """
        self.Q_s = [None for _ in range(self.p+1)]
        self.Q_s[self.p] = np.eye(self.args.layers[self.p-1])
        for i in range(self.p-1, -1, -1):
            self.Q_s[i] = np.dot(self.U_s[i], self.Q_s[i+1])

    def update_U(self, i):
        """
        Updating left hand factors.
        :param i: Layer index.
        更新左手系数。:param i：图层索引。
        """
        if i == 0:
            R = self.U_s[0].dot(self.Q_s[1].dot(self.VpVpT).dot(self.Q_s[1].T))
            R = R+self.A_sq.dot(self.U_s[0].dot(self.Q_s[1].dot(self.Q_s[1].T)))
            Ru = 2*self.A.dot(self.V_s[self.p-1].T.dot(self.Q_s[1].T))
            self.U_s[0] = (self.U_s[0]*Ru)/np.maximum(R, 10**-10)
        else:
            R = self.P.T.dot(self.P).dot(self.U_s[i]).dot(self.Q_s[i+1]).dot(self.VpVpT).dot(self.Q_s[i+1].T)
            R = R+self.A_sq.dot(self.P).T.dot(self.P).dot(self.U_s[i]).dot(self.Q_s[i+1]).dot(self.Q_s[i+1].T)
            Ru = 2*self.A.dot(self.P).T.dot(self.V_s[self.p-1].T).dot(self.Q_s[i+1].T)
            self.U_s[i] = (self.U_s[i]*Ru)/np.maximum(R, 10**-10)

    def update_P(self, i):
        """
        Setting up P matrices.
        :param i: Layer index.
        设置 P 矩阵。:param i：图层索引。
        """
        if i == 0:
            self.P = self.U_s[0]
        else:
            self.P = self.P.dot(self.U_s[i])

    def update_V(self, i):
        """
        Updating right hand factors.
        :param i: Layer index.
        更新右手系数。:param i：图层索引
        """
        if i < self.p-1:
            Vu = 2*self.A.dot(self.P).T
            Vd = self.P.T.dot(self.P).dot(self.V_s[i])+self.V_s[i]
            self.V_s[i] = self.V_s[i] * Vu/np.maximum(Vd, 10**-10)
        else:
            Vu = 2*self.A.dot(self.P).T+(self.args.lamb*self.A.dot(self.V_s[i].T)).T
            Vd = self.P.T.dot(self.P).dot(self.V_s[i])
            Vd = Vd + self.V_s[i]+(self.args.lamb*self.D.dot(self.V_s[i].T)).T
            self.V_s[i] = self.V_s[i] * Vu/np.maximum(Vd, 10**-10)

    def calculate_cost(self, i):
        """
        Calculate loss.
        :param i: Global iteration.
        计算损失。:param i： 全局迭代.
        """
        reconstruction_loss_1 = np.linalg.norm(self.A-self.P.dot(self.V_s[-1]), ord="fro")**2
        reconstruction_loss_2 = np.linalg.norm(self.V_s[-1]-self.A.dot(self.P).T, ord="fro")**2
        regularization_loss = np.trace(self.V_s[-1].dot(self.L.dot(self.V_s[-1].T)))
        self.loss.append([i+1, reconstruction_loss_1, reconstruction_loss_2, regularization_loss])

    def save_embedding(self):
        """
        Save embedding matrix.
        保存嵌入矩阵。
        """
        embedding = [np.array(range(self.P.shape[0])).reshape(-1, 1), self.P, self.V_s[-1].T]
        embedding = np.concatenate(embedding, axis=1)
        columns = ["id"] + ["x_" + str(x) for x in range(self.args.layers[-1]*2)]
        embedding = pd.DataFrame(embedding, columns=columns)
        embedding.to_csv(self.args.output_path, index=None)

    def save_membership(self):
        """
        Save cluster membership predictions to JSON.
        保存聚类成员信息到 JSON 文件。
        """
        membership_path = self.args.membership_path

        # 自动创建目录（如果不存在）
        os.makedirs(os.path.dirname(membership_path), exist_ok=True)

        membership = np.argmax(self.P, axis=1).tolist()
        with open(membership_path, "w") as f:
            json.dump(membership, f)

        print(f"Cluster membership saved to: {membership_path}")

    def training(self):
        """
        Training process after pre-training.
        预训练后的训练过程。
        """
        print("\n\nTraining started. \n")
        self.loss = []
        self.A_sq = self.A.dot(self.A.T)
        for iteration in tqdm(range(self.args.iterations), desc="Training pass: ", leave=True):
            self.setup_Q()
            self.VpVpT = self.V_s[self.p-1].dot(self.V_s[self.p-1].T)
            for i in range(self.p):
                self.update_U(i)
                self.update_P(i)
                self.update_V(i)
            if self.args.calculate_loss:
                self.calculate_cost(iteration)
        self.save_membership()
        self.save_embedding()

    def evaluate_clustering(self):
        """
        Evaluate clustering performance using NMI and ARI.
        Optionally compares with true labels if provided.

        使用 NMI 和 ARI 评估集群性能。（可选）与 true 标签（如果提供）进行比较。
        """
        true_labels = self.true_labels# 从模型内部取，不用手动传
        if true_labels is None:
            print("未提供 True 标签。无法计算外部集群指标。")
            return

        pred_labels = np.argmax(self.P, axis=1)


        # ===== NMI & ARI =====
        nmi = normalized_mutual_info_score(true_labels, pred_labels)
        ari = adjusted_rand_score(true_labels, pred_labels)

        # ===== ACC =====
        acc = self.clustering_accuracy(true_labels, pred_labels)

        print(f"NMI: {nmi:.4f}, ARI: {ari:.4f}, ACC: {acc:.4f}")
        return nmi, ari, acc

    def clustering_accuracy(sel,true_labels, pred_labels):
        """
        计算聚类准确率（ACC），基于匈牙利算法对标签进行最佳匹配。
        """
        true_labels = np.array(true_labels)
        pred_labels = np.array(pred_labels)

        D = max(pred_labels.max(), true_labels.max()) + 1
        confusion_matrix = np.zeros((D, D), dtype=np.int64)

        for i in range(len(true_labels)):
            confusion_matrix[pred_labels[i], true_labels[i]] += 1

        row_ind, col_ind = linear_sum_assignment(-confusion_matrix)  # 最大化匹配
        acc = confusion_matrix[row_ind, col_ind].sum() / len(true_labels)
        return acc

    def visualize_embedding(self, method='tsne'):
        """
        Visualize the embedding using t-SNE or PCA.
        :param method: 'tsne' or 'pca'
        :param labels: Optional true labels for coloring.
        将嵌入向量（即降维后的特征表示）通过 t-SNE 或 PCA 方法降维到二维空间，并以散点图的形式进行可视化，用于展示各个节点/样本在嵌入空间中的分布情况。
        使用 t-SNE 或 PCA 可视化嵌入。:param method： 'tsne' 或 'pca' :param labels： 用于着色的可选 true 标签。
        """
        labels = self.true_labels
        embedding = self.P
        if method == 'tsne':
            reducer = TSNE(n_components=2, random_state=42)
        elif method == 'pca':
            reducer = PCA(n_components=2)
        else:
            raise ValueError("Method must be 'tsne' or 'pca'.")

        reduced = reducer.fit_transform(embedding)
        plt.figure(figsize=(8, 6))
        if labels is not None:
            scatter = plt.scatter(reduced[:, 0], reduced[:, 1], c=labels, cmap='tab10', alpha=0.7)
            plt.legend(*scatter.legend_elements(), title="Classes")
        else:
            plt.scatter(reduced[:, 0], reduced[:, 1], alpha=0.7)
        plt.title(f'{method.upper()} visualization of DANMF embedding')
        plt.xlabel('Dim 1')
        plt.ylabel('Dim 2')
        plt.grid(False)
        plt.show()

    def plot_loss(self):
        """
        Plot loss curves recorded during training.
        绘制训练期间记录的损失曲线
        """
        if not hasattr(self, 'loss') or len(self.loss) == 0:
            print("No loss recorded.")
            return

        loss_array = np.array(self.loss)
        plt.plot(loss_array[:, 0], loss_array[:, 1], label='Recon Loss 1')
        plt.plot(loss_array[:, 0], loss_array[:, 2], label='Recon Loss 2')
        plt.plot(loss_array[:, 0], loss_array[:, 3], label='Reg Loss')
        plt.xlabel("Iteration")
        plt.ylabel("Loss")
        plt.title("Loss during training")
        plt.legend()
        plt.grid(False)
        plt.show()
