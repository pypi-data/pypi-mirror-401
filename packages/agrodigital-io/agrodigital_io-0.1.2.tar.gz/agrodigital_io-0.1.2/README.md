# AgroDigital Python SDK

[![PyPI version](https://img.shields.io/pypi/v/agrodigital_io.svg)](https://pypi.org/project/agrodigital_io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A modern, easy-to-use Python SDK for interacting with the [agrodigital.io](https://agrodigital.io) API. This library provides a high-level interface to manage agricultural entities, IoT data, meteorological stations, and satellite imagery analysis.

## Features

- **Entity Management**: CRUD operations for Farms, Fields, Polygons, and Crops.
- **Monitoring & Data**: Specialized access to Raster imagery, indexes, and Google Earth Engine clusters.
- **IoT & Meteo**: Seamless integration with IoT stations and meteorological data.
- **Operations Logs**: Track sowing, applications, and logs.
- **Scouting**: Manage bugs, weeds, and diseases via waypoints.
- **Object-Oriented**: All API responses are converted into Python objects with dot-notation access.

## Installation

You can install the SDK via `pip`:

```bash
pip install agrodigital_io
```

Or using `poetry`:

```bash
poetry add agrodigital_io
```

## Quick Start

### Authentication

To begin, initialize the `AgroDigitalClient` using either your API token or your username and password.

```python
from agrodigital_io import AgroDigitalClient

# Option 1: Using an API Token
client = AgroDigitalClient(token="your_api_token_here")

# Option 2: Using Credentials
client = AgroDigitalClient(username="your_username", password="your_password")
```

### Basic Operations

#### List all farms
```python
farms = client.farms.list()
for farm in farms:
    print(f"Farm: {farm.name} (ID: {farm.id})")
```

#### Get field data
```python
field = client.fields.retrieve(id=123)
print(f"Field name: {field.name}")
print(f"Associated crop: {field.crop.name}") # Nested objects supported
```

#### Fetch IoT Data
```python
# Get data from a specific station between dates
data = client.iot_data.list_data(
    station_id=45, 
    from_date="2023-01-01", 
    to_date="2023-01-07",
    variables=["temperature", "humidity"]
)
```

## Advanced Usage

### Raster and Imagery
Access satellite imagery metadata and available dates for specific polygons.

```python
dates = client.rasters.available_dates()
print(f"Available imagery dates: {dates}")
```

### Cluster Retrieval
Fetch Google Earth Engine or local clusters for a specific polygon and date range.

```python
clusters = client.cluster.ee_retrieve(
    from_date="2023-01-01",
    to_date="2023-12-31",
    polygon_id="poly_88",
    n_clusters=5
)
```

### Error Handling
The SDK raises `AgroDigitalError` for API-related issues, including connection timeouts and non-200 status codes.

```python
from agrodigital_io import AgroDigitalError

try:
    client.fields.retrieve(999999)
except AgroDigitalError as e:
    print(f"Error: {e.message}")
    print(f"Status Code: {e.status_code}")
```

## Requirements

- Python >= 3.10
- `requests` library

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
