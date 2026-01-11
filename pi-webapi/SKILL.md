---
name: pi-webapi
description: Retrieve time-series data from AVEVA PI System historian via PI Web API. Use when accessing current values, historical data, or navigating Asset Framework hierarchies to find PI Points. Supports point queries by tag name, time-range data retrieval (recorded, interpolated, summary), and drilling down through AF elements to discover PI Points for specific machines or equipment. Read-only operations for Boeing PI System at PI1AVDEVA.web.boeing.com.
---

# AVEVA PI Web API Integration

## Overview

Enable Claude to retrieve historian data from the Boeing AVEVA PI System through the PI Web API, supporting current value queries, historical time-series retrieval, and Asset Framework navigation to discover PI Points.

## Quick Start

### Get Current Value by Tag Name

```python
from scripts.pi_client import PIWebAPIClient
import os

client = PIWebAPIClient(
    username=os.environ["PI_USERNAME"],
    password=os.environ["PI_PASSWORD"]
)

# Get current value
value = client.get_current_value_by_tag("TAG001")
print(f"{value['Value']} {value['UnitsAbbreviation']}")
```

### Get Historical Data

```python
# Last 24 hours of recorded data
data = client.get_recorded_values_by_tag(
    tag_name="TAG001",
    start_time="*-24h",
    end_time="*",
    max_count=1000
)

for item in data['Items']:
    print(f"{item['Timestamp']}: {item['Value']}")
```

### Navigate AF to Find PI Points

```python
# Get element
element = client.get_element_by_path(
    "\\\\AF_SERVER\\ProductionData\\Site1\\Machine123"
)

# Get attributes (PI Points)
attributes = client.get_element_attributes(element['WebId'])

# Find PI Point attributes
for attr in attributes['Items']:
    if attr.get('DataReferencePlugIn') == 'PI Point':
        value = client.get_value_by_webid(attr['WebId'])
        print(f"{attr['Name']}: {value['Value']}")
```

## Core Capabilities

### 1. Current Value Retrieval

Get the most recent value for a PI tag.

**Methods:**
- `get_current_value_by_tag(tag_name)` - By tag name
- `get_value_by_webid(webid)` - By WebId (faster if cached)

**Use when:**
- Need latest sensor reading
- Checking current equipment status
- Real-time monitoring

**Example:**
```python
value = client.get_current_value_by_tag("MACHINE123.TEMP")
if value['Good']:
    print(f"Temperature: {value['Value']}°F")
else:
    print("WARNING: Bad quality data")
```

### 2. Historical Data Retrieval

Query time-series data over specified ranges.

**Data Types:**
- **Recorded** - Archive values as stored in PI
- **Interpolated** - Regular interval samples
- **Plot** - Optimized for visualization
- **Summary** - Aggregated statistics (min, max, avg)

**Time expressions:**
- Relative: `*-1d` (1 day ago), `*-8h` (8 hours ago)
- Absolute: `2024-01-15T00:00:00Z`
- Special: `*` (now), `t` (today), `y` (yesterday)

**Methods:**
```python
# Recorded values (as archived)
data = client.get_recorded_values_by_tag(
    "TAG001",
    start_time="*-7d",
    end_time="*",
    max_count=10000
)

# Interpolated (hourly samples)
data = client.get_interpolated_values_by_tag(
    "TAG001",
    start_time="*-24h",
    end_time="*",
    interval="1h"
)

# Summary statistics (daily averages)
data = client.get_summary_values_by_tag(
    "TAG001",
    start_time="*-30d",
    end_time="*",
    summary_type="Average",
    summary_duration="1d"
)
```

See [references/examples.md](references/examples.md) for more time range patterns.

### 3. Asset Framework Navigation

Drill down through AF hierarchy to find PI Points.

**Workflow:**
1. Get database by path
2. Navigate elements (Site → Area → Equipment → Machine)
3. Get element attributes
4. Filter for PI Point data references
5. Retrieve stream data

**Example:**
```python
# Get database
db = client.get_asset_database_by_path("\\\\AF_SERVER\\ProductionData")

# Get root elements
roots = client.get_elements(db['WebId'])

# Navigate to machine
machine = client.get_element_by_path(
    "\\\\AF_SERVER\\ProductionData\\Site1\\Area1\\Machine123"
)

# Get attributes with PI Point references
attributes = client.get_element_attributes(machine['WebId'])
pi_points = [
    attr for attr in attributes['Items']
    if attr.get('DataReferencePlugIn') == 'PI Point'
]

# Get current values for all PI Points
for attr in pi_points:
    value = client.get_value_by_webid(attr['WebId'])
    print(f"{attr['Name']}: {value['Value']} {value.get('UnitsAbbreviation', '')}")
```

### 4. Point Search

Find PI tags using wildcard patterns.

**Use when:**
- User doesn't know exact tag name
- Finding all tags for a machine
- Discovering available points

**Example:**
```python
# Find all tags for MACHINE123
points = client.search_points(name_filter="MACHINE123.*")

for point in points['Items']:
    print(f"{point['Name']}: {point.get('Descriptor', '')}")
```

## Configuration

### Authentication

PI Web API uses HTTP Basic Authentication.

**Setup:**
```bash
# Environment variables
export PI_USERNAME="your_username"
export PI_PASSWORD="your_password"
```

**Client initialization:**
```python
client = PIWebAPIClient(
    base_url="https://PI1AVDEVA.web.boeing.com/piwebapi",
    username=os.environ["PI_USERNAME"],
    password=os.environ["PI_PASSWORD"],
    default_data_server="PI1AVDEVA"
)
```

### Config File Pattern

```python
# config.json
{
  "pi_webapi": {
    "base_url": "https://PI1AVDEVA.web.boeing.com/piwebapi",
    "username": "username",
    "password": "password",
    "default_data_server": "PI1AVDEVA"
  }
}

# Load config
import json
with open('config.json') as f:
    config = json.load(f)

client = PIWebAPIClient(**config['pi_webapi'])
```

## Common Patterns

### Pattern 1: Get Machine Data

User asks: "What's the current temperature for Machine 123?"

```python
# Option 1: Direct tag query (if you know the tag)
value = client.get_current_value_by_tag("MACHINE123.TEMP")

# Option 2: Navigate AF (if tag is unknown)
machine = client.get_element_by_path(
    "\\\\AF_SERVER\\Production\\Site1\\Machine123"
)
attributes = client.get_element_attributes(machine['WebId'])
temp_attr = next(
    attr for attr in attributes['Items']
    if 'temp' in attr['Name'].lower()
)
value = client.get_value_by_webid(temp_attr['WebId'])

print(f"Temperature: {value['Value']}°F")
```

### Pattern 2: Time-Series Analysis

User asks: "Show me the pressure trend for the last 24 hours"

```python
# Get hourly samples for smooth visualization
data = client.get_interpolated_values_by_tag(
    "MACHINE123.PRESSURE",
    start_time="*-24h",
    end_time="*",
    interval="1h"
)

# Extract values for analysis
timestamps = [item['Timestamp'] for item in data['Items']]
values = [item['Value'] for item in data['Items']]

# Could then plot or analyze trend
```

### Pattern 3: Data Quality Checks

Always validate data quality before using values:

```python
value = client.get_current_value_by_tag("TAG001")

if not value.get('Good', False):
    print(f"WARNING: Data quality issue")
    print(f"  Questionable: {value.get('Questionable', False)}")
    print(f"  Substituted: {value.get('Substituted', False)}")
else:
    # Use value
    print(f"Valid value: {value['Value']}")
```

### Pattern 4: WebId Caching

WebIds are persistent - cache them for performance:

```python
# Store WebIds to avoid repeated path lookups
webid_cache = {}

def get_value_cached(tag_name):
    if tag_name not in webid_cache:
        point = client.get_point_by_path(f"\\\\PI1AVDEVA\\{tag_name}")
        webid_cache[tag_name] = point['WebId']
    
    return client.get_value_by_webid(webid_cache[tag_name])

# First call: queries path and caches WebId
value1 = get_value_cached("TAG001")

# Second call: uses cached WebId (faster)
value2 = get_value_cached("TAG001")
```

## Error Handling

**Common errors:**
- 401: Invalid credentials
- 404: Tag/path not found
- 400: Invalid time expression or parameters
- 403: Insufficient permissions

**Defensive pattern:**
```python
try:
    value = client.get_current_value_by_tag("TAG001")
    print(f"Value: {value['Value']}")
except ValueError as e:
    if "404" in str(e):
        print("Tag not found")
    elif "401" in str(e):
        print("Authentication failed")
    else:
        print(f"Error: {e}")
```

## Response Structure

### Value Response
```python
{
    "Timestamp": "2024-01-15T14:30:00Z",
    "Value": 75.3,
    "UnitsAbbreviation": "°F",
    "Good": True,
    "Questionable": False,
    "Substituted": False
}
```

### Time-Series Response
```python
{
    "Items": [
        {"Timestamp": "...", "Value": 72.5, "Good": True},
        {"Timestamp": "...", "Value": 73.8, "Good": True}
    ],
    "UnitsAbbreviation": "°F"
}
```

### Element Response
```python
{
    "WebId": "F1ABC...",
    "Name": "Machine123",
    "Path": "\\\\AF_SERVER\\DB\\Site\\Machine123",
    "HasChildren": True,
    "Links": {"Elements": "...", "Attributes": "..."}
}
```

### Attribute Response
```python
{
    "WebId": "F1DEF...",
    "Name": "Temperature",
    "Type": "Double",
    "DataReferencePlugIn": "PI Point",  # Indicates PI Point reference
    "ConfigString": "\\\\PI1AVDEVA\\TAG001",
    "DefaultUnitsName": "degree Fahrenheit"
}
```

## Best Practices

1. **Always specify time ranges** - Avoid open-ended queries
2. **Set maxCount limits** - Default 1000, adjust as needed
3. **Check data quality** - Use `Good`, `Questionable`, `Substituted` flags
4. **Cache WebIds** - They're persistent and faster than path lookups
5. **Use appropriate data type**:
   - Recorded: Raw archive data
   - Interpolated: Regular intervals for analysis
   - Plot: Visualization (most efficient)
   - Summary: Statistics (min, max, avg)
6. **Handle time zones** - API returns UTC, convert as needed
7. **Prefer WebId over path** - Direct WebId lookups are faster

## Resources

- **[references/api_reference.md](references/api_reference.md)** - Complete endpoint documentation
- **[references/examples.md](references/examples.md)** - Comprehensive usage examples
- **[scripts/pi_client.py](scripts/pi_client.py)** - Production-ready client implementation

## External Resources

- **PI Web API Documentation**: https://docs.aveva.com/bundle/pi-web-api-reference
- **Boeing PI Server**: https://PI1AVDEVA.web.boeing.com/piwebapi
- **Default Data Server**: PI1AVDEVA

