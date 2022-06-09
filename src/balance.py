
class Balance(object):
	def __init__(self, start_cap = {}, fee = 0):
		self.balance = start_cap
		if fee <= 1 and fee >= 0:
			self.fee = fee
	
	
	def setFee(value):
		if value > 1 or value < 0:
			return 0
		self.fee = value
		return 1
	
	
	def setBalance(symbol, amount):
		if not isinstance(symbol, str):
			return 0
		if amount < 0:
			return 0
		self.balance[symbol] = amount
		return 1
		
	
	def getBalance(symbol):
		if not isinstance(symbol, str):
			return 0
		if not symbol in self.balance.keys():
			return 0
		
		return self.balance[symbol]
	
	def getFee():
		return self.fee
	
	
	def topUp(symbol, amount):
		return self.setBalance(symbol, self.getBalance(symbol) + amount)
	
	
	def withDraw(symbol, amount):
		return self.setBalance(symbol, self.getBalance(symbol) - amount)
	
	
	def takeFee(symbol, amount):
		if self.fee == 0:
			return 1
		return self.setBalance(symbol, self.getBalance(symbol) - amount * self.fee)
	
	
	def makeTrade(fromSymbol, toSymbol, price, firstAmount):
		if self.setBalance(fromSymbol, self.getBalance(fromSymbol) - firstAmount):
			self.topUp(toSymbol, amount / price)
			return 1
		return 0
	
	
	def makeTradeWithFee(fromSymbol, toSymbol, price, firstAmount):
		if self.getBalance(fromSymbol) - firstAmount * (1 + self.fee) < 0:
			return 0
		return makeTrade(fromSymbol, toSymbol, price, firstAmount) or takeFee(fromSymbol, amount)
