"""
This module contains custom exceptions related to trade operations.

OTB-269: Entry retry mechanism - Distinguishes between retryable and fatal trade errors.
"""


class TradeException(Exception):
    """
    Base class for all trade-related exceptions.
    """
    def __init__(self, reason: str, *args):
        """
        Initialize the exception with a reason.

        Args:
            reason: Reason why the trade operation failed
            args: Additional arguments to pass to the base Exception class
        """
        super().__init__(reason, *args)
        self.reason = reason

    def __str__(self):
        return f"Trade operation failed: {self.reason}"


class RetryableTradeException(TradeException):
    """
    Exception raised when a trade operation fails but can be retried.
    
    Examples of retryable failures:
    - Minimum premium not met
    - Maximum premium exceeded
    - Max entry adjustments reached
    - No suitable strikes found (market conditions may change)
    - Adjusted price crosses zero
    """
    def __init__(self, reason: str, *args):
        super().__init__(reason, *args)

    def __str__(self):
        return f"Trade failed (retryable): {self.reason}"


class FatalTradeException(TradeException):
    """
    Exception raised when a trade operation fails and should NOT be retried.
    
    Examples of fatal failures:
    - No broker connection
    - Trading disabled
    - No Hub connection (subscription issue)
    - Maximum open trades reached
    - Template conditions not met (e.g., VIX out of range)
    """
    def __init__(self, reason: str, *args):
        super().__init__(reason, *args)

    def __str__(self):
        return f"Trade failed (fatal): {self.reason}"
