# Fragment Stars API

Python SDK for purchasing Telegram Stars and Premium via Fragment API.

## Installation

```bash
pip install fragment-stars-api
```

## Quick Start

```python
from fragment_api import FragmentAPIClient

client = FragmentAPIClient()

# Buy 50 stars (no KYC mode)
result = client.buy_stars("username", 50, seed="your_seed_base64")
print(f"Success: {result.success}")

# Buy 3 months premium
result = client.buy_premium("username", 3, seed="your_seed_base64")

# With KYC (lower commission)
result = client.buy_stars("username", 50, seed="...", cookies="cookies_base64")
```

## Custom Server

```python
client = FragmentAPIClient(base_url="https://your-server.com:8443")
```

## Commission Rates

```python
rates = client.get_rates()
print(f"No KYC: {rates.rate_no_kyc}%")
print(f"With KYC: {rates.rate_with_kyc}%")
```

## API Reference

### `FragmentAPIClient(base_url, timeout, poll_timeout)`

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `base_url` | str | `https://fragment-api.ydns.eu:8443` | API URL |
| `timeout` | float | 30.0 | Request timeout (seconds) |
| `poll_timeout` | float | 300.0 | Max wait for queue (seconds) |

### `buy_stars(username, amount, seed, cookies=None, wait=True)`

Buy Telegram Stars.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `username` | str | Yes | Telegram username |
| `amount` | int | Yes | Number of stars |
| `seed` | str | Yes | Wallet seed (base64) |
| `cookies` | str | No | Fragment cookies (base64) for KYC mode |
| `wait` | bool | No | Wait for result (default: True) |

### `buy_premium(username, duration, seed, cookies=None, wait=True)`

Buy Telegram Premium.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `username` | str | Yes | Telegram username |
| `duration` | int | Yes | Months (3, 6, or 12) |
| `seed` | str | Yes | Wallet seed (base64) |
| `cookies` | str | No | Fragment cookies (base64) for KYC mode |
| `wait` | bool | No | Wait for result (default: True) |

### `get_rates()`

Get commission rates. Returns `CommissionRatesResponse`.

### `get_status(request_id)`

Get request status. Returns `QueuedRequest`.

## Exceptions

```python
from fragment_api import FragmentAPIError, QueueTimeoutError

try:
    result = client.buy_stars("username", 50, seed="...")
except QueueTimeoutError:
    print("Request timed out")
except FragmentAPIError as e:
    print(f"Error: {e.error_code} - {e.message}")
```

## License

MIT
