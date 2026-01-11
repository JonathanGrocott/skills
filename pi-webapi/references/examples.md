# PI Web API Usage Examples

## Basic Operations

### Get Current Value by Tag Name

```python
from scripts.pi_client import PIWebAPIClient

client = PIWebAPIClient(
    base_url="https://PI1AVDEVA.web.boeing.com/piwebapi",
    username="your_username",
    password="your_password"
)

# Get current value
value = client.get_current_value_by_tag("TAG001")
print(f"Current value: {value['Value']} {value['UnitsAbbreviation']}")
print(f"Timestamp: {value['Timestamp']}")
print(f"Good quality: {value['Good']}")
```

### Get Historical Data

```python
# Get last 24 hours of data
data = client.get_recorded_values_by_tag(
    tag_name="TAG001",
    start_time="*-24h",
    end_time="*",
    max_count=1000
)

for item in data['Items']:
    print(f"{item['Timestamp']}: {item['Value']}")
```

### Get Interpolated Data

```python
# Get hourly averages for last week
data = client.get_interpolated_values_by_tag(
    tag_name="TAG001",
    start_time="*-7d",
    end_time="*",
    interval="1h"
)

for item in data['Items']:
    print(f"{item['Timestamp']}: {item['Value']}")
```

### Get Summary Statistics

```python
# Get daily averages for last month
summaries = client.get_summary_values_by_tag(
    tag_name="TAG001",
    start_time="*-30d",
    end_time="*",
    summary_type="Average",
    summary_duration="1d"
)

for summary in summaries['Items']:
    avg_value = summary['Value']['Average']
    print(f"{summary['Value']['Timestamp']}: {avg_value}")
```

## Asset Framework Navigation

### List Root Elements in Database

```python
# Get database
db = client.get_asset_database_by_path("\\\\AF_SERVER\\ProductionData")

# Get root elements
elements = client.get_elements(db['WebId'])

for elem in elements['Items']:
    print(f"{elem['Name']}: {elem['Description']}")
```

### Navigate Element Hierarchy

```python
# Get element by path
element = client.get_element_by_path(
    "\\\\AF_SERVER\\ProductionData\\Site1\\Area1\\Machine123"
)

print(f"Element: {element['Name']}")
print(f"Template: {element.get('TemplateName', 'None')}")

# Get child elements
children = client.get_child_elements(element['WebId'])

for child in children['Items']:
    print(f"  - {child['Name']}")
```

### Get Element Attributes

```python
# Get all attributes for an element
attributes = client.get_element_attributes(element['WebId'])

for attr in attributes['Items']:
    print(f"Attribute: {attr['Name']}")
    print(f"  Type: {attr['Type']}")
    print(f"  Data Reference: {attr.get('DataReferencePlugIn', 'None')}")
    
    # If it's a PI Point reference, get current value
    if attr.get('DataReferencePlugIn') == 'PI Point':
        value = client.get_value_by_webid(attr['WebId'])
        print(f"  Current Value: {value['Value']}")
```

### Find PI Points for a Machine

```python
# Navigate to machine and get all PI Point attributes
machine_path = "\\\\AF_SERVER\\ProductionData\\Site1\\Machine123"
machine = client.get_element_by_path(machine_path)

# Get attributes
attributes = client.get_element_attributes(machine['WebId'])

# Filter for PI Point references
pi_points = [
    attr for attr in attributes['Items']
    if attr.get('DataReferencePlugIn') == 'PI Point'
]

print(f"Found {len(pi_points)} PI Points for {machine['Name']}:")
for attr in pi_points:
    value = client.get_value_by_webid(attr['WebId'])
    print(f"  {attr['Name']}: {value['Value']} {value.get('UnitsAbbreviation', '')}")
```

## Advanced Queries

### Search for Points by Wildcard

```python
# Search for all tags starting with "MACHINE123"
points = client.search_points(
    name_filter="MACHINE123.*",
    max_count=100
)

for point in points['Items']:
    print(f"{point['Name']}: {point.get('Descriptor', '')}")
```

### Get Multiple Point Values at Once

```python
tag_names = ["TAG001", "TAG002", "TAG003"]

# Get WebIds for all tags
webids = []
for tag in tag_names:
    point = client.get_point_by_path(f"\\\\PI1AVDEVA\\{tag}")
    webids.append(point['WebId'])

# Get current values for all
values = {}
for tag, webid in zip(tag_names, webids):
    value = client.get_value_by_webid(webid)
    values[tag] = value['Value']

print(values)
```

### Time Range Queries

```python
# Yesterday's data
data = client.get_recorded_values_by_tag(
    tag_name="TAG001",
    start_time="y",      # Yesterday at midnight
    end_time="t",        # Today at midnight
    max_count=10000
)

# Specific date range
data = client.get_recorded_values_by_tag(
    tag_name="TAG001",
    start_time="2024-01-01T00:00:00Z",
    end_time="2024-01-02T00:00:00Z",
    max_count=10000
)

# Last 8 hours
data = client.get_recorded_values_by_tag(
    tag_name="TAG001",
    start_time="*-8h",
    end_time="*",
    max_count=1000
)
```

## Data Quality Filtering

### Filter for Good Quality Only

```python
data = client.get_recorded_values_by_tag(
    tag_name="TAG001",
    start_time="*-24h",
    end_time="*",
    max_count=1000
)

# Filter for good quality values only
good_values = [
    item for item in data['Items']
    if item.get('Good', False)
]

print(f"Total values: {len(data['Items'])}")
print(f"Good quality values: {len(good_values)}")
```

### Check Data Quality Flags

```python
value = client.get_current_value_by_tag("TAG001")

print(f"Value: {value['Value']}")
print(f"Good: {value.get('Good', False)}")
print(f"Questionable: {value.get('Questionable', False)}")
print(f"Substituted: {value.get('Substituted', False)}")

if not value.get('Good'):
    print("WARNING: Value quality is not good!")
```

## Error Handling

### Robust Error Handling

```python
try:
    value = client.get_current_value_by_tag("TAG001")
    print(f"Value: {value['Value']}")
except ValueError as e:
    print(f"Error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

### Handle Missing Tags

```python
def get_value_safe(client, tag_name):
    """Safely get value, return None if tag doesn't exist."""
    try:
        return client.get_current_value_by_tag(tag_name)
    except ValueError:
        return None

value = get_value_safe(client, "NONEXISTENT_TAG")
if value is None:
    print("Tag not found")
else:
    print(f"Value: {value['Value']}")
```

## Caching WebIds

### Cache WebIds for Performance

```python
class PIWebAPIClientWithCache(PIWebAPIClient):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._webid_cache = {}
    
    def get_point_by_path_cached(self, path):
        """Get point by path with WebId caching."""
        if path in self._webid_cache:
            return self._webid_cache[path]
        
        point = self.get_point_by_path(path)
        self._webid_cache[path] = point
        return point
    
    def get_current_value_by_tag_cached(self, tag_name):
        """Get current value using cached WebIds."""
        path = f"\\\\{self.default_data_server}\\{tag_name}"
        point = self.get_point_by_path_cached(path)
        return self.get_value_by_webid(point['WebId'])

# Usage
client = PIWebAPIClientWithCache(
    base_url="https://PI1AVDEVA.web.boeing.com/piwebapi",
    username="user",
    password="pass"
)

# First call queries the API
value1 = client.get_current_value_by_tag_cached("TAG001")

# Second call uses cache (faster)
value2 = client.get_current_value_by_tag_cached("TAG001")
```

## Batch Processing

### Process Multiple Tags Efficiently

```python
import pandas as pd

# Get historical data for multiple tags
tags = ["TAG001", "TAG002", "TAG003"]
start_time = "*-24h"
end_time = "*"

# Collect all data
data_frames = []

for tag in tags:
    data = client.get_recorded_values_by_tag(
        tag_name=tag,
        start_time=start_time,
        end_time=end_time,
        max_count=1000
    )
    
    # Convert to DataFrame
    df = pd.DataFrame(data['Items'])
    df['Tag'] = tag
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    
    data_frames.append(df)

# Combine all data
all_data = pd.concat(data_frames, ignore_index=True)

# Pivot for analysis
pivot = all_data.pivot(index='Timestamp', columns='Tag', values='Value')
print(pivot.head())
```

## Configuration File Pattern

### Store credentials in config file

```python
import json

# config.json
"""
{
  "pi_webapi": {
    "base_url": "https://PI1AVDEVA.web.boeing.com/piwebapi",
    "username": "your_username",
    "password": "your_password",
    "default_data_server": "PI1AVDEVA"
  }
}
"""

# Load config
with open('config.json') as f:
    config = json.load(f)

client = PIWebAPIClient(**config['pi_webapi'])
```
