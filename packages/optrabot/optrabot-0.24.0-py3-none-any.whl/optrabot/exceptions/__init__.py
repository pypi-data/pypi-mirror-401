"""
Package for custom exceptions used throughout the OptraBot application
"""

from optrabot.exceptions.orderexceptions import OrderException, PlaceOrderException, PrepareOrderException
from optrabot.exceptions.tradeexceptions import TradeException, RetryableTradeException, FatalTradeException

__all__ = [
    'OrderException', 
    'PlaceOrderException', 
    'PrepareOrderException',
    'TradeException',
    'RetryableTradeException',
    'FatalTradeException'
]