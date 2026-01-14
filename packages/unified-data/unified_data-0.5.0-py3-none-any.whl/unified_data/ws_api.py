from typing import Callable, Any
from .models.enums import MarketType, Exchange
from .utils import get_logger

logger = get_logger("ws_api")

# Global adapter cache
_ADAPTERS = {}

def _get_ws_adapter(exchange: str | None):
    """
    Factory to get the correct WS adapter instance.
    Currently defaults to TQSDK for futures, or if specified.
    """
    # Logic to select adapter. 
    # If exchange is explicitly TQSDK, use it.
    # If exchange is SHFE/DCE/CZCE, probably TQSDK for now?
    # Or matches current api.py logic? 
    # Current api.py defaults YFinance for futures. 
    # But we want to support TQSDK for this new feature.
    
    target_exchange = exchange
    
    if exchange == Exchange.TQSDK:
        pass # Correct
    elif exchange in ["SHFE", "DCE", "CZCE", "CFFEX", "INE"]:
         # Implicitly TQSDK for Chinese futures?
         target_exchange = Exchange.TQSDK
    elif exchange is None:
        # Fallback?
        # If market_type is futures, maybe default to TQSDK if configured?
        # For safety, let's require exchange="tqsdk" or specific chinese exchanges for now
        # unless we want to override default behavior.
        # Let's default to TQSDK if we are testing this feature.
        # But `api.py` uses YFinance.
        # I'll stick to explicit or mapped exchanges.
        pass

    if target_exchange == Exchange.TQSDK:
        if Exchange.TQSDK not in _ADAPTERS:
             from .ws_adapters.tqsdk_adapter import TQSDKAdapter
             _ADAPTERS[Exchange.TQSDK] = TQSDKAdapter()
        return _ADAPTERS[Exchange.TQSDK], Exchange.TQSDK
        
    raise ValueError(f"Unsupported WS exchange: {exchange}")

async def sub_live_price(
    ticker: str,
    market_type: str,
    exchange: str | None = None,
    callback: Callable[[dict], Any] | None = None
) -> None:
    """
    Subscribe to live price updates.
    
    Args:
        ticker: Standard symbol (e.g. "SHFE.rb2501").
        market_type: Market type (e.g. "futures").
        exchange: Exchange name (e.g. "tqsdk").
        callback: Function to call on update.
    """
    if callback is None:
        raise ValueError("Callback must be provided")

    logger.info(f"Subscribing to {ticker} ({market_type}) on {exchange}")
    
    try:
        adapter, exchange_name = _get_ws_adapter(exchange)
        
        # Convert symbol
        sym = adapter.get_exchange_symbol(ticker, market_type)
        
        await adapter.subscribe([sym], callback)
        
    except Exception as e:
        logger.error(f"Failed to subscribe: {e}")
        raise
