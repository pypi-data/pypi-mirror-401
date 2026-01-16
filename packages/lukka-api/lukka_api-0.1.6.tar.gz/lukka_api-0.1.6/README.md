# Lukka API Python Client

[![Tests](https://github.com/KENOT-IO/lukka-api/workflows/Tests/badge.svg)](https://github.com/KENOT-IO/lukka-api/actions/workflows/tests.yml)
[![codecov](https://codecov.io/gh/KENOT-IO/lukka-api/branch/main/graph/badge.svg)](https://codecov.io/gh/KENOT-IO/lukka-api)
[![PyPI version](https://badge.fury.io/py/lukka-api.svg)](https://badge.fury.io/py/lukka-api)
[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A Python library for retrieving cryptocurrency data from the Lukka API. Supports pricing sources, historical prices (minute-level and daily), latest prices, and multiple output formats (JSON, CSV, Parquet).

## Requirements

- Lukka API credentials ([Sign up here](https://www.lukka.tech/))

## Installation

### Install from source
```bash
# PyPI
pip install lukka-api
pip install -i https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ lukka-api
```

## ⚙️ Configuration

### Authentication (Required)

The library supports **three methods** for providing credentials, in order of priority:

**1. Explicit Parameters (Recommended for Production)**
```python
from lukka_api import LukkaPrices

prices = LukkaPrices(
    username="your_username",
    password="your_password"
)
```

**2. Environment Variables (Recommended for 12-Factor Apps)**
```bash
# Set in shell or via container orchestration
export username='your_username'
export password='your_password'
```

```python
from lukka_api import LukkaPrices

# Credentials loaded from environment automatically
prices = LukkaPrices()
```

**3. .env File (Local Development)**

> **Important**: Create an `.env` file in **your projects directory**.

```env
LUKKA_USERNAME=your_username
LUKKA_PASSWORD=your_password
```

```python
from lukka_api import LukkaPrices

# Credentials loaded from .env file
prices = LukkaPrices()
```

## Quick Start

### Basic Usage

```python
from lukka_api import LukkaSources, LukkaPrices
from datetime import datetime, timedelta

# Initialize with explicit credentials (recommended for production)
username = ''
password = ''
sources = LukkaSources(username=username, password=password)
prices = LukkaPrices(username=username, password=password)

# Or use environment variables / .env file
sources = LukkaSources()
prices = LukkaPrices()

# Get all available pricing sources
sources.get_sources()

# Get sources for specific pairs only
sources.get_sources(pair_codes=['XBT-USD', 'ETH-USD'])

# Get sources for specific pairs with data available from a start date
sources.get_sources(pair_codes=['XBT-USD', 'ETH-USD'], start_date="2021-01-01")

# Get detailed information for a specific source, including pair_codes.
sources.get_source_details(source_id=1000)

# Get last 30 days of historical prices (uses default date range)
prices.get_historical_price(pair_codes='XBT-USD')

# Get historical prices from specific date to now
prices.get_historical_price(pair_codes='XBT-USD', from_date="2025-11-01")

# Get historical prices from beginning up to specific date
prices.get_historical_price(pair_codes='XBT-USD', to_date="2025-11-21")

# Get historical prices for specific date range
prices.get_historical_price(pair_codes='XBT-USD', from_date="2025-11-01", to_date="2025-11-21")

# Get latest price within last hour (default lookback)
prices.get_latest_price(pair_codes='XBT-USD')
```