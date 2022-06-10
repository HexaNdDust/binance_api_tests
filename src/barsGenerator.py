import random
from tkinter import *

class Interface(object):
	def __init__(self, root, row=0, column=0, w_background='#111821'):
		
		self.canvas = Canvas(root, background=w_background)
		self.canvas.pack(side="top", fill="both", expand=True)
		#self.canvas.grid(row=row, column=column, sticky=N+S+W+E)
		
		self.window_high  = root.winfo_height()
		self.window_width = root.winfo_width()
		
		self.max_price = self.window_high
		self.min_price = 0.0
		self.scale_x = 1.0
		self.scale_y = 1.0
		self.delta_x = 0.0
		self.delta_y = 0.0
	
	def normalize(self, p_max, p_min, delta_y=0, delta_x=0):
		self.max_price = p_max
		self.min_price = p_min
		self.delta_x = delta_x
		self.delta_y = delta_y
		self.scale_y = (self.max_price - self.min_price) /\
		               (self.window_high - self.delta_y)
		#print("Normalizing...", p_min, p_max, self.scale_y)
	
	# This method is adapted for binance klines
	def bin_normalize(self, klines, delta_y=0, delta_x=0):
		min_p = 2 ** 31
		max_p = -1
		for bar in klines:
			if float(bar[2]) > max_p:
				max_p = float(bar[2])
			if float(bar[3]) < min_p:
				min_p = float(bar[3])
		self.normalize(max_p, min_p, delta_y, delta_x)
	
	def get_hor_size_bars(self):
		return int(self.window_width // (7 * self.scale_x))
	
	def size_update(self):
		self.window_high = self.canvas.winfo_height()
		self.scale_y = (self.max_price - self.min_price) /\
		               (self.window_high - self.delta_y)
	
	def clear(self):
		self.canvas.delete("all")
	
	# Raw drawing methods : 
	
	def draw_raw_candle(self, p_max, p_min, p_open, p_close, h_pos=1):
		#print("drawing one candle", self.window_high, self.window_width)
		color = '#FF4400'
		if p_open < p_close:
			color = '#00FFAA'
		self.canvas.create_line(h_pos * 7 + 3 + self.delta_x,
		                        self.window_high - (p_min + self.delta_y),
		                        h_pos * 7 + 3 + self.delta_x,
								self.window_high - (p_max + self.delta_y),
		                        fill=color)
		
		self.canvas.create_rectangle(h_pos * 7 + 0 + self.delta_x,
		                             self.window_high - (p_open + self.delta_y),
		                             h_pos * 7 + 6 + self.delta_x,
									 self.window_high - (p_close + self.delta_y),
		                             fill=color, outline='')
	
	def draw_raw_line(self, v_first, v_second, h_first=1, h_second=-1, color='#FFFFFF'):
		sec_point = h_second
		if h_second == -1:
			sec_point = h_first + 1
		self.canvas.create_line(h_first * 7 + 3   + self.delta_x,
		                        self.window_high - (v_first + self.delta_y),
		                        sec_point * 7 + 3 + self.delta_x,
		                        self.window_high - (v_second + self.delta_y),
		                        fill=color)
	
	def draw_canv_line(self, v_first, v_second, h_first, h_second, color='#FFFFFF'):
		self.canvas.create_line(h_first  + self.delta_x,
		                        self.window_high - (v_first  + self.delta_y),
		                        h_second + self.delta_x,
		                        self.window_high - (v_second + self.delta_y),
		                        fill=color)
	
	def draw_raw_bar(self, height, position, line_height=-1):
		color = '#00FF00'
		if line_height == -1:
			line_height = self.window_high // 2
		if height < 0:
			color = '#FF0000'
		self.canvas.create_rectangle(self.window_width - position * 7 + 1,
		                             self.window_high  - line_height,
		                             self.window_width - position * 7 + 6,
		                             self.window_high  - line_height - height,
		                             fill=color, outline='')
	
	def draw_raw_grid(self, color):
		w_n = 6
		h_n = 5
		w_s = self.canvas.winfo_width()
		h_s = self.canvas.winfo_height()
		
		k = (h_s * 3) / (w_s * 2)
		if k > 1:
			h_n = 5 * k
		else:
			w_n = 6 / k
		
		w_size = w_s / (w_n * 2)
		h_size = h_s / (h_n * 2)
		
		#print(int(h_n), int(w_n))
		for i in range(round(h_n)):
			self.canvas.create_line(0,   int(h_size + i * h_size * 2),
			                        w_s, int(h_size + i * h_size * 2),
									fill=color)
		
		for i in range(round(w_n)):
			self.canvas.create_line(int(w_size + i * w_size * 2), 0,
			                        int(w_size + i * w_size * 2), h_s,
									fill=color)
	
	# Scailed drawing methods : 
	
	def draw_candle(self, p_max, p_min, p_open, p_close, h_pos = 1):
		p_max   = int((p_max   - self.min_price) / self.scale_y)
		p_min   = int((p_min   - self.min_price) / self.scale_y)
		p_open  = int((p_open  - self.min_price) / self.scale_y)
		p_close = int((p_close - self.min_price) / self.scale_y)
		self.draw_raw_candle(p_max, p_min, p_open, p_close, h_pos)
	
	def draw_line(self, v_first, v_second, h_first=1, h_second=-1, color='#FFFFFF'):
		v_first  = int((v_first  - self.min_price) / self.scale_y)
		v_second = int((v_second - self.min_price) / self.scale_y)
		self.draw_raw_line(v_first, v_second, h_first, h_second, color)
	
	def draw_bar(self, height, position, line_height = -1):
		n_height = int((height - self.min_price) / self.scale)
		self.draw_raw_colomn(height, position, line_height)
	
	# draw methods for arrays of data : 
	
	def draw_bin_candle_chart(self, klines):
		# This method is adapted for binance klines
		for i in range(len(klines)):
			self.draw_candle(float(klines[i][2]),
			                 float(klines[i][3]),
							 float(klines[i][1]),
							 float(klines[i][4]), i)
	
	def draw_simple_line_array_n(self, inp_array, shift=0, color='#FFFFFF'):
		if len(inp_array) < 2:
			return
		for i in range(0, len(inp_array), 2):
			self.draw_line(inp_array[i], inp_array[i + 1], i + shift, -1, color)
	
	def draw_line_array_n(self, inp_array, shift=0, color='#FFFFFF'):
		if len(inp_array) < 2:
			return
		temp = inp_array[0]
		for i in range(1, len(inp_array)):
			self.draw_line(temp, inp_array[i], i + shift, -1, color)
			temp = inp_array[i]
	
	def random_Graph(self):
		price = int(random.random() * 100)
		for i in range(1, 145):
			p_cls = price + int(random.random() * 100) - 50
			p_mx = max(price, p_cls) + int(random.random() * 50)
			p_mn = min(price, p_cls) - int(random.random() * 50)
			self.draw_candle(p_mx, p_mn, price, p_cls, i)
			price = p_cls
