# -*- coding: utf-8 -*-
import pandas as pd
import matplotlib.pyplot as plt
import tushare as ts
import datetime
from pyecharts.charts import Line
from pyecharts import options as opts

pd.set_option('expand_frame_repr', False)  # 当列太多时不换行
plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示中文标签
plt.rcParams['axes.unicode_minus'] = False


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

# 计算高低开数据
def get_high_low(code, start, end):
    df = get_index_data(code, start, end)
    df['high_low'] = (df['open'] / df['pre_close']) - 1
    return df

# 计算牛熊市数据
def judge_bull_bear(code, start, end, rollings=20, typ='up'):
    df = get_index_data(index, start, end)
    if typ == 'up':
        df.loc[(df['close'] > df['close'].rolling(rollings, min_periods=1).mean()), typ] = True
    elif typ == 'down':
        df.loc[(df['close'] < df['close'].rolling(rollings, min_periods=1).mean()), typ] = True
    else:
        print("请输入up或者down,其他输入不合法")
    df[typ].fillna(value=False, inplace=True)
    return df

# 编写策略
def weekly_value_cal(code, start, end, rollings=20,fee_rate=0.0003, tax_rate=0.001):
    value_df = pd.DataFrame()
    indexs_data = judge_bull_bear(index, start, end, rollings=rollings, typ='up')
    value_df['benchmark'] = indexs_data['close']
    date_list = list(value_df.index)
    if date_list[0].weekday() == 3:
        value_df = value_df.drop(value_df.index[0])
    date_list = list(value_df.index)
    value_list = [(1 - fee_rate) * indexs_data.loc[date_list[0], 'close']]
    for date in date_list[1:]:
        weekday = date.weekday()
        location = date_list.index(date)
        last_date = date_list[location - 1]
        # 牛市的操作：周五开盘买入，周一收盘卖，也可以添加个 （周三开盘买，周四开盘卖）
        if indexs_data.loc[last_date, 'up']:
            if weekday == 4:
                value = value_list[location - 1] * (1 - fee_rate) * indexs_data.loc[date, 'close'] / indexs_data.loc[
                    date, 'open']
                value_list.append(value)
            elif weekday == 1 or weekday == 2 or weekday == 3:
                value = value_list[location - 1]
                value_list.append(value)
            elif weekday == 0:
                value = value_list[location - 1] * (1 + float(indexs_data.loc[date, 'pct_chg'] / 100)) * (
                        1 - fee_rate - tax_rate)
                value_list.append(value)
        # 熊市的操作：周二开盘买入，周三收盘卖
        else:
            if weekday == 1:
                value = value_list[location - 1] * (1 - fee_rate) * indexs_data.loc[date, 'close'] / indexs_data.loc[
                    date, 'open']
                value_list.append(value)
            elif weekday == 2:
                value = value_list[location - 1] * (1 + float(indexs_data.loc[date, 'pct_chg'] / 100)) * (
                        1 - fee_rate - tax_rate)

                value_list.append(value)
            elif weekday == 0 or weekday == 4 or weekday == 3:
                value = value_list[location - 1]
                value_list.append(value)
    value_df['value'] = value_list
    # 下面的两行是设置基准，归一化
    value_df['value'] = value_df['value'] / value_list[0]
    value_df['benchmark'] = value_df['benchmark'] / value_df['benchmark'][0]
    return value_df


token = '5c07c5fb27eebb27211a43c64f754c56e013f80f381b54e3c3e73f0f'
pro = ts.pro_api(token)

# 获取指数数据
# 常用大盘指数
indexs = {'上证综指': '000001.SH', '深证成指': '399001.SZ', '沪深300': '000300.SH',
          '上证50': '000016.SH', '中证500': '000905.SH', '上证180': '000010.SH'}

start = '20070101'
end = '20201030'
index = '000001.SH'
fee_rate = 0.0003
tax_rate = 0.001

value_df = weekly_value_cal(index, start, end, rollings=30, fee_rate=0.0003, tax_rate=0.001)
print(value_df)

line = Line()
# x铀
line.add_xaxis(value_df.index.to_list())
# 每个y轴
line.add_yaxis("benchmark", value_df['benchmark'].round(5).to_list())
line.add_yaxis("my_stra", value_df['value'].round(5).to_list())

# 图表配置
line.set_global_opts(
    title_opts=opts.TitleOpts(title='黑色星期四择时策略）\n 2007-2020'),
    tooltip_opts=opts.TooltipOpts(trigger='axis', axis_pointer_type='cross'),
    toolbox_opts=opts.ToolboxOpts()
)
line.render('black_Thurs（第二版避开周四优化）.html')
