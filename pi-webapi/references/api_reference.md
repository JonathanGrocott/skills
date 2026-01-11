# AVEVA PI Web API Reference

## Base URL

**Default:** `https://PI1AVDEVA.web.boeing.com/piwebapi`

## Authentication

PI Web API uses HTTP Basic Authentication.

**Header:**
```
Authorization: Basic <base64(username:password)>
```

## Core Controllers

### Stream Controller

Retrieve time-series data from PI Points.

**Base path:** `/streams/{webId}`

#### Key Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/streams/{webId}/value` | GET | Get current value |
| `/streams/{webId}/recorded` | GET | Get recorded (archive) values |
| `/streams/{webId}/interpolated` | GET | Get interpolated values at regular intervals |
| `/streams/{webId}/plot` | GET | Get plot values (optimized for visualization) |
| `/streams/{webId}/summary` | GET | Get summary statistics (min, max, avg, etc.) |
| `/streams/{webId}/end` | GET | Get most recent (end) value |

#### Common Query Parameters

**Time Range:**
- `startTime`: Start time (e.g., `*-1d`, `2024-01-01T00:00:00Z`, `*-24h`)
- `endTime`: End time (e.g., `*`, `2024-01-02T00:00:00Z`)

**Data Selection:**
- `maxCount`: Maximum number of values to return
- `interval`: Time interval for interpolated/plot data (e.g., `1h`, `15m`)
- `summaryType`: Type of summary (`Total`, `Average`, `Minimum`, `Maximum`, `Range`, `StdDev`, `Count`)
- `summaryDuration`: Duration for each summary interval (e.g., `1d`, `1h`)

**Data Quality:**
- `filterExpression`: Filter based on value or quality
- `includeFilteredValues`: Include values that don't match filter

### Point Controller

Access PI Point configuration and metadata.

**Base path:** `/points`

#### Key Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/points/{webId}` | GET | Get point by WebId |
| `/points?path={path}` | GET | Get point by path |
| `/dataservers/{webId}/points` | GET | Search points in data server |
| `/points/{webId}/attributes` | GET | Get point attributes (metadata) |

#### Search Parameters

- `nameFilter`: Filter by point name (supports wildcards `*`)
- `descriptionFilter`: Filter by description
- `pointClass`: Filter by point class
- `pointType`: Filter by point type
- `maxCount`: Maximum results to return
- `startIndex`: Pagination offset

**Example point path:**
```
\\PI1AVDEVA\TagName
```

### AssetDatabase Controller

Access Asset Framework databases.

**Base path:** `/assetdatabases`

#### Key Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/assetdatabases?path={path}` | GET | Get database by path |
| `/assetservers/{webId}/assetdatabases` | GET | List databases on server |
| `/assetdatabases/{webId}/elements` | GET | Get root elements in database |

**Example database path:**
```
\\AF_SERVER\DatabaseName
```

### Element Controller

Navigate Asset Framework element hierarchy.

**Base path:** `/elements`

#### Key Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/elements/{webId}` | GET | Get element by WebId |
| `/elements?path={path}` | GET | Get element by path |
| `/elements/{webId}/elements` | GET | Get child elements |
| `/elements/{webId}/attributes` | GET | Get element attributes |
| `/elements/{webId}/attributes?nameFilter={name}` | GET | Search attributes by name |

**Example element path:**
```
\\AF_SERVER\DatabaseName\RootElement\ChildElement\Machine123
```

#### Navigating to PI Points

1. Get element by path or WebId
2. Get element attributes
3. Find attributes that reference PI Points (check `DataReferencePlugIn` property)
4. Use attribute's `WebId` to get stream data

## WebId

**WebId** is a unique, encoded identifier for any PI Web API object.

- Format: Base64-encoded string
- Persistent across sessions
- Required for most data retrieval operations
- Can be obtained from path-based queries

**Getting WebId from path:**
```
GET /points?path=\\PI1AVDEVA\TAG001
```
Response includes `WebId` property.

## Time Expressions

PI Web API supports flexible time expressions:

**Relative times:**
- `*` - Current time
- `*-1d` - 1 day ago
- `*-8h` - 8 hours ago
- `*-30m` - 30 minutes ago
- `t` - Today at midnight
- `y` - Yesterday at midnight

**Absolute times:**
- ISO 8601 format: `2024-01-15T14:30:00Z`
- PI time format: `15-Jan-24 14:30:00`

**Examples:**
- Last 24 hours: `startTime=*-24h&endTime=*`
- Yesterday: `startTime=y&endTime=t`
- Specific range: `startTime=2024-01-01T00:00:00Z&endTime=2024-01-02T00:00:00Z`

## Response Formats

### Stream Value Response

```json
{
  "Timestamp": "2024-01-15T14:30:00Z",
  "Value": 75.3,
  "UnitsAbbreviation": "°F",
  "Good": true,
  "Questionable": false,
  "Substituted": false
}
```

### Recorded Values Response

```json
{
  "Items": [
    {
      "Timestamp": "2024-01-15T14:00:00Z",
      "Value": 72.5,
      "UnitsAbbreviation": "°F",
      "Good": true
    },
    {
      "Timestamp": "2024-01-15T14:15:00Z",
      "Value": 73.8,
      "UnitsAbbreviation": "°F",
      "Good": true
    }
  ],
  "UnitsAbbreviation": "°F"
}
```

### Element Response

```json
{
  "WebId": "F1ABC...",
  "Id": "12345",
  "Name": "Machine123",
  "Description": "Production Machine 123",
  "Path": "\\\\AF_SERVER\\Database\\Site\\Machine123",
  "TemplateName": "MachineTemplate",
  "HasChildren": true,
  "Links": {
    "Self": "https://...",
    "Elements": "https://...",
    "Attributes": "https://..."
  }
}
```

### Attribute Response

```json
{
  "WebId": "F1DEF...",
  "Id": "67890",
  "Name": "Temperature",
  "Description": "Machine temperature sensor",
  "Path": "\\\\AF_SERVER\\Database\\Site\\Machine123|Temperature",
  "Type": "Double",
  "DefaultUnitsName": "degree Fahrenheit",
  "DataReferencePlugIn": "PI Point",
  "ConfigString": "\\\\PI1AVDEVA\\MACHINE123.TEMP",
  "IsConfigurationItem": false,
  "Links": {
    "Self": "https://...",
    "Point": "https://...",
    "Value": "https://...",
    "InterpolatedData": "https://..."
  }
}
```

## Common Workflows

### 1. Get Current Value by Point Name

```
GET /points?path=\\PI1AVDEVA\TAG001
→ Extract WebId from response
GET /streams/{webId}/value
```

### 2. Get Historical Data for Last 24 Hours

```
GET /points?path=\\PI1AVDEVA\TAG001
→ Extract WebId
GET /streams/{webId}/recorded?startTime=*-24h&endTime=*&maxCount=1000
```

### 3. Navigate AF Hierarchy to Find PI Points

```
GET /assetdatabases?path=\\AF_SERVER\DatabaseName
→ Extract database WebId
GET /assetdatabases/{dbWebId}/elements
→ Find root element, extract WebId
GET /elements/{elementWebId}/elements
→ Navigate to machine element
GET /elements/{machineWebId}/attributes
→ Find temperature attribute with DataReferencePlugIn = "PI Point"
→ Extract attribute WebId
GET /streams/{attrWebId}/value
```

### 4. Search for Points by Wildcard

```
GET /dataservers/{dsWebId}/points?nameFilter=MACHINE123.*&maxCount=100
```

## Error Responses

**401 Unauthorized:**
- Invalid credentials
- Missing Authorization header

**404 Not Found:**
- Invalid WebId
- Path does not exist

**400 Bad Request:**
- Invalid time expression
- Invalid query parameters

**403 Forbidden:**
- Insufficient permissions for resource

## Rate Limiting

- No explicit rate limits documented
- Use reasonable request patterns
- Batch operations when possible
- Cache WebIds to reduce lookups

## Best Practices

1. **Cache WebIds** - WebIds are persistent; cache them to reduce path lookups
2. **Use specific time ranges** - Avoid open-ended queries
3. **Limit maxCount** - Always specify reasonable limits (default: 1000)
4. **Check data quality** - Use `Good`, `Questionable`, `Substituted` flags
5. **Handle time zones** - PI Web API returns UTC; convert as needed
6. **Use plot data for visualization** - More efficient than recorded data
7. **Prefer WebId over path** - WebId lookups are faster


## When Reference Docs Are Useful

Reference docs are ideal for:
- Comprehensive API documentation
- Detailed workflow guides
- Complex multi-step processes
- Information too lengthy for main SKILL.md
- Content that's only needed for specific use cases

## Structure Suggestions

### API Reference Example
- Overview
- Authentication
- Endpoints with examples
- Error codes
- Rate limits

### Workflow Guide Example
- Prerequisites
- Step-by-step instructions
- Common patterns
- Troubleshooting
- Best practices
