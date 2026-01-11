# Bluetooth Qualified Products API Specification

## API Endpoint

**Base URL:** `https://qualificationapi.bluetooth.com/api/Platform/Listings/Search`

**Method:** `POST`

**Content-Type:** `application/json`

---

## Request Structure

### Headers

```javascript
{
  "Content-Type": "application/json",
  "Accept": "application/json",
  "User-Agent": "YourApp/1.0"
}
```

### Payload

```json
{
  "PublicSearch": true,
  "IsAnonymous": true,
  "UserId": 0,
  "MemberId": null,
  "SearchString": "search term here",
  "ProductName": "",
  "SearchQualificationsAndDesigns": true,
  "SearchDeclarationOnly": true,
  "SearchEndProductList": true,
  "SearchPRDProductList": true,
  "SearchMyCompany": false,
  "BQAApprovalStatusId": -1,
  "BQALockStatusId": -1,
  "MaxResults": 1000,
  "IncludeTestData": false
}
```

### Parameters

| Parameter | Type | Description | Recommended |
|-----------|------|-------------|-------------|
| `PublicSearch` | boolean | Enable public search | `true` |
| `IsAnonymous` | boolean | Anonymous user mode | `true` |
| `UserId` | integer | User ID | `0` |
| `MemberId` | integer/null | Member ID | `null` |
| `SearchString` | string | **Main search term** | User input |
| `ProductName` | string | Product filter | `""` |
| `SearchQualificationsAndDesigns` | boolean | Include qualified products | `true` |
| `SearchDeclarationOnly` | boolean | Include declarations | `true` |
| `SearchEndProductList` | boolean | Include end products | `true` |
| `SearchPRDProductList` | boolean | Include PRD products | `true` |
| `SearchMyCompany` | boolean | Company-specific | `false` |
| `BQAApprovalStatusId` | integer | Approval filter | `-1` (all) |
| `BQALockStatusId` | integer | Lock filter | `-1` (all) |
| `MaxResults` | integer | Result limit | `1000` |
| `IncludeTestData` | boolean | Include test data | `false` |

---

## Response Structure

### Success Response

```json
{
  "Results": [
    {
      "CompanyName": "Company Name",
      "MemberCompany": "Company Name",
      "Name": "Design Name",
      "ModelNumber": "MODEL123",
      "QualificationDate": "2024-01-15T00:00:00",
      "Description": "Product description",
      "Products": [
        {
          "MarketingName": "Product Name",
          "Model": "MODEL-123",
          "Description": "Detailed description",
          "PublishDate": "2024-01-15T00:00:00"
        }
      ]
    }
  ]
}
```

### Response Variants

The API may return:
- `{"Results": [...]}`
- `{"results": [...]}`
- `[...]` (direct array)

### Data Fields Priority

**Always prioritize `Products[0]` over top-level:**

1. **Company**: `CompanyName` or `MemberCompany`
2. **Product Name**: `Products[0].MarketingName` > `Name` > `ProductName`
3. **Model**: `Products[0].Model` > `ModelNumber` > `Model`
4. **Description**: `Products[0].Description` > `Description`
5. **Date**: `Products[0].PublishDate` > `QualificationDate`

---

## Node.js Example

```javascript
const axios = require('axios');

async function searchBluetoothProducts(searchTerm, maxResults = 1000) {
  const payload = {
    PublicSearch: true,
    IsAnonymous: true,
    UserId: 0,
    MemberId: null,
    SearchString: searchTerm,
    ProductName: '',
    SearchQualificationsAndDesigns: true,
    SearchDeclarationOnly: true,
    SearchEndProductList: true,
    SearchPRDProductList: true,
    SearchMyCompany: false,
    BQAApprovalStatusId: -1,
    BQALockStatusId: -1,
    MaxResults: maxResults,
    IncludeTestData: false
  };

  try {
    const response = await axios.post(
      'https://qualificationapi.bluetooth.com/api/Platform/Listings/Search',
      payload,
      {
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        },
        timeout: 45000
      }
    );

    const data = response.data;
    return data.Results || data.results || data || [];
  } catch (error) {
    console.error('API Error:', error.message);
    return null;
  }
}

function extractProductData(result) {
  const company = result.CompanyName || result.MemberCompany || 'N/A';
  
  let productName = 'N/A';
  let modelNumber = 'N/A';
  let description = 'N/A';
  let publishDate = null;

  if (result.Products?.[0]) {
    const product = result.Products[0];
    productName = product.MarketingName?.trim() || productName;
    modelNumber = product.Model?.trim() || modelNumber;
    description = product.Description?.trim() || description;
    publishDate = product.PublishDate;
  }

  // Fallbacks
  productName = productName === 'N/A' ? (result.Name || result.ProductName || 'N/A') : productName;
  modelNumber = modelNumber === 'N/A' ? (result.ModelNumber || result.Model || 'N/A') : modelNumber;
  description = description === 'N/A' ? (result.Description || 'N/A') : description;
  publishDate = publishDate || result.QualificationDate;

  return {
    companyName: company,
    productName,
    modelNumber,
    description,
    publishDate,
    rawData: result
  };
}

// Usage
(async () => {
  const results = await searchBluetoothProducts('Apple');
  if (results) {
    results.slice(0, 5).forEach(result => {
      const product = extractProductData(result);
      console.log(product);
    });
  }
})();
```

---

## React Hook

```javascript
import { useState, useCallback } from 'react';
import axios from 'axios';

export const useBluetoothProducts = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [results, setResults] = useState([]);

  const searchProducts = useCallback(async (searchTerm, maxResults = 1000) => {
    setLoading(true);
    setError(null);

    const payload = {
      PublicSearch: true,
      IsAnonymous: true,
      UserId: 0,
      MemberId: null,
      SearchString: searchTerm,
      ProductName: '',
      SearchQualificationsAndDesigns: true,
      SearchDeclarationOnly: true,
      SearchEndProductList: true,
      SearchPRDProductList: true,
      SearchMyCompany: false,
      BQAApprovalStatusId: -1,
      BQALockStatusId: -1,
      MaxResults: maxResults,
      IncludeTestData: false
    };

    try {
      const response = await axios.post(
        'https://qualificationapi.bluetooth.com/api/Platform/Listings/Search',
        payload,
        {
          headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
          },
          timeout: 45000
        }
      );

      const data = response.data;
      let products = data.Results || data.results || data || [];

      // Standardize data
      const standardized = products.map(result => ({
        companyName: result.CompanyName || result.MemberCompany || 'N/A',
        productName: result.Products?.[0]?.MarketingName?.trim() || 
                     result.Name || result.ProductName || 'N/A',
        modelNumber: result.Products?.[0]?.Model?.trim() || 
                     result.ModelNumber || result.Model || 'N/A',
        description: result.Products?.[0]?.Description?.trim() || 
                     result.Description || 'N/A',
        publishDate: result.Products?.[0]?.PublishDate || 
                     result.QualificationDate,
        rawData: result
      }));

      setResults(standardized);
      setLoading(false);
      return standardized;
    } catch (err) {
      setError(err.message);
      setLoading(false);
      return null;
    }
  }, []);

  return { searchProducts, loading, error, results };
};

// Component usage:
// const { searchProducts, loading, error, results } = useBluetoothProducts();
// await searchProducts('Apple');
```

---

## Implementation Best Practices

### 1. Multi-Field Search (OR Logic)

For searching company AND product, use separate calls:

```python
# Search company
company_results = api.search("Apple")

# Filter by product
filtered = [r for r in company_results 
            if "iPhone" in r.get("Products", [{}])[0].get("MarketingName", "")]
```

### 2. Timeout Handling

- Default: 45 seconds
- API can be slow for large companies
- Implement retry logic (2-3 attempts max)

```python
import time

def search_with_retry(api, term, retries=2):
    for attempt in range(retries + 1):
        try:
            results = api.search(term)
            if results is not None:
                return results
            time.sleep(2 ** attempt)  # Exponential backoff
        except Exception:
            if attempt == retries:
                raise
    return None
```

### 3. Result Sorting

Sort by most recent:

```python
results.sort(
    key=lambda x: x.get('Products', [{}])[0].get('PublishDate', ''), 
    reverse=True
)
```

### 4. Error Handling

```python
results = api.search(term)

if results is None:
    # API error (network, timeout, etc.)
    handle_error()
elif len(results) == 0:
    # Valid response, no matches
    show_no_results()
else:
    # Success
    display_results()
```

### 5. Rate Limiting

- No explicit limits documented
- Use reasonable delays for bulk queries
- Consider caching common searches

---

## Testing

### cURL Test

```bash
curl -X POST https://qualificationapi.bluetooth.com/api/Platform/Listings/Search \
  -H "Content-Type: application/json" \
  -d '{
    "PublicSearch": true,
    "IsAnonymous": true,
    "UserId": 0,
    "MemberId": null,
    "SearchString": "Apple",
    "ProductName": "",
    "SearchQualificationsAndDesigns": true,
    "SearchDeclarationOnly": true,
    "SearchEndProductList": true,
    "SearchPRDProductList": true,
    "SearchMyCompany": false,
    "BQAApprovalStatusId": -1,
    "BQALockStatusId": -1,
    "MaxResults": 10,
    "IncludeTestData": false
  }'
```

### Test Cases

1. **Company**: `"SearchString": "Apple"`
2. **Product**: `"SearchString": "iPhone"`
3. **Model**: `"SearchString": "A2342"`
4. **No Results**: `"SearchString": "NonExistent123"`

---

## Dependencies

```bash
# Python
pip install requests

# Node.js
npm install axios

# React
npm install axios
```
