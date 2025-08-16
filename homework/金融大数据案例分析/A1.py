import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

plt.style.use('seaborn')
plt.rcParams['font.family'] = 'SimHei'
plt.rcParams['axes.unicode_minus'] = False

data = pd.read_csv("688262国芯科技.csv", header=0, encoding='gbk')
data = data[['日期', '涨跌额']]
print(data.head())

x = data['日期']
y = data["涨跌额"]

fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(20, 15))

# 绘制初始数据走势图
ax1.plot(x, y)
tick_spacing = 10
ax1.xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))
ax1.set_xticklabels(x, rotation=90)
ax1.set_xlabel('时间')
ax1.set_ylabel('迭涨幅')
ax1.set_title('初始数据走势图')

# 计算迭涨幅数据的均值和标准差
mean = y.mean()
std = y.std()

# 生成服从正态分布的随机数，并计算未来30日的预期收益率
random_values = np.random.normal(mean, std, size=30)
expected_returns = random_values[0:30]  # 从预测数据中提取30个值

# 绘制原始数据和预测数据的走势图
ax2.plot(x, y, color='blue', label='原始数据')
ax2.plot(np.arange(len(x), len(x)+30), expected_returns, color='red', label='预测数据')
ax2.xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))
ax2.set_xticklabels(x, rotation=90)
ax2.set_xlabel('时间')
ax2.set_ylabel('迭涨幅')
ax2.set_title('原始数据和预测数据')
ax2.legend()

# 绘制未来30日的预期收益率柱状图
ax3.bar(np.arange(len(x), len(x) + 30), expected_returns)
ax3.set_xlabel('交易日')
ax3.set_ylabel('预期收益率')
ax3.set_title('未来30日的预期收益率')

plt.subplots_adjust(hspace=0.5)
plt.show()