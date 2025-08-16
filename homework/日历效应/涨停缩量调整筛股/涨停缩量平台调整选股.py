# -*- coding: utf-8 -*-
import pandas as pd
import matplotlib.pyplot as plt
import tushare as ts
from pyecharts.charts import Line, Scatter
from pyecharts import options as opts
import re

pd.set_option('expand_frame_repr', False)  # 当列太多时不换行
plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示中文标签
plt.rcParams['axes.unicode_minus'] = False

# 获取正常上市的所有股票代码
def get_allstock_code(exchange='', list_status='L', fields='ts_code'):
    data = pro.stock_basic(exchange=exchange, list_status=list_status, fields=fields)
    return data


# 获取股票数据
def get_stock_data(code, start, end):
    stock_df = pro.daily(ts_code=code, start_date=start, end_date=end)
    stock_df.index = pd.to_datetime(stock_df.trade_date)
    stock_df = stock_df.sort_index()
    return stock_df



token = 'dba4bda45f22ecbbd8acc69715e3bf2b0878bc989ba920f829440ec8'
pro = ts.pro_api(token)

# start = '20201122'
# end = '20210201'
# code = '603712.SH'
fee_rate = 0.0003
tax_rate = 0.001

df_code = get_allstock_code(exchange='', list_status='L', fields='ts_code, name')
# 不玩创业板和科创板
df_code = df_code[df_code.ts_code.str.startswith(('60', '00'))]
chose_df = pd.DataFrame()
# # 计算均线的周期尽量多
start = '20201022'
end = '20210201'
aga_code = []
for code in df_code.ts_code:
    df = get_stock_data(code, start, end)
    df = df[['ts_code', 'open', 'close', 'pct_chg', 'vol']]
    if len(df) > 60:
        df['30ma'] = df['close'].rolling(30).mean()
        df['60ma'] = df['close'].rolling(60).mean()
        df.dropna(inplace=True)
        print(code)
        date_list = list(df.index)
        df1 = pd.DataFrame()
        for date in date_list[:-10]:
            location = date_list.index(date)
            next_date = date_list[location + 9]
            if df.loc[date, 'pct_chg'] > 9.94:
                open = df.loc[date, 'open']
                close = df.loc[date, 'close']
                vol = df.loc[date, 'vol']
                ma_30 = df.loc[next_date, '30ma']
                ma_60 = df.loc[next_date, '60ma']
                df1 = df[date:next_date]
                max_close = df1.close.max()
                min_close = df1.close.min()
                # avg_close = df1.close.mean()
                max_vol = df1.vol.max()
                min_vol = df1.vol.min()
                if max_close < close * 1.10 and min_close > open*1.03 \
                   and max_vol < vol * 1.5 and min_close > ma_60 \
                   and min_close*1.02 > ma_30 > ma_60:
                    stock_code = df.loc[date, 'ts_code']
                    aga_code.append(stock_code)
print(aga_code)