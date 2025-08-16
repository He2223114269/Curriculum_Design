# -*- coding: utf-8 -*-
import backtrader as bt
import pandas as pd
import matplotlib.pyplot as plt
import tushare as ts
import datetime
from pyecharts.charts import Line, Scatter
from pyecharts import options as opts
from pyecharts.faker import Faker

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


token = '5c07c5fb27eebb27211a43c64f754c56e013f80f381b54e3c3e73f0f'
pro = ts.pro_api(token)

# 获取指数数据
# 常用大盘指数
indexs = {'上证综指': '000001.SH', '深证成指': '399001.SZ', '沪深300': '000300.SH',
          '创业板指': '399006.SZ', '上证50': '000016.SH', '中证500': '000905.SH',
          '中小板指': '399005.SZ', '上证180': '000010.SH'}
start = '20131117'
end = '20201030'

index_data = pd.DataFrame()
for name, code in indexs.items():
    index_data[name] = get_index_data(code, start, end)['close']
df = index_data / index_data.iloc[0]

# 用pyecharts 画图
# from pyecharts.charts import Line
# from pyecharts import options as opts
#
# line = Line()
# # x铀
# line.add_xaxis(df.index.to_list())
# # 每个y轴
# for name, code in indexs.items():
#     line.add_yaxis(name, df[name].round(2).to_list())
# # 图表配置
# line.set_global_opts(
#                      title_opts=opts.TitleOpts(title='A股指数累积收益率\n 2014-2020'),
#                      tooltip_opts=opts.TooltipOpts(trigger='axis', axis_pointer_type='cross')
#                      )
# line.render('all_indexs.html')


# 将价格数据转为收益率
all_ret = index_data / index_data.shift(1) - 1  # 计算涨跌幅赋给一个新的列表
north_data = get_north_money(start, end)
all_data = all_ret.join(north_data['north_money'], how='inner')
all_data.rename(columns={'north_money': '北向资金'}, inplace=True)
all_data.dropna(inplace=True)
# print(all_data)
print(all_data.corr()) # 计算北向资金与各大指数的相关性系数，这个时候相关性不大
# 移动窗口计算短期（120内）的北向资金与各大指数的相关性系数，这里能达到0.7
# 输出后9行数据
print(all_data.rolling(120).corr().tail(9))

# import seaborn as sns
#
# plt.figure(figsize=(10, 6))
# sns.regplot(x=list(all_data["北向资金"][-120:]), y=list(all_data["沪深300"][-120:]))
# plt.title('沪深300与北向资金拟合回归线', size=15)
# plt.xlabel('北向资金', size=12)
# plt.ylabel('沪深300收益率', size=12)
# plt.show()

# ----------------------------------拟回归分析---------------------------------
# sca = Scatter()
# sca.add_xaxis(list(all_data["北向资金"][-120:].round(2)))
# sca.add_yaxis("沪深300收益率", list(all_data["沪深300"][-120:].round(2)),
#               label_opts=opts.LabelOpts(is_show=False),  # 数据不显示
#               symbol_size=5,  # 设置散点的大小
#               # symbol='pin',  # 设置散点的形状（cricle,rect,pin,triangle）
#               )
# sca.set_global_opts(title_opts=opts.TitleOpts(title="沪深300与北向资金拟合回归线"),
#                     xaxis_opts=opts.AxisOpts(name='北向资金', type_='value', split_number=10),
#                     yaxis_opts=opts.AxisOpts(name='沪深300收益率', type_='value', split_number=10)
#                     )
# sca.render('回归线.html')

# ------------------------------------沪深300日收益率 VS 北向资金---------------------------
# # 沪深300指数收益率与北向资金
# final_data = all_data[['沪深300', '北向资金']].dropna()
#
# line1 = Line()
# # x铀
# line1.add_xaxis(final_data.index.to_list())
# # 每个y轴
# line1.add_yaxis('北向资金', final_data['北向资金'].round(3).to_list(), yaxis_index=0,)
# line1.extend_axis(yaxis=opts.AxisOpts())
#
# line2 = Line()
# line2.add_xaxis(final_data.index.to_list())
# line2.add_yaxis('沪深300日收益率', final_data['沪深300'].round(3).to_list(), yaxis_index=1)
#
# line1.overlap(line2)
# # 图表配置
# line1.set_global_opts(
#                      title_opts=opts.TitleOpts(title='沪深300日收益率 VS 北向资金\n 2014-2020'),
#                      tooltip_opts=opts.TooltipOpts(trigger='axis', axis_pointer_type='cross')
#                      )
# line1.render('沪深300日收益率 VS 北向资金.html')


# --------------------------------------------沪深300与北向资金移动120日相关系数----------------------
# cor=cal_rol_cor(final_data,period=120)
# print(cor)
# cor.describe()
# print(cor.describe())
# cor_mean = []
# for i in cor:
#     cor_mean.append(cor.mean())
# line = Line()
# line.add_xaxis(final_data.index.to_list())
# # 每个y轴
# line.add_yaxis('相关性系数', cor.values.round(3))
# line.add_yaxis('相关系数均值', cor_mean)
# # 图表配置
# line.set_global_opts(
#                      title_opts=opts.TitleOpts(title='沪深300与北向资金移动120日相关系数\n 2014-2020'),
#                      tooltip_opts=opts.TooltipOpts(trigger='axis', axis_pointer_type='cross')
#                      )
# line.render('沪深300与北向资金移动120日相关系数.html')
