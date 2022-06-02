from api import BinanceAPI
client = BinanceAPI('vmPUZE6mv9SD5VNHk4HlWFsOr6aKE2zvsw0MuIgwCIPy6utIco14y7Ju91duEh8A',
					'NhqPtmdSJYdKjVHjA7PZj4Mge3R5YNiP1e3UZjInClVN65XAbvqqM6A7H5fATj0j')
					# This keys is given by binance examples and dont attached to any account :T

from barsGenerator import *

from TimeSeriesInstruments import *
timeSeries = TimeSeries()

def Normalize(interface, klines):
	min_p = 2 ** 20
	max_p = -1
	for bar in klines:
		if float(bar[2]) > max_p:
			max_p = float(bar[2])
		if float(bar[3]) < min_p:
			min_p = float(bar[3])
	interface.mormalize(max_p, min_p, 100)
	#print(max_p, min_p)

def ShowGraph(interface, klines):
	i = 1
	for bar in klines:
		interface.draw_Bar_n(float(bar[2]), float(bar[3]), float(bar[1]), float(bar[4]), i)
		i += 1

def mean_from_klines(klines):
	out_array = []
	for i in range(len(klines)):
		out_array.append((float(klines[i][1]) + float(klines[i][4])) / 2)
	return out_array


All_prices = client.allPrices()
#for elem in All_prices:
#	if not elem['symbol'].find('USDT') == -1:
#		print(elem)

symbol = 'BTCUSDT' #All_prices[30]['symbol']
interface = Interface(720, 1280, symbol)
kline = client.klines(symbol, '1h', limit = interface.get_hor_size_bars())
#[ [Open time,   Open,   High,   Low,   Close,   Volume,   Close time,
#   Quote asset volume,   Number of trades, Taker buy base asset volume, Taker buy quote asset volume, Ignore],... ]


Normalize(interface, kline)
ShowGraph(interface, kline)

level = 20
interface.draw_array_n(timeSeries.Blend_LWMA(mean_from_klines(kline), level), level - 1, '#00FF00')

#level = 5
interface.draw_array_n(timeSeries.Blend_SMA(mean_from_klines(kline), level), level - 1, '#FF0000')








interface.Quit()