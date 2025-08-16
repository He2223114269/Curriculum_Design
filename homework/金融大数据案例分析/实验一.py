import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import warnings
warnings.filterwarnings("ignore")

matplotlib.rcParams['font.family'] = 'SimHei'

data1 = pd.read_csv("688599天合光能.csv", encoding="gbk")

# 提取第一列的时间数据
time_data = data1.iloc[:, 0]

# 提取第十列的迭涨幅数据
column10_data = data1.iloc[:, 9]

# 绘制初始数据的走势图
plt.plot(time_data, column10_data)
plt.xlabel('时间')
plt.ylabel('迭涨幅')
plt.title('初始数据走势图')
plt.show()

# 计算迭涨幅数据的均值和标准差
mean = column10_data.mean()
std = column10_data.std()

# 生成服从正态分布的随机数，并计算未来30日的预期收益率
random_values = np.random.normal(mean, std, size=30)
expected_returns = random_values[0:30]  # 从预测数据中提取30个值

matplotlib.rcParams['axes.unicode_minus'] = False
# 绘制原始数据和预测数据的走势图
plt.plot(time_data, column10_data, color='blue', label='原始数据')
plt.plot(np.arange(len(time_data), len(time_data)+30), expected_returns, color='red', label='预测数据')
plt.xlabel('时间')
plt.ylabel('迭涨幅')
plt.title('原始数据和预测数据')
plt.legend()
plt.show()

# 绘制未来30日的预期收益率柱状图
plt.bar(np.arange(len(time_data), len(time_data) + 30), expected_returns)
plt.xlabel('交易日')
plt.ylabel('预期收益率')
plt.title('未来30日的预期收益率')
plt.show()
