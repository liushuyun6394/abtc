import pandas as pd
from function import *
import matplotlib.pyplot as plt

pd.set_option('expand_frame_repr', False)  # 当列太多时不换行
pd.set_option('display.max_rows', 5000)  # 最多显示数据的行数

# 读取数据
# df = pd.read_csv('BTC-USDT-1d.csv', encoding='gbk', parse_dates=['candle_time'])
df = pd.read_csv('BTC-USDT-1d-sum.csv', encoding='gbk', parse_dates=['candle_time'])
# df = pd.read_csv('BTCUSD-1d-curr.csv', encoding='gbk', parse_dates=['candle_time'])
# 设置参数
can_sell = False  # 是否允许卖出
days = 250  # 均线日期D
region = 0.1  # 单位范围X
step = 0.1  # 单位定投率Y

invest_cash = 1000  # 每次的基准定投金额
week = 4  # 每周几定投。0代表周一，1代表周二，以此类推

# 计算均线
df['ma'] = df['close'].rolling(days, min_periods=1).mean()
# 从17年开始回测
# df = df[df['candle_time'] >= pd.to_datetime('20170101')]
# df = df[df['candle_time'] >= pd.to_datetime('20171202')]
df = df[df['candle_time'] >= pd.to_datetime('20171217')]

# df['week'] = df['candle_time'].dt.dayofweek
df['week'] = df['candle_time'].dt.dayofweek
df['bias'] = (df['close'] - df['ma']) / df['ma']

# 计算高于均线的扣款率
df.loc[(df['bias'] >= 0) & (df['bias'] < region), 'invest_rate'] = 1 - step
df.loc[(df['bias'] >= region) & (df['bias'] < 2 * region), 'invest_rate'] = 1 - 2 * step
df.loc[(df['bias'] >= 2 * region) & (df['bias'] < 3 * region), 'invest_rate'] = 1 - 3 * step
df.loc[(df['bias'] >= 3 * region) & (df['bias'] < 4 * region), 'invest_rate'] = 1 - 4 * step
df.loc[(df['bias'] >= 4 * region) & (df['bias'] < 5 * region), 'invest_rate'] = 1 - 5 * step
df.loc[(df['bias'] >= 5 * region), 'invest_rate'] = 1 - 6 * step
if not can_sell:
    df.loc[(df['invest_rate'] < 0), 'invest_rate'] = 0

# 计算低于均线的扣款率
df.loc[(df['bias'] >= -region) & (df['bias'] < 0), 'invest_rate'] = 1 + step
df.loc[(df['bias'] >= -2 * region) & (df['bias'] < -region), 'invest_rate'] = 1 + 2 * step
df.loc[(df['bias'] >= -3 * region) & (df['bias'] < -2 * region), 'invest_rate'] = 1 + 3 * step
df.loc[(df['bias'] >= -4 * region) & (df['bias'] < -3 * region), 'invest_rate'] = 1 + 4 * step
df.loc[(df['bias'] >= -5 * region) & (df['bias'] < -4 * region), 'invest_rate'] = 1 + 5 * step
df.loc[(df['bias'] < -5 * region), 'invest_rate'] = 1 + 6 * step

# 比较均线定投和普通定投的区别
df = compare_smart_and_normal_invest(df, week=week, invest_cash=invest_cash, trade_rate=0.15 / 100, can_sell=can_sell)[
    0]

# 绘制资金曲线
# draw_pic(df, invest='normal_invest_all', capital='normal_capital', invest_name='累计投入资金', capital_name='持有市值')

draw_pic(df, invest='smart_invest_all', capital='smart_capital', invest_name='累计投入资金', capital_name='持有市值')

# df.to_csv('E:\聪明（D：%s,X:%s,Y:%s）.csv' % (days, region, step), encoding='gbk', index=False)
df.to_csv('聪明abtc.csv', encoding='gbk', index=False)

print(df.tail(5))
exit()
