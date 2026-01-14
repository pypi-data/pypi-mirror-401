from abc import ABC, abstractmethod
from typing import Callable, Any, List
from ..models.enums import MarketType

class WSBaseAdapter(ABC):
    """Abstract base class for Websocket/Streaming adapters."""

    @abstractmethod
    async def subscribe(self, symbols: List[str], callback: Callable[[dict], Any]) -> None:
        """
        Subscribe to live price updates for a list of symbols.
        
        Args:
            symbols: List of exchange-specific symbols.
            callback: Async or sync function to call with update data. 
                      Data format should be consistent if possible, 
                      or raw if specified.
        """
        pass

    @abstractmethod
    def get_exchange_symbol(self, ticker: str, market_type: MarketType | str) -> str:
        """Convert standard ticker to exchange-specific symbol."""
        pass
