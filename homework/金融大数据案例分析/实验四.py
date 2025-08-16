import pandas as pd
import numpy as np
import statsmodels.api as sm
import scipy.stats as scs
import matplotlib.pyplot as plt

# 导入需要的包
import pandas as pd
import numpy as np
import statsmodels.api as sm # 统计运算
import scipy.stats as scs # 科学计算
import matplotlib.pyplot as plt # 绘图

# 选取几只感兴趣的股票
stock_set = ['000413.XSHE','000063.XSHE','002007.XSHE','000001.XSHE','000002.XSHE']
noa = len(stock_set)
df = get_price(stock_set, start_date='2019-10-31', end_date='2020-10-31', frequency='daily', fields=['close'])
data = df['close']

# 规范化后时序数据
(data / data.ix[0] * 100).plot(figsize=(8, 5))

# 计算不同证券的均值、协方差
returns = np.log(data / data.shift(1))
returns.mean() * 252
returns.cov() * 252

# 给不同资产随机分配初始权重
weights = np.random.random(noa)
weights /= np.sum(weights)
weights

# 计算预期组合年化收益、组合方差和组合标准差
np.sum(returns.mean() * weights) * 252
np.dot(weights.T, np.dot(returns.cov() * 252, weights))
np.sqrt(np.dot(weights.T, np.dot(returns.cov() * 252, weights)))

# 用蒙特卡洛模拟产生大量随机组合
port_returns = []
port_variance = []

for p in range(4000):
    weights = np.random.random(noa)
    weights /= np.sum(weights)
    port_returns.append(np.sum(returns.mean() * 252 * weights))
    port_variance.append(np.sqrt(np.dot(weights.T, np.dot(returns.cov() * 252, weights))))

port_returns = np.array(port_returns)
port_variance = np.array(port_variance)

# 无风险利率设定为4%
risk_free = 0.04

plt.figure(figsize=(8, 4))
plt.scatter(port_variance, port_returns, c=(port_returns - risk_free) / port_variance, marker='o')
plt.grid(True)
plt.xlabel('expected volatility')
plt.ylabel('expected return')
plt.colorbar(label='Sharpe ratio')

# 投资组合优化1——sharpe最大
# 建立statistics函数来记录重要的投资组合统计数据（收益，方差和夏普比）
# 通过对约束最优问题的求解，得到最优解。其中约束是权重总和为1。

def statistics(weights):
    weights = np.array(weights)
    port_returns = np.sum(returns.mean() * weights) * 252
    port_variance = np.sqrt(np.dot(weights.T, np.dot(returns.cov() * 252, weights)))
    return np.array([port_returns, port_variance, port_returns / port_variance])

# 最小化夏普指数的负值
def min_sharpe(weights):
    return -statistics(weights)[2]

# 约束是所有参数(权重)的总和为1
cons = ({'type':'eq', 'fun': lambda x: np.sum(x) - 1})

# 优化函数调用中忽略的唯一输入是起始参数列表(对权重的初始猜测)，我们简单的使用平均分布。
opts = sco.minimize(min_sharpe, noa*[1./noa,], method='SLSQP', bounds=bnds, constraints=cons)
opts

# 得到的最优组合权重向量为：
opts['x'].round(3)

# sharpe最大的组合3个统计数据分别为：预期收益率、预期波动率、最优夏普指数
statistics(opts['x']).round(3)

# 投资组合优化2——方差最小
# 定义一个函数对方差进行最小化
def min_variance(weights):
    return statistics(weights)[1]

optv = sco.minimize(min_variance, noa*[1./noa,],method='SLSQP', bounds=bnds, constraints=cons)
optv

# 方差最小的最优组合权重向量及组合的统计数据分别为：
optv['x'].round(3)

# 得到的预期收益率、波动率和夏普指数
statistics(optv['x']).round(3)

# 组合的有效前沿
# 有效前沿有既定的目标收益率下方差最小的投资组合构成。
# 在最优化时采用两个约束，1.给定目标收益率，2.投资组合权重和为1。
def min_variance(weights):
    return statistics(weights)[1]

# 在不同目标收益率水平循环时，最小化的一个约束条件会变化。
target_returns = np.linspace(0.0, 0.5, 50)
target_variance = []
for tar in target_returns:
    cons = ({'type':'eq','fun': lambda x:statistics(x)[0]-tar},{'type':'eq','fun': lambda x:np.sum(x)-1})
    res = sco.minimize(min_variance, noa*[1./noa,],method='SLSQP', bounds=bnds, constraints=cons)
    target_variance.append(res['fun'])

target_variance = np.array(target_variance)

plt.figure(figsize=(8, 4))
plt.scatter(port_variance, port_returns, c = port_returns / port_variance, marker='o')
plt.scatter(target_variance, target_returns, c = target_returns / target_variance, marker='x')
plt.plot(statistics(opts['x'])[1], statistics(opts['x'])[0], 'r*', markersize=15.0)
plt.plot(statistics(optv['x'])[1], statistics(optv['x'])[0], 'y*', markersize=15.0)
plt.grid(True)
plt.xlabel('expected volatility')
plt.ylabel('expected return')
plt.colorbar(label='Sharpe ratio')