# -*- coding: utf-8 -*-
import pandas as pd
import matplotlib.pyplot as plt
import tushare as ts
from pyecharts.charts import Line, Scatter
from pyecharts import options as opts

pd.set_option('expand_frame_repr', False)  # 当列太多时不换行
plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示中文标签
plt.rcParams['axes.unicode_minus'] = False


# 获取北向资金数据
def get_north_money(start, end):
    # 获取交易日历
    dates = get_cal_date(start, end)
    # tushare限制流量，每次只能获取300条记录
    df = pro.moneyflow_hsgt(start_date=start, end_date=end)
    # 拆分时间进行拼接，再删除重复项
    for i in range(0, len(dates) - 300, 300):
        d0 = pro.moneyflow_hsgt(start_date=dates[i], end_date=dates[i + 300])
        df = pd.concat([d0, df])
        # 删除重复项
        df = df.drop_duplicates()
        df.index = pd.to_datetime(df.trade_date)
        df = df.sort_index()
    return df


# 获取交易日历
def get_cal_date(start, end):
    cal_date = pro.trade_cal(exchange='', start_date=start, end_date=end)
    cal_date = cal_date[cal_date.is_open == 1]
    dates = cal_date.cal_date.values
    return dates


# 获取指数数据
def get_index_data(code, start, end):
    index_df = pro.index_daily(ts_code=code, start_date=start, end_date=end)
    index_df.index = pd.to_datetime(index_df.trade_date)
    index_df = index_df.sort_index()
    return index_df


# 获取北向资金与沪深300收益率的滚动窗口相关系数
def cal_rol_cor(data, period=30):
    cors = data.rolling(period).corr()
    cors = cors.dropna().iloc[1::2, 0]
    cors = cors.reset_index()
    cors = cors.set_index('trade_date')
    return cors['沪深300']


def North_Strategy(data, window, stdev_n, cost):
    '''输入参数：
    data:包含北向资金和指数价格数据
    window:移动窗口
    stdev_n:几倍标准差
    cost:手续费
    '''
    # 中轨
    df = data.copy().dropna()
    df['mid'] = df['北向资金'].rolling(window).mean()
    stdev = df['北向资金'].rolling(window).std()
    # 上下轨
    df['upper'] = df['mid'] + stdev_n * stdev
    df['lower'] = df['mid'] - stdev_n * stdev
    df['ret'] = df.close / df.close.shift(1) - 1
    df.dropna(inplace=True)

    # 设计买卖信号
    # 当日北向资金突破上轨线发出买入信号设置为1
    df.loc[df['北向资金'] > df.upper, 'signal'] = 1
    # 当日北向资金跌破下轨线发出卖出信号设置为0
    df.loc[df['北向资金'] < df.lower, 'signal'] = 0
    df['position'] = df['signal'].shift(1)
    df['position'].fillna(method='ffill', inplace=True)
    df['position'].fillna(0, inplace=True)
    # 根据交易信号和仓位计算策略的每日收益率
    df.loc[df.index[0], 'capital_ret'] = 0
    # 今天开盘新买入的position在今天的涨幅(扣除手续费)
    df.loc[df['position'] > df['position'].shift(1), 'capital_ret'] = \
        (df.close / df.open - 1) * (1 - cost)
    # 卖出同理
    df.loc[df['position'] < df['position'].shift(1), 'capital_ret'] = \
        (df.open / df.close.shift(1) - 1) * (1 - cost)
    # 当仓位不变时,当天的capital是当天的change * position
    df.loc[df['position'] == df['position'].shift(1), 'capital_ret'] = \
        df['ret'] * df['position']
    # 计算标的、策略、指数的累计收益率
    df['策略净值'] = (df.capital_ret + 1.0).cumprod()
    df['指数净值'] = (df.ret + 1.0).cumprod()
    return df


token = '5c07c5fb27eebb27211a43c64f754c56e013f80f381b54e3c3e73f0f'
pro = ts.pro_api(token)

# 获取指数数据
# 常用大盘指数
indexs = {'上证综指': '000001.SH', '深证成指': '399001.SZ', '沪深300': '000300.SH',
          '创业板指': '399006.SZ', '上证50': '000016.SH', '中证500': '000905.SH',
          '中小板指': '399005.SZ', '上证180': '000010.SH'}
start = '20131117'
end = '20201030'
code = '000300.SH'

index_data = pd.DataFrame()
index_data['close'] = get_index_data(code, start, end)['close']
index_data['open'] = get_index_data(code, start, end)['open']
north_data = get_north_money(start, end)  # 2014-11-17之前的获取不到，不知是有还是没有
all_data = index_data.join(north_data['north_money'], how='inner')
all_data.rename(columns={'north_money': '北向资金'}, inplace=True)
all_data.dropna(inplace=True)
print(all_data)
all_data = North_Strategy(all_data, 250, 1.5, 0.0008)
print(all_data)
line = Line()
line.add_xaxis(all_data.index.to_list())
# 每个y轴
line.add_yaxis('my_stra', all_data['策略净值'].round(5).to_list())
line.add_yaxis('hs300', all_data['指数净值'].round(5).to_list())
# 图表配置
line.set_global_opts(
                     title_opts=opts.TitleOpts(title='向北策略--沪深300与北向资金250日\n 2014-2020'),
                     tooltip_opts=opts.TooltipOpts(trigger='axis', axis_pointer_type='cross')
                     )
line.render('向北策略--沪深300与北向资金250日.html')