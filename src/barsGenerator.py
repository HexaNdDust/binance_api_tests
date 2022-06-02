import random
from tkinter import *

class Interface(object):
	def __init__(self, high = 720, width = 1280, w_name = 'No name'):
		self.window_high = high
		self.window_width = width
		
		self.root = Tk()
		self.root.title(w_name)
		self.root.resizable(0, 0)
		
		self.max_price = high
		self.min_price = 0
		self.scale = 1
		self.delta = 0
		
		self.canvas = Canvas(self.root, width = self.window_width, height = self.window_high, background = '#001122')
		self.canvas.pack()
	
	
	# Initializing methods :
	
	def get_hor_size_bars(self):
		return self.window_width // 7 - 1
	
	
	def Normalize(self, p_max, p_min, delta = 0):
		self.max_price = p_max
		self.min_price = p_min
		self.delta = delta
		self.scale = (self.max_price - self.min_price) / (self.window_high - self.delta)
	
	
	def Quit(self):
		self.root.mainloop()
	
	
	# Raw drawing functions : 
	
	def draw_Bar(self, p_max, p_min, p_open, p_close, h_pos = 2, v_pos = 360):
		if p_open < p_close:
			color = '#00FFAA'
		else:
			color = '#FF4400'
		
		self.canvas.create_line(h_pos * 7 + 3, v_pos - p_min, h_pos * 7 + 3, v_pos - p_max, fill = color)	
		self.canvas.create_rectangle( h_pos * 7 + 1,
								v_pos - p_open,
								h_pos * 7 + 6,
								v_pos - p_close,
								fill = color,
								outline = '')
		self.root.update()
	
	
	def draw_line(self, v_first, v_second, h_first = 1, h_second = -1, color = '#FFFFFF'):
		if h_second == -1:
			self.canvas.create_line(h_first * 7 + 3, self.window_high - v_first - self.delta, (h_first + 1) * 7 + 3, self.window_high - v_second - self.delta, fill = color)
		else:
			self.canvas.create_line(h_first * 7 + 3, self.window_high - v_first - self.delta, h_second * 7 + 3, self.window_high - v_second - self.delta, fill = color)
	
	
	def random_Graph(self):
		price = int(random.random() * 100)
		
		for i in range(1, 145):
			p_cls = price + int(random.random() * 100) - 50
			p_mx = max(price, p_cls) + int(random.random() * 50)
			p_mn = min(price, p_cls) - int(random.random() * 50)
			
			self.draw_Bar(p_mx, p_mn, price, p_cls, i)
			price = p_cls
	
	'''
	def draw_colomn(self, height, position, line_height):
		if height < 0:
			
		else:
			
	'''
	
	# Normalized drawing functions :
	
	def draw_Bar_n(self, p_max, p_min, p_open, p_close, h_pos = 2):
		p_max   = int((p_max - self.min_price)   / self.scale)
		p_min   = int((p_min - self.min_price)   / self.scale)
		p_open  = int((p_open - self.min_price)  / self.scale)
		p_close = int((p_close - self.min_price) / self.scale)
		
		self.draw_Bar(p_max, p_min, p_open, p_close, h_pos, self.window_high - self.delta)
	
	
	def draw_line_n(self, v_first, v_second, h_first = 1, h_second = -1, color = '#FFFFFF'):
		v_first = int((v_first - self.min_price)   / self.scale)
		v_second = int((v_second - self.min_price)   / self.scale)
		
		self.draw_line(v_first, v_second, h_first, h_second, color)
	
	def draw_array_n(self, inp_array, shift = 0, color = '#FFFFFF'):
		if len(inp_array) < 2:
			return
		temp = inp_array[0]
		for i in range(1, len(inp_array)):
			self.draw_line_n(temp, inp_array[i], i + shift, -1, color)
			temp = inp_array[i]
	