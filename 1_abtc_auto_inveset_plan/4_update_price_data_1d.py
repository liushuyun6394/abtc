import ccxt
import time
import json
import logging
import pandas as pd

# logging.basicConfig(level=logging.DEBUG)
# ===获取行情数据
# 申明okex交易所
# exchange = ccxt.okex3()

# 获取最新的ticker数据，运行需要翻墙，btc、ltc
# data = exchange.fetchTicker(symbol='BTC/USDT')
# 获取最新的K线数据：日线、小时线
# data = exchange.fetch_ohlcv(symbol='BTC/USDT', timeframe='1h', limit=50)  # '1h'，'1d'

# 获取币安交易所的相关数据
# exchange = ccxt.binance()
# data = exchange.fetchTicker(symbol='BTC/USDT')

# ===下单交易
# 申明币安交易所
# exchange = ccxt.binance()
# 走代理
exchange = ccxt.binance({
    'enableRateLimit': True,
    # 'rateLimit': 1000,  # unified exchange property
    'proxies': {
        'http': 'http://localhost:41091',
        'https': 'http://localhost:41091',
    },
})
# 填写API秘钥
exchange.apiKey = 'tjhvSu7O78YaFb0AIB1qmvPRRnB8zF3cLuhaZ9qjLQpEXeCblaV9WnN9B1ss1DuA'
exchange.secret = 'G5HDKOOcqXaIEsEUFIu3B142JGUJGNBG9NGx8U9u8Nqd1bO5mtxyeEtFd3ZMiW0K'

# 获取账户余额
# balance = exchange.fetch_balance()
# balance_str = json.dumps(balance, indent=4)
# print(balance_str)

# 限价单卖出：交易对、买卖数量、价格。如何买？
# order_info = exchange.create_limit_sell_order('BTC/USDT', 0.01, 13000)

# 撤单
# order_info = exchange.cancel_order(id='486207276', symbol='BTC/USDT')

# ===完整案例程序1：反复下单、撤单
# while True:
#     order_info = exchange.create_limit_sell_order('BTC/USDT', 0.01, 14000)
#     print('下单完成')
#     time.sleep(2)
#     order_info = exchange.cancel_order(id=order_info['id'], symbol='BTC/USDT')
#     print('撤单完成')
#     time.sleep(2)


# # ===完整案例程序2：实时监测价格达到止损条件后，卖出止损
# while True:
#     # 获取最新价格数据
#     data = exchange.fetchTicker(symbol='BTC/USDT')
#     new_price = data['bid']
#     print('最新买一价格：', new_price)
#
#     # 判断是否交易
#     if new_price < 10000:
#         # 下单卖出，止损
#         order_info = exchange.create_market_sell_order('BTC/USDT', 0.01)
#         print('达到止损价，下单卖出。', new_price)
#         break
#     else:
#         print('价格未达止损价，5s后继续监测\n')
#         time.sleep(5)

# ===实盘量化程序流程
# 1. 通过行情接口，获取实时数据
# 2. 根据策略处理数据，产生交易信号
# 3. 根据交易信号实际下单。


# print('暂停5s.................................................')
# time.sleep(5)
data = exchange.fetch_ticker(symbol='BTC/USDT')
new_price = data['bid']
print('最新buy_1_price：', new_price)
# print(json.dumps(data, indent=4))

momentum_days = 20
# 请求的candles个数
limit = 500

# 当前时间
current_time = int(time.time() // 60 * 60 * 1000)  # 毫秒
print(current_time)

# 获取请求开始的时间
since_time = current_time - limit * 60 * 1000

print('BTC/USDT start-------------------------------------------------')
if exchange.has['fetchOHLCV']:
    eth_usdt_OHLCV = exchange.fetch_ohlcv(symbol='BTC/USDT', timeframe='1d')
    print('BTC/USDT', eth_usdt_OHLCV)  # one day

print('-------------------------------------------------')
df = pd.DataFrame(eth_usdt_OHLCV, columns=['candle_end_time', 'open', 'high', 'low', 'close', 'volume'])
# df['candle_end_time'] = df['candle_end_time'].map(lambda x: pd.Timestamp(x, unit="ms"))
df['candle_end_time'] = pd.to_datetime(df['candle_end_time'] / 1000, unit='s',
                                       origin='1970-01-01 08:00:00').dt.strftime('%Y-%m-%d %H:%M:%S')
# print(df)
print(df.tail(10))
df.to_csv('BTCUSD-1d-curr.csv', encoding='gbk', index=False)

time.sleep(exchange.rateLimit / 1000)  # time.sleep wants seconds

print('ETH/USDT start-------------------------------------------------')
if exchange.has['fetchOHLCV']:
    eth_usdt_OHLCV = exchange.fetch_ohlcv(symbol='ETH/USDT', timeframe='1d')
    print('ETH/USDT', eth_usdt_OHLCV)  # one day

print('-------------------------------------------------')
df = pd.DataFrame(eth_usdt_OHLCV, columns=['candle_end_time', 'open', 'high', 'low', 'close', 'volume'])
# df['candle_end_time'] = df['candle_end_time'].map(lambda x: pd.Timestamp(x, unit="ms"))
df['candle_end_time'] = pd.to_datetime(df['candle_end_time'] / 1000, unit='s',
                                       origin='1970-01-01 08:00:00').dt.strftime('%Y-%m-%d %H:%M:%S')
# print(df)
print(df.tail(10))
df.to_csv('ETHUSD-1d-curr.csv', encoding='gbk', index=False)

# df = pd.DataFrame(data)
# df = df.rename(columns={0: 'open_time', 1: 'open', 2: 'high', 3: 'low', 4: 'close', 5: 'volume'})
#
# # 时间转换成北京时间
# df['open_time'] = pd.to_datetime(df['open_time'], unit='ms') + pd.Timedelta(hours=8)
# # 设置index
# df = df.set_index('open_time', drop=True)
# # 保存成csv文件
# df.to_csv('bitmex_data.csv')  # comma seperate Value
# print(df)
exit()
