import datetime as dt
import math
from typing import Dict

import pytz


def _is_invalid_price(value: float) -> bool:
	"""Check if a price value is invalid (None, negative, NaN, or infinite)."""
	if value is None:
		return True
	if isinstance(value, float) and (math.isnan(value) or math.isinf(value)):
		return True
	if value < 0:
		return True
	return False


class OptionStrikePriceData:
	def __init__(self) -> None:
		self.callBid: float = None
		self.callAsk: float = None
		self.callDelta: float = None
		self.putBid: float = None
		self.putAsk: float = None
		self.putDelta: float = None
		self.brokerSpecific = {}  # Broker specific data
		self.lastUpdated: dt.datetime =None  # Last time the data was updated

	def getPutMidPrice(self) -> float:
		"""
		Returns the mid price of the put option.
		Treats None, negative, NaN, or infinite bid/ask values as 0.
		IB returns -1 when no bid/ask available, and may return NaN in some cases.
		"""
		bidPrice = 0 if _is_invalid_price(self.putBid) else self.putBid
		askPrice = 0 if _is_invalid_price(self.putAsk) else self.putAsk
		return (bidPrice + askPrice) / 2
	
	def getCallMidPrice(self) -> float:
		"""
		Returns the mid price of the call option.
		Treats None, negative, NaN, or infinite bid/ask values as 0.
		IB returns -1 when no bid/ask available, and may return NaN in some cases.
		"""
		bidPrice = 0 if _is_invalid_price(self.callBid) else self.callBid
		askPrice = 0 if _is_invalid_price(self.callAsk) else self.callAsk
		return (bidPrice + askPrice) / 2

	def get_call_delta(self) -> float:
		"""
		Returns the delta of the call option.
		Returns 0 if delta is None, NaN, or infinite.
		"""
		if self.callDelta is None:
			return 0
		if isinstance(self.callDelta, float) and (math.isnan(self.callDelta) or math.isinf(self.callDelta)):
			return 0
		return self.callDelta
	
	def get_put_delta(self) -> float:
		"""
		Returns the delta of the put option.
		Returns 0 if delta is None, NaN, or infinite.
		"""
		if self.putDelta is None:
			return 0
		if isinstance(self.putDelta, float) and (math.isnan(self.putDelta) or math.isinf(self.putDelta)):
			return 0
		return self.putDelta

	def is_outdated(self) -> bool:
		"""
		Returns true if the data is outdated
		"""
		if self.lastUpdated == None:
			return True
		delta = dt.datetime.now(pytz.timezone('US/Eastern')) - self.lastUpdated
		return delta.total_seconds() > 30

class OptionStrikeData:
	def __init__(self) -> None:
		self.strikeData: Dict[float, OptionStrikePriceData] = {}