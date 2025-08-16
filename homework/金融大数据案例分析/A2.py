# 导入库
import pandas as pd
import mplfinance as mpf
import matplotlib.pyplot as plt
import matplotlib as mpl       # 用于设置图形参数
from cycler import cycler      # 用于定制线条颜色

# 忽略警告
import warnings
warnings.filterwarnings('ignore')

mpl.rcParams['font.sans-serif'] = ['SimHei']  # 指定默认字体
mpl.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题


# 导入股票数据
sbux = pd.read_csv("实验二数据.csv", index_col=0, encoding="GBK")
sbux.index = pd.to_datetime(sbux.index, format='%Y-%m-%d')
# print(sbux.head())

'''绘制图形的类型，有candle, renko, ohlc, line等；K线图为candle
mav(moving average):均线类型,此处设置5,20,60日线
volume:布尔类型，设置是否显示成交量，默认False
title:设置标题   y_label:设置纵轴主标题
figratio:设置图形纵横比
figscale:设置图形尺寸(数值越大图像质量越高)'''
kwargs = dict(type='candle', mav=(5, 20, 60), volume=True, ylabel='Candles', figratio=(12, 9), figscale=4)


'''设置K线线柱颜色，up意为收盘价大于等于开盘价,down:与up相反，这样设置与国内K线颜色标准相符
edge:K线线柱边缘颜色(i代表继承自up和down的颜色)，下同。详见官方文档)
wick:灯芯(上下影线)颜色
volume:成交量直方图的颜色'''
mc = mpf.make_marketcolors(up='red', down='green', edge='i', wick='i', volume='in')

'''设置图形风格
gridaxis:设置网格线位置
gridstyle:设置网格线线型
y_on_right:设置y轴位置是否在右'''
s = mpf.make_mpf_style(gridaxis='both', gridstyle='-.', y_on_right=False, marketcolors=mc)

'''设置均线颜色，配色图
建议设置较深的颜色且与红色、绿色形成对比
此处设置七条均线的颜色，也可应用默认设置'''
mpl.rcParams['axes.prop_cycle'] = cycler(color=['dodgerblue', 'deeppink','navy', 'teal', 'maroon', 'darkorange', 'indigo'])

# # 设置线宽
mpl.rcParams['lines.linewidth'] = 1.5

# 图形绘制
# show_nontrading:是否显示非交易日，默认False
mpf.plot(sbux, **kwargs, style=s, show_nontrading=False,)
plt.show()


# 简单图
import pyecharts.options as opts
from pyecharts.charts import Candlestick
sbux = pd.read_csv("实验二数据.csv", index_col=0)


# 数据准备
new_Sbux = sbux.iloc[::20]
x_data = new_Sbux.index.tolist()
y_data = new_Sbux[["Open", "Close", "Low", "High"]].values.tolist()

kline = (
    Candlestick(init_opts=opts.InitOpts(width="600px", height="400px"))
        .add_xaxis(xaxis_data=x_data)
        .add_yaxis(series_name="", y_axis=y_data)
        .set_series_opts()
        .set_global_opts(
        yaxis_opts=opts.AxisOpts(
            splitline_opts=opts.SplitLineOpts(
                is_show=True, linestyle_opts=opts.LineStyleOpts(width=1)
            )
        )
    )

)
kline.render_notebook()


import numpy as np
# 移动平均线
data_close = sbux['Close']
ma20 = np.round(data_close.rolling(window=20, center=True).mean(), 2)
ma5 = np.round(data_close.rolling(window=5, center=True).mean(), 2)
fig, ax = plt.subplots()
ax.plot(ma5, linestyle='-', lw=2)
ax.plot(ma20, linestyle='--', lw=2)
plt.legend(["MA5", "MA20"])
plt.show()

# 决策
diff = ma5-ma20
signal = np.sign(diff-diff.shift(1))
buy = pd.DataFrame({"price": data_close.loc[signal.values == 1], "operation": "Buy"})
sell = pd.DataFrame({"price": data_close.loc[signal.values == -1], "operation": "Sell"})
trade = pd.concat([buy, sell])
trade.sort_index(inplace=True)
print(trade.head())


sbux["ma5"] = sbux['Close'].rolling(window=5, center=True).mean()
sbux["ma20"] = sbux['Close'].rolling(window=20, center=True).mean()

sbux['Close'] = sbux['Close'].astype('float')

sbux['position'] = np.where(sbux["ma5"] > sbux["ma20"], 1, -1)


# 计算对数化后的基准投资收益率
sbux['returns'] = np.log(sbux['Close'] / sbux['Close'].shift(1))

# 通过将前一期的头寸position和当期的对数化收益率，得到的是交易策略当期的收益
sbux['strategy'] = sbux['position'].shift(1) * sbux['returns']

# 计算加总的基准和策略对数收益率，通过指数函数算出绝对收益
print(np.exp(sbux[['returns', 'strategy']].sum()))

fig, ax = plt.subplots()
ax.plot(sbux['returns'], linestyle='-')
ax.plot(sbux['strategy'], linestyle='--')
plt.legend(["returns", "strategy"])
plt.show()


