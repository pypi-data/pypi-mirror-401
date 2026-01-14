import asyncio
import os
from typing import Callable, Any, List, Dict
from tqsdk import TqApi, TqAuth
from .base import WSBaseAdapter
from ..models.enums import MarketType
from ..utils import get_logger

logger = get_logger("tqsdk_adapter")

class TQSDKAdapter(WSBaseAdapter):
    def __init__(self):
        self._api: TqApi | None = None
        self._quotes = {} 
        self._callbacks: Dict[str, List[Callable]] = {}
        self._running = False
        self._task = None
        self._lock = asyncio.Lock()

    def _ensure_api(self):
        if not self._api:
            tq_user = os.getenv("TQ_USER", "mobile-number")
            tq_pass = os.getenv("TQ_PASS", "password")
            
            # Warn if credentials missing?
            if not tq_user or tq_user == "mobile-number":
                logger.warning("TQ_USER/TQ_PASS not set. TQSDK might fail.")
                
            auth = TqAuth(tq_user, tq_pass)
            self._api = TqApi(auth=auth)

    async def _loop(self):
        """Main loop to wait for data updates."""
        try:
            logger.info("Starting TQSDK loop")
            async with self._api:
                while self._running:
                    await self._api.wait_update()
                    
                    # Check for updates
                    for symbol, quote in self._quotes.items():
                        if self._api.is_changing(quote):
                            # Extract useful fields
                            # Note: TQSDK quote objects use nan for missing values.
                            data = {
                                "symbol": symbol,
                                "last_price": quote.last_price,
                                "bid_price1": quote.bid_price1,
                                "ask_price1": quote.ask_price1,
                                "volume": quote.volume,
                                "open_interest": quote.open_interest,
                                "ts": quote.datetime, # TQSDK uses string or float? Usually nanoseconds?
                                # quote.datetime is string in standard TQSDK? "2018-01-01 10:00:00.000000"
                                # need to check. Documentation says: "2017-07-26 23:04:21.000001" (str)
                            }
                            
                            cbs = self._callbacks.get(symbol, [])
                            for cb in cbs:
                                if asyncio.iscoroutinefunction(cb):
                                    await cb(data)
                                else:
                                    cb(data)
        except Exception as e:
            logger.error(f"TQSDK Loop Error: {e}")
            self._running = False

    async def subscribe(self, symbols: List[str], callback: Callable[[dict], Any]) -> None:
        async with self._lock:
            self._ensure_api()
            
            new_syms = []
            for s in symbols:
                if s not in self._quotes:
                    # Get quote object
                    try:
                        self._quotes[s] = self._api.get_quote(s)
                        new_syms.append(s)
                    except Exception as e:
                        logger.error(f"Failed to get quote for {s}: {e}")
                        continue
                
                if s not in self._callbacks:
                    self._callbacks[s] = []
                self._callbacks[s].append(callback)
            
            if new_syms:
                logger.info(f"Subscribed to new symbols: {new_syms}")

            # Start loop if not running
            if not self._running:
                self._running = True
                self._task = asyncio.create_task(self._loop())

    def get_exchange_symbol(self, ticker: str, market_type: MarketType | str) -> str:
        # Simple heuristics or passthrough
        # If user passes generic "RB", we might default to "SHFE.rb" ?
        # But we don't know correct suffix/prefix easily.
        # Support "KQ.m@SHFE.rb" style
        
        # If it contains dots, assume it's correct TQSDK format
        if "." in ticker:
            return ticker
            
        # If input is like "RB=F" (Yahoo), TQSDK main contract is usually "KQ.m@<EX>.<prod>"
        # Assuming SHFE for now for RB?
        # This is risky. Better to return ticker and let caller ensure valid TQSDK symbol.
        return ticker
