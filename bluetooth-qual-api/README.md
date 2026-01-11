# Bluetooth Qualified Products API Skill

A comprehensive skill for searching and retrieving Bluetooth SIG Qualified Products certification data.

## What This Skill Provides

This skill enables Claude to search the Bluetooth SIG Qualified Products database and retrieve certification information for Bluetooth devices. It includes:

- **Ready-to-use Python client** with search and data extraction
- **Complete API specification** with Node.js and React examples
- **Best practices** for handling API responses and edge cases
- **Command-line interface** for quick queries

## Usage

When users ask about Bluetooth certified products, qualified devices, or need to search by company/product/model, Claude will automatically use this skill.

### Example User Requests

- "Search for Apple Bluetooth products"
- "Find all Sony headphones in the Bluetooth qualification database"
- "Look up qualification info for model A2342"
- "Get the latest certified Bluetooth devices from Qualcomm"

## Quick Start

### As Python Module

```python
from scripts.bluetooth_api_client import BluetoothQualifiedProductsAPI

api = BluetoothQualifiedProductsAPI()
results = api.search("Apple")

for result in results[:5]:
    product = api.extract_product_data(result)
    print(f"{product['company_name']}: {product['product_name']}")
```

### Command Line

```bash
python scripts/bluetooth_api_client.py --search "Sony" --max-results 10 --sort-by-date
```

### Get JSON Output

```bash
python scripts/bluetooth_api_client.py --search "Qualcomm" --json
```

## File Structure

```
bluetooth-qual-api/
├── SKILL.md                            # Main skill instructions for Claude
├── scripts/
│   └── bluetooth_api_client.py         # Python client (executable)
└── references/
    └── api_spec.md                     # Complete API documentation
```

## Key Features

### Python Client (`scripts/bluetooth_api_client.py`)

- ✅ Search by company, product, or model number
- ✅ Automatic data extraction and standardization
- ✅ Handles multiple response format variations
- ✅ Command-line interface with formatting options
- ✅ Proper timeout handling (45s default)
- ✅ Prioritizes nested `Products[0]` data over top-level fields

### API Reference (`references/api_spec.md`)

- Complete request/response documentation
- Node.js implementation examples
- React hook example
- Best practices for multi-field search, error handling, and sorting
- cURL test commands
- Common patterns and edge cases

## Installation

```bash
# Install dependencies
pip install requests

# Optional: Install for command-line usage globally
pip install -e .
```

## Testing the Skill

```bash
# Test basic search
python scripts/bluetooth_api_client.py --search "Apple" --max-results 5

# Test with sorting
python scripts/bluetooth_api_client.py --search "Sony" --sort-by-date --max-results 10

# Get JSON for integration testing
python scripts/bluetooth_api_client.py --search "Samsung" --json
```

## API Details

- **Endpoint**: `https://qualificationapi.bluetooth.com/api/Platform/Listings/Search`
- **Method**: POST
- **Authentication**: None required (public API)
- **Rate Limits**: No documented limits
- **Timeout**: 45 seconds recommended
- **Max Results**: Up to 1000 per query

## Common Patterns

### Search and Filter

```python
# Search by company
results = api.search("Apple")

# Filter by product name client-side
filtered = [r for r in results 
            if "AirPods" in api.extract_product_data(r)['product_name']]
```

### Sort by Date

```python
products = [api.extract_product_data(r) for r in results]
products.sort(key=lambda x: x.get('publish_date') or '', reverse=True)
```

### Handle Errors

```python
results = api.search("CompanyName")
if results is None:
    print("API error occurred")
elif len(results) == 0:
    print("No results found")
else:
    # Process results
    pass
```

## License

See LICENSE.txt for complete terms.
