
import pandas as pd
import os
import math
import datetime
import matplotlib.pyplot as plt

_ = os.path.abspath(os.path.dirname(__file__))  # 返回当前文件路径
root_path = os.path.abspath(os.path.join(_, '../../..'))  # 返回根目录文件夹


# 对比智能定投和普通定投的区别
# df：原始数据，week:周几定投,invest_cash:定投金融，trade_rate：交易费率，can_sell：是否允许卖出
def compare_smart_and_normal_invest(df, week, invest_cash, trade_rate, can_sell=False):
    # 计算投资金额
    df.reset_index(drop=True, inplace=True)
    df.loc[(df['week'] == week), 'smart_invest'] = df['invest_rate'] * invest_cash
    df.loc[(df['week'] == week), 'normal_invest'] = invest_cash
    # 计算买入份额
    df['si_share'] = df['smart_invest'] / (df['close'] * (1 + trade_rate))
    df['si_share'].fillna(value=0, inplace=True)
    df['ni_share'] = df['normal_invest'] / (df['close'] * (1 + trade_rate))
    df['smart_share'] = df['si_share'].cumsum()
    df['normal_share'] = df['ni_share'].cumsum()
    # 处理一下没有份额卖出的情况
    if can_sell:
        for i in range(0, df.shape[0]):
            if i == 0:
                df['smart_share'][i] = 0 + df['si_share'][i]
            if i != 0:
                df['smart_share'][i] = df['si_share'][i] + df['smart_share'][i - 1]
            if df['smart_share'][i] < 0:
                df['smart_share'][i] = 0
                if i != 0:
                    df['smart_invest'][i] = -df['smart_share'][i - 1] * df['close'][i] / (1 + trade_rate)

    df.loc[(df['smart_share'] == 0) & (df['smart_share'].shift(1) == 0), 'smart_invest'] = 0.0
    df['smart_share'].fillna(method='ffill', inplace=True)
    df['normal_share'].fillna(method='ffill', inplace=True)

    df['smart_capital'] = df['smart_share'] * df['close']
    df['normal_capital'] = df['normal_share'] * df['close']

    df['smart_invest_all'] = df['smart_invest'].cumsum()
    df['normal_invest_all'] = df['normal_invest'].cumsum()

    df['smart_rate'] = df['smart_capital'] / df['smart_invest_all']
    df['normal_rate'] = df['normal_capital'] / df['normal_invest_all']

    si_invest_all = round(df['smart_invest'].sum(), 2)
    ni_invest_all = round(df['normal_invest'].sum(), 2)

    si_capital = round(df['smart_capital'].iloc[-1], 2)
    ni_capital = round(df['normal_capital'].iloc[-1], 2)
    print('【智能定投】总投入：%s  总资产：%s  资产/投入：%s' % (si_invest_all, si_capital, si_capital / si_invest_all))
    print('【普通定投】总投入：%s  总资产：%s  资产/投入：%s' % (ni_invest_all, ni_capital, ni_capital / ni_invest_all))
    return df, si_invest_all, si_capital, si_capital / si_invest_all, ni_invest_all, ni_capital, ni_capital / ni_invest_all


# 绘制图片
def draw_pic(df, date='candle_time', invest='invest', capital='capital', invest_name='invest', capital_name='capital'):
# def draw_pic(df, date='candle_end_time', invest='invest', capital='capital', invest_name='invest', capital_name='capital'):
    plt.rcParams["font.family"] = 'Arial Unicode MS'
    df[invest].fillna(method='ffill', inplace=True)
    df[capital].fillna(method='ffill', inplace=True)
    plt.figure(figsize=(8.64, 4.8))
    plt.plot(df[date], df[invest], label=invest_name)
    plt.plot(df[date], df[capital], label=capital_name)
    plt.legend(loc='best')
    plt.show()
