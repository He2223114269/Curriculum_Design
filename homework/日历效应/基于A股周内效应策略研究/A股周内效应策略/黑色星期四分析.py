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


def get_high_low(code, start, end):
    df = get_index_data(code, start, end)
    df['high_low'] = (df['open']/df['pre_close'])-1
    return df

def judge_bull_bear(code, start, end, rollings=20, typ='up'):
    df = get_index_data(index, start, end)
    if typ=='up':
        df.loc[(df['close'] > df['close'].rolling(20, min_periods=1).mean()), typ] = True
    elif typ=='down':
        df.loc[(df['close'] < df['close'].rolling(20, min_periods=1).mean()), typ] = True
    else:
        print("请输入up或者down,其他输入不合法")
    df[typ].fillna(value=False, inplace=True)
    df = df[df[typ] == True]
    return df


# 这里填入你自己在tushare的token，这个是我之前的，已经更新了
token = '5c07c5fb27eebb27211a43c64f754c56e013f80f381b54e3c3e73f0f'
pro = ts.pro_api(token)

# 获取指数数据
# 常用大盘指数
indexs = {'上证综指': '000001.SH', '深证成指': '399001.SZ', '沪深300': '000300.SH',
          '上证50': '000016.SH', '中证500': '000905.SH', '上证180': '000010.SH'}

start = '20060101'
end = '20201030'
index = '000001.SH'

# df = judge_bull_bear(index, start, end, rollings=20, typ='up')
# print(df)



# # -------------------------------------------单个指数的牛熊市周内效应分析--------------------------------
# df = judge_bull_bear(index, start, end, rollings=20, typ='down')
# print(df)
#
# df = df['pct_chg']
# df = df.reset_index()
# df['week'] = df['trade_date'].dt.weekday
# result = df.groupby('week')['pct_chg'].describe()
# all_size = df.groupby('week')['pct_chg'].size()
# up_size = df[df['pct_chg'] > 0].groupby('week')['pct_chg'].size()
# result['win'] = up_size / all_size
# df1 = result[['50%', 'win', 'mean']]
# df1.reset_index(inplace=True)
# num = [0, 1, 2, 3, 4]
# week = ['星期一', '星期二', '星期三', '星期四', '星期五']
# df1.replace(num, week, inplace=True)
# line = Line()
# # x铀
# line.add_xaxis(df1['week'].to_list())
# # 每个y轴
# line.add_yaxis("涨跌幅中位数", df1['50%'].round(5).to_list())
# line.add_yaxis("胜率", df1['win'].round(5).to_list())
# line.add_yaxis("均值", df1['mean'].round(5).to_list())
# # 图表配置
# line.set_global_opts(
#     title_opts=opts.TitleOpts(title='涨跌幅的周内效应（股票指数）\n 2006-2020'),
#     tooltip_opts=opts.TooltipOpts(trigger='axis', axis_pointer_type='cross'),
#     toolbox_opts=opts.ToolboxOpts()
# )
# line.render('bear(one).html')




# ---------------------------------单个指数的周内效应分析----------------------
index_code = '000001.SH'
df = get_index_data(index_code, start, end)
df = df[['close', 'pct_chg', 'amount']]
df = df.reset_index()
df['week'] = df['trade_date'].dt.weekday
result = df.groupby('week')['pct_chg'].describe()
all_size = df.groupby('week')['pct_chg'].size()
up_size = df[df['pct_chg'] > 0].groupby('week')['pct_chg'].size()
result['win'] = up_size / all_size
df1 = result[['50%', 'win', 'mean']]
df1.reset_index(inplace=True)
num = [0, 1, 2, 3, 4]
week = ['星期一', '星期二', '星期三', '星期四', '星期五']
df1.replace(num, week, inplace=True)
print(df1)
line = Line()
# x铀
line.add_xaxis(df1['week'].to_list())
# 每个y轴
line.add_yaxis("涨跌幅中位数", df1['50%'].round(5).to_list())
line.add_yaxis("胜率", df1['win'].round(5).to_list())
line.add_yaxis("均值", df1['mean'].round(5).to_list())
# 图表配置
line.set_global_opts(
    title_opts=opts.TitleOpts(title='涨跌幅的周内效应（股票指数）\n 2006-2020'),
    tooltip_opts=opts.TooltipOpts(trigger='axis', axis_pointer_type='cross'),
    toolbox_opts=opts.ToolboxOpts()
)
line.render('(one)analysis.html')


# --------------------------------------多个指数的周内效应分析---------------------------
index_data = pd.DataFrame()
for name, code in indexs.items():
    index_data[name] = get_index_data(code, start, end)['pct_chg'] #这里可以换成成交量和成交额
index_data = index_data.reset_index()
index_data['week'] = index_data['trade_date'].dt.weekday
all_indexs = pd.DataFrame()
for name, code in indexs.items():
    result = index_data.groupby('week')[name].describe()
    all_size = index_data.groupby('week')[name].size()
    up_size =index_data[index_data[name] > 0].groupby('week')[name].size()
    result['win'] = up_size / all_size
    all_indexs[name] = result['50%']

all_indexs.reset_index(inplace=True)
num = [0, 1, 2, 3, 4]
week = ['星期一', '星期二', '星期三', '星期四', '星期五']
all_indexs= all_indexs.replace(num, week)
print(all_indexs)


line = Line()
# x铀
line.add_xaxis(all_indexs['week'].to_list())
# 每个y轴
for name, code in indexs.items():
    line.add_yaxis(name, all_indexs[name].round(5).to_list())

# 图表配置
line.set_global_opts(
    title_opts=opts.TitleOpts(title='涨跌幅的周内效应（股票指数）\n 2006-2020'),
    tooltip_opts=opts.TooltipOpts(trigger='axis', axis_pointer_type='cross'),
    toolbox_opts=opts.ToolboxOpts()
)
line.render('all_analysis(vol).html') # 发现周五的成交额是最少的，不管是哪一个指数，还有一个逐渐减少的规律


# ---------------------------------------------多个指数的走势---------------------------------
index_data = pd.DataFrame()
for name, code in indexs.items():
    index_data[name] = get_index_data(code, start, end)['close']
# 这个是基准
df = index_data / index_data.iloc[0]

# 用pyecharts 画图
from pyecharts.charts import Line
from pyecharts import options as opts

line = Line()
# x铀
line.add_xaxis(df.index.to_list())
# 每个y轴
line.add_yaxis("上证综指", df['上证综指'].round(2).to_list())
line.add_yaxis("深证成指", df['深证成指'].round(2).to_list())
line.add_yaxis("沪深300", df['沪深300'].round(2).to_list())
line.add_yaxis("上证50", df['上证50'].round(2).to_list())
line.add_yaxis("中证500", df['中证500'].round(2).to_list())
line.add_yaxis("上证180", df['上证180'].round(2).to_list())
# 图表配置
line.set_global_opts(
                     title_opts=opts.TitleOpts(title='A股指数累积收益率\n 2006-2020'),
                     tooltip_opts=opts.TooltipOpts(trigger='axis', axis_pointer_type='cross')
                     )
line.render('all.html')

# -----------------------------------------周内高低开分析--------------------------------
# 结果发现现在a股市场普遍低开为主
index_data = pd.DataFrame()
for name, code in indexs.items():
    index_data[name] = get_high_low(code, start, end)['high_low'] #这里可以换成成交量和成交额
index_data = index_data.reset_index()
index_data['week'] = index_data['trade_date'].dt.weekday

all_indexs = pd.DataFrame()
for name, code in indexs.items():
    result = index_data.groupby('week')[name].describe()
    all_size = index_data.groupby('week')[name].size()
    up_size =index_data[index_data[name] > 0].groupby('week')[name].size()
    result['win'] = up_size / all_size
    all_indexs[name] = result['50%']

all_indexs.reset_index(inplace=True)
num = [0, 1, 2, 3, 4]
week = ['星期一', '星期二', '星期三', '星期四', '星期五']
all_indexs= all_indexs.replace(num, week)
print(all_indexs)


line = Line()
# x铀
line.add_xaxis(all_indexs['week'].to_list())
# 每个y轴
for name, code in indexs.items():
    line.add_yaxis(name, all_indexs[name].round(5).to_list())

# 图表配置
line.set_global_opts(
    title_opts=opts.TitleOpts(title='涨跌幅的周内效应（股票指数）\n 2006-2020'),
    tooltip_opts=opts.TooltipOpts(trigger='axis', axis_pointer_type='cross'),
    toolbox_opts=opts.ToolboxOpts()
)
line.render('high_low_analysis.html')  # 发现周五的成交额是最少的，不管是哪一个指数，还有一个逐渐减少的规律
