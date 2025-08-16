import pandas as pd
import tushare as ts
standard=ts.get_hist_data('000688',start='2019-07-22',end='2021-10-30')


from pandas_datareader import data
import matplotlib.pyplot as plt
import numpy as np
standard_close=standard.close
ls=np.arange(1,len(standard_close) + 1)
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
plt.rcParams["font.sans-serif"] = ["SimHei"]   # 用来正常显示中文标签
plt.rcParams["axes.unicode_minus"] = False     # 解决负号"-"显示为方块的问题
fig=plt.figure( figsize=(10,7) )   #定义整个画布
ax=fig.add_subplot(2,2,(1,2))                     #第一个子图ax.xaxis.set_major_locator(plt.MultipleLocator(60))
ax.xaxis.set_minor_locator(plt.MultipleLocator(30))
plt.plot(ls,standard_close)
plt.tick_params(labelsize=13)
plt.tick_params(axis='both',which='major',labelsize=14)
plt.xlabel('Date',fontsize=14)
plt.ylabel('Close',fontsize=14)
plt.rcParams['lines.linewidth'] = 2
plt.legend(['Close'],fontsize = 13)
plt.title('科创50收盘价趋势图')

