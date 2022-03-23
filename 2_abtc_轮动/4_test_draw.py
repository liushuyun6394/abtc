
import pandas as pd
from function import *
import matplotlib.pyplot as plt
pd.set_option('expand_frame_repr', False)  # 当列太多时不换行
pd.set_option('display.max_rows', 5000)  # 最多显示数据的行数

# 读取数据
df = pd.read_csv('abtc_轮动_改进.csv', encoding='gbk', parse_dates=['candle_end_time'])
# df = pd.read_csv('abtc_轮动.csv', encoding='gbk', parse_dates=['candle_end_time'])

df['strategy_net_normal'] = df['total_capital'] / df['normal_invest_all']
# 绘制图片
plt.plot(df['candle_end_time'], df['strategy_net'], label='strategy')
plt.plot(df['candle_end_time'], df['coin1_net'], label='coin1_net')
plt.plot(df['candle_end_time'], df['coin2_net'], label='coin2_net')
plt.plot(df['candle_end_time'], df['strategy_net_normal'], label='strategy_net_normal')
# plt.plot(df['candle_end_time'], df['total_capital'], label='total_capital')
# plt.plot(df['candle_end_time'], df['normal_invest_all'], label='normal_invest_all')
# plt.plot(df['candle_end_time'], df['total_capital_turn'], label='total_capital_turn')
plt.show()

# 保存文件
print(df.tail(10))
df.to_csv('abtc_轮动_改进.csv', encoding='gbk', index=False)
