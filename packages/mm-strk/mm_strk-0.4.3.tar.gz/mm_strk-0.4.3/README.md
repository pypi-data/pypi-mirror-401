# mm-strk

Starknet utilities library.

**Requires RPC node version 0.9+**

## Installation

```bash
pip install mm-strk
```

## API

### is_address

Validates a Starknet address.

```python
from mm_strk.account import is_address

is_address("0x123abc")  # True - minimal form
is_address("0x0000000000000000000000000000000000000000000000000000000000123abc")  # True - full 64-char form
is_address("invalid")  # False
```

### get_balance

Queries token balance for an address.

```python
import asyncio
from mm_strk.balance import get_balance, ETH_ADDRESS_MAINNET, STRK_ADDRESS_MAINNET

result = asyncio.run(get_balance(
    rpc_url="https://your-rpc-node.com",
    address="0x123...",
    token=ETH_ADDRESS_MAINNET,
))
if result.is_ok():
    print(result.ok)  # balance in wei
```

Token constants:
- `ETH_ADDRESS_MAINNET`, `ETH_DECIMALS` (18)
- `STRK_ADDRESS_MAINNET`, `STRK_DECIMALS` (18)
- `USDC_ADDRESS_MAINNET`, `USDC_DECIMALS` (6)
- `USDT_ADDRESS_MAINNET`, `USDT_DECIMALS` (6)
- `DAI_ADDRESS_MAINNET`, `DAI_DECIMALS` (18)

### address_to_domain

Resolves a Starknet address to its Starknet ID domain.

```python
import asyncio
from mm_strk.domain import address_to_domain

result = asyncio.run(address_to_domain("0x123..."))
if result.is_ok():
    print(result.ok)  # "example.stark" or None if not found
```

## CLI

### mm-strk node

Check status of Starknet RPC nodes.

```bash
mm-strk node https://rpc-node-1.com https://rpc-node-2.com
```
