# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.5] - 2025-11-21

### Initial Release

#### Core Features
- Python client for Lukka cryptocurrency data API
- Support for pricing sources retrieval (`LukkaSources`)
- Historical price data with automatic pagination (`get_historical_price`)
- Latest price data retrieval (`get_latest_price`)
- Flexible date handling with optional parameters and sensible defaults

#### Data Management
- Data export to multiple formats: JSON, CSV, and Parquet
- Automatic pagination for large datasets (handles 1000+ records)
- Professional terminal output with formatted tables and headers

#### Authentication & Caching
- Distributed OAuth2 token caching (file-based and Redis)
- Cross-platform cache path support (Windows, Linux, macOS)
- Multiple credential options: explicit parameters, environment variables, or .env file
- Machine usage tracking for distributed systems

#### Performance & Reliability
- Connection pooling and retry logic with exponential backoff
- Rate limiting coordination (5 requests/second)
- Timeout protection (configurable, default 30s)
- Comprehensive error handling and logging

#### Developer Experience
- Full type hints for IDE support
- Context manager support for resource cleanup
- Extensive documentation and examples
- Python 3.13+ support

