# Trade Tracking

The SDK provides two methods for tracking trades:

1. **Historical trades** via backend API
2. **Live streaming** via WebSocket RPC

## Historical Trades

Query past trades from the indexed backend API.

### Get Pool Trades

```python
from xccy import XccyClient

client = XccyClient(
    rpc_url="https://polygon-rpc.com",
    backend_url="https://api.xccy.finance",
)

# Get recent trades for a pool
trades, cursor = client.trades.get_pool_trades(
    pool_id="0x...",
    limit=50,
)

for trade in trades:
    print(f"{trade.timestamp}: {trade.notional} @ {trade.fixed_rate:.2%}")
    print(f"  Trader: {trade.trader}")
    print(f"  Type: {'Fixed Taker' if trade.is_fixed_taker else 'Variable Taker'}")
```

### Filter by User

```python
# Get trades for a specific user
my_trades = client.trades.get_user_trades(
    pool_id="0x...",
    user_address="0x...",
    limit=100,
)

total_volume = sum(t.notional for t in my_trades)
print(f"My total volume: {total_volume}")
```

### Pagination

```python
# Fetch all trades with pagination
all_trades = []
cursor = None

while True:
    trades, cursor = client.trades.get_pool_trades(
        pool_id="0x...",
        cursor=cursor,
        limit=200,
    )
    all_trades.extend(trades)
    
    if not cursor:
        break

print(f"Total trades: {len(all_trades)}")
```

Or use the convenience method:

```python
all_trades = client.trades.get_all_pool_trades(
    pool_id="0x...",
    max_trades=1000,
)
```

## Live Streaming

Subscribe to real-time trade events via WebSocket.

### Setup

```python
import os
from xccy import XccyClient

client = XccyClient(
    rpc_url=os.getenv("POLYGON_RPC"),
    ws_rpc_url=os.getenv("WS_POLYGON_RPC"),  # wss://...
)
```

### Subscribe to Events

```python
from xccy import TradeEvent

def on_trade(event: TradeEvent):
    print(f"New {event.event_type}!")
    print(f"  Pool: {event.pool_id[:16]}...")
    print(f"  TX: {event.tx_hash}")
    print(f"  Block: {event.block_number}")
    
    if event.event_type == "Swap":
        print(f"  Fixed delta: {event.fixed_token_delta}")
        print(f"  Variable delta: {event.variable_token_delta}")
    elif event.event_type in ("Mint", "Burn"):
        print(f"  Amount: {event.amount}")

# Subscribe to all events
client.stream.subscribe(on_trade)

# Or filter by event type
client.stream.subscribe(on_trade, event_types=["Swap"])

# Or filter by pool
client.stream.subscribe(on_trade, pool_id="0x...")
```

### Start Listening

**Blocking mode:**

```python
client.stream.start()  # Blocks forever
```

**Async mode:**

```python
import asyncio

async def main():
    client.stream.subscribe(on_trade)
    await client.stream.start_async()

asyncio.run(main())
```

**Background mode:**

```python
client.stream.start_background()

# ... do other work ...

client.stream.stop()
```

### Event Types

| Event | Description | Key Fields |
|-------|-------------|------------|
| `Swap` | Trader swap | `fixed_token_delta`, `variable_token_delta`, `fee_incurred` |
| `Mint` | LP adds liquidity | `amount`, `tick_lower`, `tick_upper` |
| `Burn` | LP removes liquidity | `amount`, `tick_lower`, `tick_upper` |

### TradeEvent Fields

```python
@dataclass
class TradeEvent:
    event_type: str      # "Swap", "Mint", "Burn"
    pool_id: str         # Pool identifier
    sender: str          # Transaction sender
    block_number: int    # Block number
    tx_hash: str         # Transaction hash
    log_index: int       # Log index
    timestamp: int       # Block timestamp (if available)
    
    # Swap-specific
    fixed_token_delta: int
    variable_token_delta: int
    fee_incurred: int
    
    # Mint/Burn-specific
    amount: int          # Liquidity amount
    tick_lower: int
    tick_upper: int
```

## Example: Trade Monitor

```python
import os
import asyncio
from decimal import Decimal
from xccy import XccyClient, TradeEvent, format_amount

client = XccyClient(
    rpc_url=os.getenv("POLYGON_RPC"),
    ws_rpc_url=os.getenv("WS_POLYGON_RPC"),
    backend_url="https://api.xccy.finance",
)

def on_swap(event: TradeEvent):
    notional = format_amount(abs(event.variable_token_delta), "USDC")
    direction = "Fixed Taker" if event.variable_token_delta > 0 else "Variable Taker"
    print(f"[SWAP] {notional} USDC ({direction})")
    print(f"       TX: {event.tx_hash}")

def on_lp(event: TradeEvent):
    action = "Added" if event.event_type == "Mint" else "Removed"
    print(f"[LP] {action} liquidity: {event.amount}")
    print(f"     Range: [{event.tick_lower}, {event.tick_upper}]")

# Subscribe to events
client.stream.subscribe(on_swap, event_types=["Swap"])
client.stream.subscribe(on_lp, event_types=["Mint", "Burn"])

print("Listening for trades...")
client.stream.start()
```

## WebSocket Providers

The SDK works with any WebSocket RPC provider:

| Provider | URL Format |
|----------|------------|
| Alchemy | `wss://polygon-mainnet.g.alchemy.com/v2/KEY` |
| Infura | `wss://polygon-mainnet.infura.io/ws/v3/KEY` |
| QuickNode | `wss://xxx.polygon.quiknode.pro/KEY` |

Store your WebSocket URL in `.env`:

```bash
WS_POLYGON_RPC=wss://polygon-mainnet.g.alchemy.com/v2/your-api-key
```
