"""
Live trade streaming via WebSocket.

This module provides real-time trade event streaming by subscribing
to Swap, Mint, and Burn events from the VAMMManager contract via
a WebSocket RPC connection.
"""

import asyncio
import logging
import threading
from typing import Callable, Optional, Set

from web3 import Web3
from web3.middleware import ExtraDataToPOAMiddleware

from xccy.types import TradeEvent


logger = logging.getLogger(__name__)


# Event signatures (keccak256)
SWAP_TOPIC = Web3.keccak(
    text="Swap(bytes32,address,uint96,address,int24,int24,uint256,int256,int256,int24,uint160)"
).hex()
MINT_TOPIC = Web3.keccak(
    text="Mint(bytes32,address,uint96,address,int24,int24,uint128)"
).hex()
BURN_TOPIC = Web3.keccak(
    text="Burn(bytes32,address,uint96,address,int24,int24,uint128)"
).hex()

EVENT_TOPICS = {
    SWAP_TOPIC: "Swap",
    MINT_TOPIC: "Mint",
    BURN_TOPIC: "Burn",
}


class TradeStream:
    """
    Live trade event stream using WebSocket RPC.
    
    Subscribes to Swap, Mint, and Burn events from the VAMMManager contract
    and delivers them to registered callbacks in real-time.
    
    Args:
        ws_rpc_url: WebSocket RPC URL (e.g., wss://polygon-mainnet.g.alchemy.com/v2/KEY).
        vamm_address: VAMMManager contract address.
        
    Example:
        >>> def on_trade(event: TradeEvent):
        ...     print(f"New {event.event_type}: {event.tx_hash}")
        >>> 
        >>> stream = TradeStream(ws_url, vamm_address)
        >>> stream.subscribe(on_trade, event_types=["Swap"])
        >>> stream.start()  # Blocking
        
        >>> # Or async:
        >>> async def main():
        ...     stream.subscribe(on_trade)
        ...     await stream.start_async()
    """
    
    def __init__(self, ws_rpc_url: str, vamm_address: str) -> None:
        """Initialize the trade stream."""
        self._ws_url = ws_rpc_url
        self._vamm_address = Web3.to_checksum_address(vamm_address)
        # Callbacks: (callback, pool_id, user_address, event_types)
        self._callbacks: list[tuple[
            Callable[[TradeEvent], None],
            Optional[str],  # pool_id
            Optional[str],  # user_address
            Optional[Set[str]],  # event_types
        ]] = []
        self._running = False
        self._stop_event: Optional[asyncio.Event] = None
        self._web3: Optional[Web3] = None
        self._thread: Optional[threading.Thread] = None
    
    def subscribe(
        self,
        callback: Callable[[TradeEvent], None],
        pool_id: Optional[str] = None,
        user_address: Optional[str] = None,
        event_types: Optional[list[str]] = None,
    ) -> None:
        """
        Add a subscription for trade events.
        
        Args:
            callback: Function to call with each TradeEvent.
            pool_id: Optional filter by pool ID (hex string).
                     If None, receives events from all pools.
            user_address: Optional filter by user/owner address.
                         If None, receives events from all users.
            event_types: Optional filter by event types (["Swap", "Mint", "Burn"]).
                        If None, receives all event types.
                        
        Example:
            >>> # All events
            >>> stream.subscribe(on_event)
            >>> 
            >>> # Only swaps in a specific pool
            >>> stream.subscribe(on_swap, pool_id="0x...", event_types=["Swap"])
            >>> 
            >>> # Only my trades
            >>> stream.subscribe(on_my_trade, user_address="0x...")
            >>> 
            >>> # My trades in a specific pool
            >>> stream.subscribe(on_trade, pool_id="0x...", user_address="0x...")
        """
        types_set = set(event_types) if event_types else None
        user_addr = user_address.lower() if user_address else None
        self._callbacks.append((callback, pool_id, user_addr, types_set))
    
    def unsubscribe(self, callback: Callable[[TradeEvent], None]) -> None:
        """
        Remove a subscription.
        
        Args:
            callback: The callback to remove.
        """
        self._callbacks = [
            (cb, pid, user, types) for cb, pid, user, types in self._callbacks
            if cb != callback
        ]
    
    def _parse_swap_event(self, log: dict) -> TradeEvent:
        """Parse a Swap event log."""
        topics = log["topics"]
        data = log["data"]
        
        # Indexed: poolId (topic[1]), owner (topic[2]), accountId (topic[3])
        pool_id = topics[1].hex() if hasattr(topics[1], "hex") else topics[1]
        owner = "0x" + topics[2].hex()[-40:] if hasattr(topics[2], "hex") else "0x" + topics[2][-40:]
        
        # Decode non-indexed data
        # isolatedMarginToken, tickLower, tickUpper, cumulativeFeeIncurred,
        # fixedTokenDelta, variableTokenDelta, currentTick, sqrtPriceX96
        data_bytes = bytes.fromhex(data[2:]) if isinstance(data, str) else data
        
        # ABI decode the data
        from eth_abi import decode
        decoded = decode(
            ["address", "int24", "int24", "uint256", "int256", "int256", "int24", "uint160"],
            data_bytes
        )
        
        isolated_margin_token, tick_lower, tick_upper, fee, fixed_delta, variable_delta, _, _ = decoded
        
        return TradeEvent(
            event_type="Swap",
            pool_id=pool_id,
            sender=owner,
            block_number=log["blockNumber"],
            tx_hash=log["transactionHash"].hex() if hasattr(log["transactionHash"], "hex") else log["transactionHash"],
            log_index=log.get("logIndex", 0),
            fixed_token_delta=fixed_delta,
            variable_token_delta=variable_delta,
            fee_incurred=fee,
            tick_lower=tick_lower,
            tick_upper=tick_upper,
        )
    
    def _parse_mint_burn_event(self, log: dict, event_type: str) -> TradeEvent:
        """Parse a Mint or Burn event log."""
        topics = log["topics"]
        data = log["data"]
        
        # Indexed: poolId, owner, accountId
        pool_id = topics[1].hex() if hasattr(topics[1], "hex") else topics[1]
        owner = "0x" + topics[2].hex()[-40:] if hasattr(topics[2], "hex") else "0x" + topics[2][-40:]
        
        # Decode non-indexed: isolatedMarginToken, tickLower, tickUpper, amount
        data_bytes = bytes.fromhex(data[2:]) if isinstance(data, str) else data
        
        from eth_abi import decode
        decoded = decode(
            ["address", "int24", "int24", "uint128"],
            data_bytes
        )
        
        _, tick_lower, tick_upper, amount = decoded
        
        return TradeEvent(
            event_type=event_type,
            pool_id=pool_id,
            sender=owner,
            block_number=log["blockNumber"],
            tx_hash=log["transactionHash"].hex() if hasattr(log["transactionHash"], "hex") else log["transactionHash"],
            log_index=log.get("logIndex", 0),
            amount=amount,
            tick_lower=tick_lower,
            tick_upper=tick_upper,
        )
    
    def _parse_event(self, log: dict) -> Optional[TradeEvent]:
        """Parse a log entry into a TradeEvent."""
        try:
            topics = log.get("topics", [])
            if not topics:
                return None
            
            topic0 = topics[0].hex() if hasattr(topics[0], "hex") else topics[0]
            
            if topic0 == SWAP_TOPIC:
                return self._parse_swap_event(log)
            elif topic0 == MINT_TOPIC:
                return self._parse_mint_burn_event(log, "Mint")
            elif topic0 == BURN_TOPIC:
                return self._parse_mint_burn_event(log, "Burn")
            
            return None
        except Exception as e:
            logger.warning(f"Failed to parse event: {e}")
            return None
    
    def _dispatch_event(self, event: TradeEvent) -> None:
        """Dispatch event to matching callbacks."""
        for callback, pool_id_filter, user_filter, types_filter in self._callbacks:
            # Check pool filter
            if pool_id_filter and event.pool_id != pool_id_filter:
                continue
            
            # Check user filter (case-insensitive)
            if user_filter and event.sender.lower() != user_filter:
                continue
            
            # Check type filter
            if types_filter and event.event_type not in types_filter:
                continue
            
            try:
                callback(event)
            except Exception as e:
                logger.error(f"Callback error: {e}")
    
    async def start_async(self) -> None:
        """
        Start listening for events (async version).
        
        Blocks until stop() is called or connection is lost.
        
        Example:
            >>> async def main():
            ...     stream.subscribe(on_event)
            ...     await stream.start_async()
        """
        from web3 import AsyncWeb3
        from web3.providers import WebSocketProvider
        
        self._running = True
        self._stop_event = asyncio.Event()
        
        logger.info(f"Connecting to {self._ws_url}...")
        
        async with AsyncWeb3(WebSocketProvider(self._ws_url)) as w3:
            # Add PoA middleware
            w3.middleware_onion.inject(ExtraDataToPOAMiddleware, layer=0)
            
            # Build filter
            filter_params = {
                "address": self._vamm_address,
                "topics": [[SWAP_TOPIC, MINT_TOPIC, BURN_TOPIC]],
            }
            
            # Create subscription
            subscription_id = await w3.eth.subscribe("logs", filter_params)
            logger.info(f"Subscribed with ID: {subscription_id}")
            
            try:
                async for response in w3.socket.process_subscriptions():
                    if self._stop_event.is_set():
                        break
                    
                    # Parse and dispatch
                    result = response.get("result")
                    if result:
                        event = self._parse_event(result)
                        if event:
                            self._dispatch_event(event)
            except asyncio.CancelledError:
                logger.info("Stream cancelled")
            finally:
                await w3.eth.unsubscribe(subscription_id)
                self._running = False
    
    def start(self) -> None:
        """
        Start listening for events (blocking).
        
        Runs the async event loop in the current thread.
        Call stop() from another thread to stop.
        
        Example:
            >>> stream.subscribe(on_event)
            >>> stream.start()  # Blocks forever
        """
        asyncio.run(self.start_async())
    
    def start_background(self) -> None:
        """
        Start listening in a background thread.
        
        Non-blocking. Use stop() to terminate.
        
        Example:
            >>> stream.subscribe(on_event)
            >>> stream.start_background()
            >>> # ... do other work ...
            >>> stream.stop()
        """
        def run():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                loop.run_until_complete(self.start_async())
            finally:
                loop.close()
        
        self._thread = threading.Thread(target=run, daemon=True)
        self._thread.start()
    
    def stop(self) -> None:
        """
        Stop listening for events.
        
        Safe to call from any thread.
        """
        self._running = False
        if self._stop_event:
            self._stop_event.set()
        
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=5.0)
    
    @property
    def is_running(self) -> bool:
        """True if stream is currently running."""
        return self._running
