
class Balance(object):
	def __init__(self, start_cap={}, fee=0):
		self.balance = start_cap
		if fee <= 1 and fee >= 0:
			self.fee = fee
	
	def set_fee(self, value):
		if value > 1 or value < 0:
			return 0
		self.fee = value
		return 1
	
	def set_balance(self, symbol, amount):
		if not isinstance(symbol, str):
			return 0
		if amount < 0:
			return 0
		self.balance[symbol] = amount
		return 1
	
	def get_balance(self, symbol):
		if not isinstance(symbol, str):
			return 0
		if not symbol in self.balance.keys():
			return 0
		return self.balance[symbol]
	
	def get_fee(self):
		return self.fee
	
	def top_up(self, symbol, amount):
		return self.set_balance(symbol, self.get_balance(symbol) + amount)
	
	def with_draw(self, symbol, amount):
		return self.set_balance(symbol, self.get_balance(symbol) - amount)
	
	def take_fee(self, symbol, amount):
		if self.fee == 0:
			return 1
		return self.set_balance(symbol,
		                        self.get_balance(symbol) - amount * self.fee)
	
	def make_trade(self, fromSymbol, toSymbol, price, firstAmount):
		if self.set_balance(fromSymbol, self.get_balance(fromSymbol) - firstAmount):
			self.top_up(toSymbol, amount / price)
			return 1
		return 0
	
	def make_trade_with_fee(self, fromSymbol, toSymbol, price, firstAmount):
		if self.get_balance(fromSymbol) - firstAmount * (1 + self.fee) < 0:
			return 0
		return self.make_trade(fromSymbol, toSymbol, price, firstAmount) or\
		       self.take_fee(fromSymbol, amount)
