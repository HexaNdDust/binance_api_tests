
class TimeSeries(object):
	def __init__(self):
		self.nothing = 0
		# Nothing here
	
	# Returnes sum of all array
	# input:  array
	# output: sum of array
	def CumulativeSum(self, inp_array):
		c_sum = 0.0
		for elem in inp_array:
			c_sum += elem
		return c_sum
	
	# Returnes array of coeffs of function y(x) = (1 - x / n) * 1 / (2 * n)
	# The feature of this function is square under the triangle equals 1, and this coeffs may be used for linear weight normalize
	# input:  len of triangle (len of array)
	# output: array of coeffs [level]
	def Get_Linear_Normalized_Coefs(self, level):
		out_array = []
		temp = 2 / level
		
		for i in range(level):
			out_array.append((1 - (i + 0.5) / level) * temp)
		return out_array
	
	# CMA (cumulative moving average) - arithmetic mean of all period
	# input:  array of states [count]
	# output: CMA blended array of states [count]
	def Blend_CMA(self, inp_array):
		out_array = []
		cma_sum = 0
		
		for i in range(0, len(inp_array)):
			cma_sum += inp_array[i]
			out_array.append(cma_sum / (i + 1))
		return out_array
	
	# SMA (simple moving average) - arithmetic mean of level period
	# input:  array of states [count] , level - level of blending
	# output: SMA blended array of states [count - level + 1]
	def Blend_SMA(self, inp_array, level):
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
	
	# 
	# input:  ...
	# output: ...
	def Blend_LWMA(self, inp_array, level):
		if level > len(inp_array):
			return []
		out_array = []
		lwma_sum = 0.0
		coeffs = self.Get_Linear_Normalized_Coefs(level)
		for i in range(level):
			lwma_sum += inp_array[i] * coeffs[-(i + 1)]
		
		out_array.append(lwma_sum)
		for i in range(level, len(inp_array)):
			lwma_sum = 0.0
			for j in range(level):
				lwma_sum += inp_array[i - j] * coeffs[j]
			out_array.append(lwma_sum)
		
		return out_array
	'''
	# 
	# input:  ...
	# output: ...
	def Blend_WMA(self, inp_array, weight_array, level):
		if level > len(inp_array):
			return []
		out_array = []
		
		return out_array
	
	# 
	# input:  ...
	# output: ...
	def Blend_WMA(self, inp_array, weight_array):
		if level > len(inp_array):
			return []
		out_array = []
		
		return out_array
	
	# 
	# input:  ...
	# output: ...
	def Blend_EMA(self, inp_array):
		out_array = []
		
		return out_array
	'''