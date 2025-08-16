import matplotlib.pyplot as plt
import numpy as np

# 参数范围
param_range = [10, 1, 0.1, 0.01, 0.001]

# 五个数据集的名称
datasets = ['Email', 'PubMed', 'Cora', 'Citeseer', 'Wiki']

# 假设你的效果指标是 NMI，这里放上示例数据，你需要把它们替换为自己的实验数据
# shape: (len(datasets), len(param_range))
lambda_results = [
    [0.55, 0.60, 0.65, 0.75, 0.70],  # Email
    [0.45, 0.50, 0.55, 0.68, 0.65],  # Cora
    [0.52, 0.58, 0.62, 0.73, 0.71],  # Citeseer
    [0.48, 0.53, 0.59, 0.70, 0.68],  # PubMed
    [0.50, 0.55, 0.60, 0.72, 0.69],  # BlogCatalog
]

alpha_results = [
    [0.50, 0.60, 0.75, 0.70, 0.68],
    [0.45, 0.53, 0.70, 0.65, 0.62],
    [0.48, 0.58, 0.74, 0.68, 0.66],
    [0.46, 0.54, 0.72, 0.67, 0.63],
    [0.49, 0.57, 0.73, 0.69, 0.65],
]

sigma_results = [
    [0.48, 0.58, 0.70, 0.75, 0.72],
    [0.42, 0.52, 0.65, 0.70, 0.68],
    [0.45, 0.55, 0.68, 0.73, 0.70],
    [0.44, 0.53, 0.67, 0.72, 0.69],
    [0.47, 0.56, 0.69, 0.74, 0.71],
]

# 画图函数
def plot_param_curve(param_name, results):
    plt.figure(figsize=(10, 6))
    for idx, dataset in enumerate(datasets):
        plt.plot(param_range, results[idx], marker='o', label=dataset)
    plt.xscale('log')
    plt.xlabel(f'{param_name} value (log scale)')
    plt.ylabel('NMI')
    plt.title(f'Effect of {param_name} on Model Performance')
    plt.legend()
    plt.grid(True)
    plt.show()

# 绘制 lambda 图
plot_param_curve('Lambda', lambda_results)

# 绘制 alpha 图
plot_param_curve('Alpha', alpha_results)

# 绘制 sigma 图
plot_param_curve('Sigma', sigma_results)
