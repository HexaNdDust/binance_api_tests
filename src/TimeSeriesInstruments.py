
class TimeSeries(object):
	def __init__(self):
		# Nothing here
		self.nothing = 0
	
	def csum(self, inp_array):
		# Returnes sum of all array
		# input:  array
		# output: sum of array
		c_sum = 0.0
		for elem in inp_array:
			c_sum += elem
		return c_sum
	
	def get_linear_normalized_coefs(self, level):
		# Returnes array of coeffs of function y(x) = (1 - x / n) * 1 / (2 * n)
		# The feature of this function is square under the triangle equals 1
		# and this coeffs may be used for linear weight normalize
		# input:  len of triangle (len of array)
		# output: array of coeffs [level]
		out_array = []
		temp = 2 / level
		for i in range(level):
			out_array.append((1 - (i + 0.5) / level) * temp)
		return out_array
	
	def blend_CMA(self, inp_array):
		# CMA (cumulative moving average) - arithmetic mean of all period
		# input:  array of states [count]	out_array = []
		# output: CMA blended array of states [count]	cma_sum = 0
		for i in range(0, len(inp_array)):
			cma_sum += inp_array[i]
			out_array.append(cma_sum / (i + 1))
		return out_array
	
	def blend_SMA(self, inp_array, level):
		# SMA (simple moving average) - arithmetic mean of level period
		# input:  array of states [count] , level - level of blending
		# output: SMA blended array of states [count - level + 1]
		if level > len(inp_array):
			return []
		out_array = []
		sma_sum = 0
		for i in range(level):
			sma_sum += inp_array[i]
		out_array.append(sma_sum / level)
		for i in range(level, len(inp_array)):
			sma_sum -= inp_array[i - level]
			sma_sum += inp_array[i]
			out_array.append(sma_sum / level)
		return out_array
	
	def blend_LWMA(self, inp_array, level):
		# LWMA (lienar weighted moving average)
		# input:  array of states [count] , level - level of blending
		# output: LWMA blended array of states [count - level, + 1]
		if level > len(inp_array):
			return []
		out_array = []
		lwma_sum = 0.0
		coeffs = self.get_linear_normalized_coefs(level)
		for i in range(level):
			lwma_sum += inp_array[i] * coeffs[-(i + 1)]
		out_array.append(lwma_sum)
		for i in range(level, len(inp_array)):
			lwma_sum = 0.0
			for j in range(level):
				lwma_sum += inp_array[i - j] * coeffs[j]
			out_array.append(lwma_sum)
		return out_array
	
	def blend_EMA(self, inp_array, level, alpha=-1):
		# EMA (exponentially weighted moving average)
		# input:  array of states [count], level - level of blending
		# alpha - coeff of blending (used one of level/alpha, level is primary)
		# output: EMA blended array of states [count]
		if level > len(inp_array):
			return []
		out_array = []
		out_array.append(inp_array[0])
		f_alpha = alpha
		if alpha < 0:
			f_alpha = 2 / (level + 1)
		for i in range(1, len(inp_array)):
			out_array.append(out_array[i - 1] +
			                 f_alpha * (inp_array[i] - out_array[i - 1]))
		return out_array
	
	def blend_DMA(self, inp_array, level, alpha=-1):
		# DMA (double exponentially weighted moving average)
		# input:  array of states [count], level - level of blending,
		# alpha - coeff of blending (used one of level/alpha, level is primary)
		# output: DMA blended array of states [count]
		return self.blend_EMA(self.blend_EMA(inp_array, level, alpha),
		                      level, alpha)
	
	def blend_TMA(self, inp_array, level, alpha=-1):
		# TMA (triple exponentially weighted moving average)
		# input:  array of states [count], level - level of blending,
		# alpha - coeff of blending (used one of level/alpha, level is primary)
		# output: TMA blended array of states [count]
		return self.blend_EMA(self.blend_DMA(inp_array, level, alpha),
		                      level, alpha)
	
	def MACD(self, inp_array, EMALong=26, EMAShort=12):
		# 
		# input: 
		# output: 
		if len(inp_array) < max(EMAShort, EMALong):
			return []
		out_array = []
		EMAL = self.blend_EMA(inp_array, EMALong)
		EMAS = self.blend_EMA(inp_array, EMAShort)
		for i in range(len[inp_array]):
			out_array.append(EMAS[i] - EMAL[i])
		return out_array
	
	def MACD_signal(self, inp_array, EMALong=26, EMAShort=12, EMABlend=9):
		# 
		# input: 
		# output: 
		return blend_EMA(self, self.MACD(inp_array, EMALong, EMAShort), EMABlend)
	
	def MACD_histogram(self, inp_array, EMALong=26, EMAShort=12, EMABlend=9):
		# 
		# input: 
		# output: 
		if len(inp_array) < max(EMABlend, EMAShort, EMALong):
			return []
		out_array = []
		MACD = self.MACD(inp_array, EMALong, EMAShort)
		MACD_signal = self.blend_EMA(self, MACD, EMABlend)
		for i in range(len(inp_array)):
			out_array.append(MACD[i] - MACD_signal[i])
		return out_array
