# �����
import pandas as pd
import mplfinance as mpf
import matplotlib.pyplot as plt
import matplotlib as mpl       # ��������ͼ�β���
from cycler import cycler      # ���ڶ���������ɫ

# ���Ծ���
import warnings
warnings.filterwarnings('ignore')

mpl.rcParams['font.sans-serif'] = ['SimHei']  # ָ��Ĭ������
mpl.rcParams['axes.unicode_minus'] = False  # �������ͼ���Ǹ���'-'��ʾΪ���������


# �����Ʊ����
sbux = pd.read_csv("ʵ�������.csv", index_col=0, encoding="GBK")
sbux.index = pd.to_datetime(sbux.index, format='%Y-%m-%d')
# print(sbux.head())

'''����ͼ�ε����ͣ���candle, renko, ohlc, line�ȣ�K��ͼΪcandle
mav(moving average):��������,�˴�����5,20,60����
volume:�������ͣ������Ƿ���ʾ�ɽ�����Ĭ��False
title:���ñ���   y_label:��������������
figratio:����ͼ���ݺ��
figscale:����ͼ�γߴ�(��ֵԽ��ͼ������Խ��)'''
kwargs = dict(type='candle', mav=(5, 20, 60), volume=True, ylabel='Candles', figratio=(12, 9), figscale=4)


'''����K��������ɫ��up��Ϊ���̼۴��ڵ��ڿ��̼�,down:��up�෴���������������K����ɫ��׼���
edge:K��������Ե��ɫ(i����̳���up��down����ɫ)����ͬ������ٷ��ĵ�)
wick:��о(����Ӱ��)��ɫ
volume:�ɽ���ֱ��ͼ����ɫ'''
mc = mpf.make_marketcolors(up='red', down='green', edge='i', wick='i', volume='in')

'''����ͼ�η��
gridaxis:����������λ��
gridstyle:��������������
y_on_right:����y��λ���Ƿ�����'''
s = mpf.make_mpf_style(gridaxis='both', gridstyle='-.', y_on_right=False, marketcolors=mc)

'''���þ�����ɫ����ɫͼ
�������ý������ɫ�����ɫ����ɫ�γɶԱ�
�˴������������ߵ���ɫ��Ҳ��Ӧ��Ĭ������'''
mpl.rcParams['axes.prop_cycle'] = cycler(color=['dodgerblue', 'deeppink','navy', 'teal', 'maroon', 'darkorange', 'indigo'])

# # �����߿�
mpl.rcParams['lines.linewidth'] = 1.5

# ͼ�λ���
# show_nontrading:�Ƿ���ʾ�ǽ����գ�Ĭ��False
mpf.plot(sbux, **kwargs, style=s, show_nontrading=False,)
plt.show()


# ��ͼ
import pyecharts.options as opts
from pyecharts.charts import Candlestick
sbux = pd.read_csv("ʵ�������.csv", index_col=0)


# ����׼��
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
# �ƶ�ƽ����
data_close = sbux['Close']
ma20 = np.round(data_close.rolling(window=20, center=True).mean(), 2)
ma5 = np.round(data_close.rolling(window=5, center=True).mean(), 2)
fig, ax = plt.subplots()
ax.plot(ma5, linestyle='-', lw=2)
ax.plot(ma20, linestyle='--', lw=2)
plt.legend(["MA5", "MA20"])
plt.show()

# ����
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


# �����������Ļ�׼Ͷ��������
sbux['returns'] = np.log(sbux['Close'] / sbux['Close'].shift(1))

# ͨ����ǰһ�ڵ�ͷ��position�͵��ڵĶ����������ʣ��õ����ǽ��ײ��Ե��ڵ�����
sbux['strategy'] = sbux['position'].shift(1) * sbux['returns']

# ������ܵĻ�׼�Ͳ��Զ��������ʣ�ͨ��ָ�����������������
print(np.exp(sbux[['returns', 'strategy']].sum()))

fig, ax = plt.subplots()
ax.plot(sbux['returns'], linestyle='-')
ax.plot(sbux['strategy'], linestyle='--')
plt.legend(["returns", "strategy"])
plt.show()


