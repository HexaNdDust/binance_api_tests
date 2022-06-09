'''
// 
// 
# in bin api, klines has view of: 
#[ [Open time,   Open,   High,   Low,   Close,   Volume,   Close time,
#   Quote asset volume,   Number of trades, Taker buy base asset volume, Taker buy quote asset volume, Ignore],... ]
// 
// 
'''

from tkinter import *
from api import BinanceAPI
from barsGenerator import *
from TimeSeriesInstruments import *
from balance import *


#client = BinanceAPI('vmPUZE6mv9SD5VNHk4HlWFsOr6aKE2zvsw0MuIgwCIPy6utIco14y7Ju91duEh8A',
#					'NhqPtmdSJYdKjVHjA7PZj4Mge3R5YNiP1e3UZjInClVN65XAbvqqM6A7H5fATj0j')
					# This keys is given by binance examples and dont attached to any account :T
timeSeries = TimeSeries()
balance = Balance()

#outPort1 =Interface(root)

# ==================================================================================================
def resize(event):
	global window_width, window_height
	if event.widget.widgetName == "toplevel":
		if (window_width != event.width) and (window_height != event.height):
			window_width, window_height = event.width, event.height
			print(f"The width of Toplevel is {window_width} and the height of Toplevel " f"is {window_height}")

last_width, last_height = 0, 0

def respond(event):
	global last_height, last_width
	if last_width != event.width or last_height != event.height:
		print(event.width, event.height)
		last_height = event.height
		last_width = event.width
		outPort.clear()
		outPort.draw_raw_grid('#212831')

# Need to be moved into binApi
def mean_from_klines(klines, openClose = 0):
	out_array = []
	opCl = 1 + openClose * 3
	for i in range(len(klines)):
		out_array.append(float(klines[i][opCl]))
	return out_array
# ==================================================================================================

#All_prices = client.allPrices()
#for elem in All_prices:
#	if not elem['symbol'].find('USDT') == -1:
#		print(elem)

root = Tk()



symbol = 'BTCUSDT' #All_prices[30]['symbol']

outPort = Interface(root, w_height = 720, w_width = 1280, row = 0, column = 0)
#klines = client.klines(symbol, '1d', limit = outPort.get_hor_size_bars())
#outPort.draw_raw_grid('#212831')
#outPort.bin_normalize(klines, 0, 3)
#outPort.draw_bin_candle_chart(klines)



root.bind("<Configure>", respond)

'''
level = 75
outPort.draw_line_array_n(timeSeries.Blend_LWMA(mean_from_klines(kline), level), level - 1, '#00FF00')

level = 5
outPort.draw_line_array_n(timeSeries.Blend_SMA(mean_from_klines(kline), level), level - 1, '#FF0000')

outPort.draw_line_array_n(timeSeries.Blend_EMA(mean_from_klines(kline), level), 0, '#FFFF00')


EMA12 = timeSeries.Blend_EMA(mean_from_klines(kline), 12)
EMA26 = timeSeries.Blend_EMA(mean_from_klines(kline), 26)

outPort.draw_line_array_n(EMA12, 0, '#FF00FF')
outPort.draw_line_array_n(EMA26, 0, '#00FF00')

diff = []
for i in range(len(EMA12)):
	diff.append(EMA12[i] - EMA26[i])

macd = timeSeries.Blend_EMA(diff, 10, 2 / (10 + 1))

outPort.draw_line_array_n(macd, 0, '#FF0000')

for i in range(0, outPort.get_hor_size_bars()):
	outPort.draw_colomn_n((EMA12[i] - EMA26[i]) / 5, i, 620)
'''

root.mainloop()

