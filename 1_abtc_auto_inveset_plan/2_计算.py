import pandas as pd
from function import *
import matplotlib.pyplot as plt

pd.set_option('expand_frame_repr', False)  # 当列太多时不换行
pd.set_option('display.max_rows', 5000)  # 最多显示数据的行数

can_sell = False  # 是否允许卖出
region = 0.1  # 单位范围X
step = 0.1  # 单位定投率Y

invest_cash = 108

now_price = 44083.6
ma_price = 47369.35

bias = (now_price - ma_price) / ma_price

# 计算高于均线的扣款率
if (bias >= 0) & (bias < region):
    invest_rate = 1 - step
if (bias >= region) & (bias < 2 * region):
    invest_rate = 1 - 2 * step
if (bias >= 2 * region) & (bias < 3 * region):
    invest_rate = 1 - 3 * step
if (bias >= 3 * region) & (bias < 4 * region):
    invest_rate = 1 - 4 * step
if (bias >= 4 * region) & (bias < 5 * region):
    invest_rate = 1 - 5 * step
if bias >= 5 * region:
    invest_rate = 1 - 6 * step
# 计算低于均线的扣款率
if (bias >= -region) & (bias < 0):
    invest_rate = 1 + step
if (bias >= -2 * region) & (bias < -region):
    invest_rate = 1 + 2 * step
if (bias >= -3 * region) & (bias < -2 * region):
    invest_rate = 1 + 3 * step
if (bias >= -4 * region) & (bias < -3 * region):
    invest_rate = 1 + 4 * step
if (bias >= -5 * region) & (bias < -4 * region):
    invest_rate = 1 + 5 * step
if bias < -5 * region:
    invest_rate = 1 + 6 * step

print("invest_rate-------------:%f" % invest_rate)
smart_invest = invest_cash * invest_rate
print("smart_invest-----------:%f" % smart_invest)
print("invest_追加-----------:%f" % (smart_invest - invest_cash))

#
# # 比较均线定投和普通定投的区别
# df = compare_smart_and_normal_invest(df, week=week, invest_cash=invest_cash, trade_rate=0.15 / 100, can_sell=can_sell)[
#     0]
#
# # 绘制资金曲线
# # draw_pic(df, invest='normal_invest_all', capital='normal_capital', invest_name='累计投入资金', capital_name='持有市值')
#
# draw_pic(df, invest='smart_invest_all', capital='smart_capital', invest_name='累计投入资金', capital_name='持有市值')
#
# # df.to_csv('E:\聪明（D：%s,X:%s,Y:%s）.csv' % (days, region, step), encoding='gbk', index=False)
# df.to_csv('聪明aaa.csv', encoding='gbk', index=False)
#
# print(df.tail(5))
exit()
