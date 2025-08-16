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


# 基础周内策略——周五开盘买入周三收盘卖出
# (买入时万分之三，卖出时万分之三加千分之一印花税)
def weekly_value_cal(code, start, end, fee_rate=0.0003, tax_rate=0.001):
    value_df = pd.DataFrame()
    indexs_data = get_index_data(code, start, end)
    value_df['benchmark'] = indexs_data['close']
    date_list = list(value_df.index)
    if date_list[0].weekday() == 3:
        date_list = date_list.remove(date_list[0])
        value_df = value_df.drop([date_list[0]])
    value_list = [(1 - fee_rate) * indexs_data.loc[date_list[0], 'close']]
    for date in date_list[1:]:
        weekday = date.weekday()
        location = date_list.index(date)
        last_date = date_list[location - 1]
        if weekday == 0 or weekday == 1:
            value = value_list[location - 1] * (1 + float(indexs_data.loc[date, 'pct_chg'] / 100))
            value_list.append(value)
        elif weekday == 2:
            value = value_list[location - 1] * (1 + float(indexs_data.loc[date, 'pct_chg'] / 100)) * (
                    1 - fee_rate - tax_rate)
            value_list.append(value)
        # 这是周三收盘卖，周五开盘买 最后结果 5455
        elif weekday == 3:
            value = value_list[location - 1]
            value_list.append(value)
        elif weekday == 4:
            value = value_list[location - 1] * (1 - fee_rate) * indexs_data.loc[date, 'close'] / indexs_data.loc[
                date, 'open']
            value_list.append(value)
        # 这是周三收盘卖，周四收盘买  最后结果 2478 这就说明了周四到周五普遍是低开的
        # 当然分析到周一到周五都是普遍低开的。周一还稍微好一点
        # elif weekday == 3:
        #     value = value_list[location - 1] * (1 - fee_rate)
        #     value_list.append(value)
        #     print(value)
        # elif weekday == 4:
        #     value = value_list[location - 1] * (1+float(indexs_data.loc[date, 'pct_chg']/100))
        #     value_list.append(value)

    value_df['value'] = value_list
    # value_df['value'] = value_df['value'] / value_list[0]
    return value_df


token = '5c07c5fb27eebb27211a43c64f754c56e013f80f381b54e3c3e73f0f'
pro = ts.pro_api(token)

# 获取指数数据
# 常用大盘指数
indexs = {'上证综指': '000001.SH', '深证成指': '399001.SZ', '沪深300': '000300.SH',
          '上证50': '000016.SH', '中证500': '000905.SH', '上证180': '000010.SH'}

start = '20060101'
end = '20201030'
code = '000001.SH'
fee_rate = 0.0003
tax_rate = 0.001

# -------------------------单个指数的黑色星期四择时策略--------------------------
# value_df = weekly_value_cal(code, start, end, fee_rate=0.0003, tax_rate=0.001)
# print(value_df)
#
# line = Line()
# # x铀
# line.add_xaxis(value_df.index.to_list())
# # 每个y轴
# line.add_yaxis("benchmark", value_df['benchmark'].round(5).to_list())
# line.add_yaxis("my_stra", value_df['value'].round(5).to_list())
#
# # 图表配置
# line.set_global_opts(
#     title_opts=opts.TitleOpts(title='黑色星期四择时策略）\n 2006-2020'),
#     tooltip_opts=opts.TooltipOpts(trigger='axis', axis_pointer_type='cross'),
#     toolbox_opts=opts.ToolboxOpts()
# )
# line.render('black_Thurs（第一版避开周四）.html')


# -------------------------多个指数的黑色星期四择时策略--------------------------

value_df = pd.DataFrame()
benchmark_df = pd.DataFrame()
for name, code in indexs.items():
    value_df[name] = weekly_value_cal(code, start, end, fee_rate=0.0003, tax_rate=0.001)['value']
    benchmark_df[name] = weekly_value_cal(code, start, end, fee_rate=0.0003, tax_rate=0.001)['benchmark']
line = Line()
# x铀
line.add_xaxis(value_df.index.to_list())
# 每个y轴
for name, code in indexs.items():
    line.add_yaxis(name, benchmark_df[name].round(5).to_list())
    line.add_yaxis(name+'my_stra', value_df[name].round(5).to_list())

# 图表配置
line.set_global_opts(
    title_opts=opts.TitleOpts(title='黑色星期四择时策略）\n 2006-2020'),
    tooltip_opts=opts.TooltipOpts(trigger='axis', axis_pointer_type='cross'),
    toolbox_opts=opts.ToolboxOpts()
)
line.render('black_Thurs（第一版避开周四）.html')