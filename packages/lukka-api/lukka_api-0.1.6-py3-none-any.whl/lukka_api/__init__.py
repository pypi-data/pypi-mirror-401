"""
Lukka API Python Client Library

A Python library for retrieving cryptocurrency data from the Lukka API,
with built-in distributed token caching and comprehensive data export capabilities.

Example usage:
    >>> from lukka_api import LukkaSources, LukkaPrices
    >>>
    >>> # Get pricing sources
    >>> sources = LukkaSources()
    >>> all_sources = sources.get_sources()
    >>>
    >>> # Get historical prices
    >>> prices = LukkaPrices()
    >>> data = prices.get_historical_price(
    ...     source_id=1000,
    ...     pair="XBT-USD",
    ...     from_date="2024-01-01T00:00:00Z",
    ...     to_date="2024-12-31T23:59:59Z"
    ... )
"""

__version__ = "0.1.6"
__author__ = "KENOT-IO"
__license__ = "MIT"

# Import main classes for easy access
from .sources import LukkaSources
from .prices import LukkaPrices
from .write import WriteData
from .distributed_lukka_api import DistributedLukkaAPIClient

# Define public API
__all__ = [
    "LukkaSources",
    "LukkaPrices",
    "WriteData",
    "DistributedLukkaAPIClient",
]
