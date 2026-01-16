
import asyncio
import copy
import datetime
from typing import List, Optional, Callable, Awaitable

from optrabot.broker.order import (Execution, Leg, OptionRight, Order,
                                   OrderAction)
from optrabot.deltaadjuster import DeltaAdjuster
from optrabot.models import Trade
from optrabot.stoplossadjuster import StopLossAdjuster
from optrabot.tradestatus import TradeStatus
from optrabot.tradetemplate.templatefactory import Template


class EntryResult:
	"""
	OTB-269: Represents the result of an entry order attempt.
	Used to communicate the outcome of entry order tracking back to the caller.
	"""
	def __init__(self, success: bool, reason: str = '', retryable: bool = False):
		self.success = success
		self.reason = reason
		self.retryable = retryable  # If True, the caller may retry the entry

	def __repr__(self):
		return f"EntryResult(success={self.success}, reason='{self.reason}', retryable={self.retryable})"


class ManagedTrade:
	"""
	ManagedTrade is representing a trade which is currently managed by the TradeManager.
	"""
	adjustment_orders: List[Order]

	def __init__(self, trade: Trade, template: Template, entryOrder: Order, account: str = ''): 
		self.trade = trade
		self.entryOrder = entryOrder
		self.template = template
		self.account = account
		self.takeProfitOrder: Order = None
		self.stopLossOrder: Order = None
		self.closing_order: Order = None
		self.status = TradeStatus.NEW
		self.realizedPNL = 0.0
		self.transactions = []
		self.expired = False
		self.entry_price = None					# Holds the entry price for the trade
		self.current_price: float = None		# Holds the current price of the trade
		self.current_delta: float = None		# Holds the current delta of the position
		self.current_legs: List[Leg] = []		# Holds the current legs of the trade (filled after entry order is excuted)
		self.stoploss_adjusters: List[StopLossAdjuster] = []
		self.delta_adjusters: List[DeltaAdjuster] = []
		self.long_legs_removed = False			# will be set to true for credit_trades if the long legs are no longer available
		self.adjustment_orders = []				# Holds orders which are created by delta adjusters
		self.entry_adjustment_count = 0			# Tracks the number of entry order price adjustments
		self.excluded_closing_legs: List[Leg] = []  # Legs excluded from closing order (no bid price)
		# OTB-269: Entry completion tracking for retry mechanism
		self._entry_result: Optional[EntryResult] = None
		self._entry_complete_event: asyncio.Event = asyncio.Event()
		self._entry_result_callback: Optional[Callable[[EntryResult], Awaitable[None]]] = None

	def set_entry_result_callback(self, callback: Callable[['EntryResult'], Awaitable[None]]) -> None:
		"""
		OTB-269: Set a callback to be invoked when entry completes (success or failure).
		"""
		self._entry_result_callback = callback

	async def signal_entry_complete(self, result: EntryResult) -> None:
		"""
		OTB-269: Signal that entry order processing is complete.
		Called by TradeManager when entry is filled or cancelled.
		
		Note: This method handles multiple calls gracefully - only the first
		call will set the result and trigger the callback.
		"""
		# Ignore duplicate signals - first signal wins
		if self._entry_complete_event.is_set():
			return
		
		self._entry_result = result
		self._entry_complete_event.set()
		if self._entry_result_callback:
			await self._entry_result_callback(result)

	async def wait_for_entry_complete(self, timeout: float = None) -> Optional[EntryResult]:
		"""
		OTB-269: Wait for entry order processing to complete.
		Returns the EntryResult or None if timeout occurs.
		"""
		try:
			if timeout:
				await asyncio.wait_for(self._entry_complete_event.wait(), timeout=timeout)
			else:
				await self._entry_complete_event.wait()
			return self._entry_result
		except asyncio.TimeoutError:
			return None

	def isActive(self) -> bool:
		"""
		Returns True if the trade is active
		"""
		return self.status == TradeStatus.OPEN
	
	def setup_stoploss_adjusters(self):
		""" 
		Copies the stop loss adjusters from the template to the managed trade and sets the
		base price for earch of the adjusters
		"""
		for adjuster in self.template.get_stoploss_adjusters():
			adjuster_copy = copy.copy(adjuster)
			adjuster_copy.setBasePrice(self.entry_price)
			self.stoploss_adjusters.append(adjuster_copy)

	def setup_delta_adjusters(self):
		"""
		Copies the delta adjusters from the template to the managed trade
		"""
		for adjuster in self.template.get_delta_adjusters():
			adjuster_copy = copy.copy(adjuster)
			self.delta_adjusters.append(adjuster_copy)

	def update_current_legs(self, adjustment_order: Order):
		"""
		Updates the current legs of the trade from the execution of the adjustment order.
		"""
		for leg in adjustment_order.legs:
			opposite_action = OrderAction.SELL if leg.action == OrderAction.BUY else OrderAction.BUY
			existing_leg = next((l for l in self.current_legs if l.strike == leg.strike and l.right == leg.right and l.action != opposite_action), None)
			if existing_leg:
				# If an existing leg was found, remove it from the current legs, because it has been closed
				self.current_legs.remove(existing_leg)
			else:
				# Otherwise it is a new leg added by execution of the adjustment order
				self.current_legs.append(copy.copy(leg))

	def get_expiration_date(self) -> datetime:
		"""
		Returns the expiration date of the trade based on the legs of the entry order.
		Assumes all legs have the same expiration date.
		"""
		if self.current_legs and len(self.current_legs) > 0:
			return self.current_legs[0].expiration
		return None