import matplotlib.pyplot as plt

# 模拟的训练时间数据（单位：秒）
training_times = {
    'Email': 120.5,
    'wiki': 480.3,
    'Cora': 340.9,
    'Citeseer': 640.7,
    'Pubmed': 1750.2

}

# 输出模拟值
print("\n=== Training Time Summary ===")
for dataset, t in training_times.items():
    print(f"{dataset}: {t:.2f} seconds")

# 绘制柱状图
datasets = list(training_times.keys())
times = [training_times[d] for d in datasets]

plt.figure(figsize=(8, 5))
plt.bar(datasets, times, color='skyblue')
plt.ylabel('Training Time (seconds)')
plt.title('Model Training Time on Different Datasets')
plt.show()
