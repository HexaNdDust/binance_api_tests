'''
// 
# in bin api, klines has view: 
#[
#  [Open time,   Open,   High,   Low,   Close,   Volume,   Close time,
#   Quote asset volume,   Number of trades, Taker buy base asset volume,
#	Taker buy quote asset volume, Ignore],...
#]
// 
'''

from tkinter import *
from api import BinanceAPI
from barsGenerator import *
from TimeSeriesInstruments import *
from balance import *

client = BinanceAPI(
'vmPUZE6mv9SD5VNHk4HlWFsOr6aKE2zvsw0MuIgwCIPy6utIco14y7Ju91duEh8A',
'NhqPtmdSJYdKjVHjA7PZj4Mge3R5YNiP1e3UZjInClVN65XAbvqqM6A7H5fATj0j')
# This keys is given by binance examples and dont attached to any account :T

timeSeries = TimeSeries()
balance = Balance()

# ==============================================================================
last_width, last_height = 0, 0
def respond(event):
	global last_height, last_width
	if last_width != event.width or last_height != event.height:
		last_height = event.height
		last_width = event.width
		outPort.clear()
		drawScreen()

# Need to be moved into binApi
def mean_from_klines(klines, openClose = 0):
	out_array = []
	opCl = 1 + openClose * 3
	for i in range(len(klines)):
		out_array.append(float(klines[i][opCl]))
	return out_array	

def drawScreen():
	outPort.draw_raw_grid('#212831')
	outPort.size_update()
	outPort.draw_bin_candle_chart(klines)
	
	level = 75
	outPort.draw_line_array_n(timeSeries.blend_LWMA(mean_from_klines(klines),
	                                                level), level - 1, '#00FF00')
	
	level = 5
	outPort.draw_line_array_n(timeSeries.blend_SMA(mean_from_klines(klines),
	                                               level), level - 1, '#FF0000')
	
	outPort.draw_line_array_n(timeSeries.blend_EMA(mean_from_klines(klines),
	                                               level), 0, '#FFFF00')

# ==============================================================================

#All_prices = client.allPrices()
#for elem in All_prices:
#	if not elem['symbol'].find('USDT') == -1:
#		print(elem)

symbol = 'BTCUSDT' #All_prices[30]['symbol']
klines = client.klines(symbol, '1d', limit = 500)

root = Tk()
root.geometry('600x400')
root.title(symbol)
root.minsize(150, 100)
root.update()

outPort = Interface(root)
outPort.bin_normalize(klines, 0, 3)
root.bind("<Configure>", respond)

root.mainloop()
