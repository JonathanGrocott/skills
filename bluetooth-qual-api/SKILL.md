---
name: bluetooth-qual-api
description: Search and retrieve Bluetooth SIG Qualified Products data. Use when users need to look up Bluetooth certified products, search by company name/product name/model number, or retrieve qualification details from the Bluetooth SIG database. Provides Python client, request/response handling, and data extraction guidance.
---

# Bluetooth Qualified Products API

## Overview

Enables searching the Bluetooth SIG Qualified Products database to retrieve certification information for Bluetooth devices. Use the Python client in `scripts/bluetooth_api_client.py` for queries or consult `references/api_spec.md` for implementation details.

## Quick Start

**Basic search workflow:**

```python
# Use the bundled client script
from scripts.bluetooth_api_client import BluetoothQualifiedProductsAPI

api = BluetoothQualifiedProductsAPI()

# Search by company, product, or model
results = api.search("Apple")

# Extract standardized data
for result in results[:5]:
    product = api.extract_product_data(result)
    print(f"{product['company_name']}: {product['product_name']}")
```

**Via terminal:**

```bash
python scripts/bluetooth_api_client.py --search "Apple" --max-results 10
```

## Core Operations

### 1. Simple Search

Search by company name, product name, or model number:

```python
results = api.search("Sony")  # Company search
results = api.search("WH-1000XM4")  # Product search
results = api.search("A2342")  # Model number search
```

### 2. Extract Product Data

The API response has nested structures. Always use `extract_product_data()` to prioritize `Products[0]` data over top-level fields:

```python
for result in results:
    product = api.extract_product_data(result)
    # Guaranteed fields: company_name, product_name, model_number, 
    # description, publish_date, raw_data
```

### 3. Advanced Filtering

For multi-criteria searches (e.g., company AND product), make separate calls and filter client-side:

```python
# Search for company
company_results = api.search("Apple")

# Filter results by product name
filtered = [r for r in company_results 
            if "AirPods" in api.extract_product_data(r)['product_name']]
```

## Data Structure Priority

**Always prioritize nested `Products[0]` data:**

- ✅ `Products[0].MarketingName` → `product_name`
- ✅ `Products[0].Model` → `model_number`  
- ✅ `Products[0].Description` → `description`
- ✅ `Products[0].PublishDate` → `publish_date`

**Fallback to top-level fields only if `Products` array is empty.**

## Common Patterns

**Display recent products:**
```python
# Sort by publish date
sorted_results = sorted(results, 
    key=lambda x: api.extract_product_data(x)['publish_date'] or '', 
    reverse=True)
```

**Handle large result sets:**
```python
# Paginate or limit results
results = api.search("Qualcomm", max_results=100)
```

**Error handling:**
```python
results = api.search("CompanyName")
if results is None:
    print("API error occurred")
elif len(results) == 0:
    print("No results found")
```

## Implementation Notes

- **Timeout**: API calls use 45s timeout (can be slow for large companies)
- **Response formats**: Handles `Results`, `results`, or direct array
- **No rate limits**: No documented limits, but use reasonable delays for bulk queries
- **Empty searches**: Returns empty array, not error

## Resources

### scripts/bluetooth_api_client.py
Complete Python client with search and data extraction methods. Can be executed directly or imported as a module.

### references/api_spec.md  
Full API specification including request payload structure, response schema, Node.js/React examples, and testing instructions.
