#!/usr/bin/env python3
"""
Bluetooth SIG Qualified Products API Client

Search and retrieve Bluetooth certified product information from the
Bluetooth SIG qualification database.

Usage:
    # As a module
    from bluetooth_api_client import BluetoothQualifiedProductsAPI
    api = BluetoothQualifiedProductsAPI()
    results = api.search("Apple")
    
    # From command line
    python bluetooth_api_client.py --search "Apple" --max-results 10
"""

import requests
import json
from typing import List, Dict, Optional
import argparse


class BluetoothQualifiedProductsAPI:
    """
    Client for Bluetooth SIG Qualified Products API
    """
    
    def __init__(self):
        self.base_url = "https://qualificationapi.bluetooth.com/api/Platform/Listings/Search"
        self.timeout = 45  # seconds
    
    def search(
        self, 
        search_term: str, 
        max_results: int = 1000
    ) -> Optional[List[Dict]]:
        """
        Search for qualified products
        
        Args:
            search_term: Search query (company, product, or model)
            max_results: Maximum number of results (default: 1000)
            
        Returns:
            List of product dictionaries or None if error
        """
        
        payload = {
            "PublicSearch": True,
            "IsAnonymous": True,
            "UserId": 0,
            "MemberId": None,
            "SearchString": search_term,
            "ProductName": "",
            "SearchQualificationsAndDesigns": True,
            "SearchDeclarationOnly": True,
            "SearchEndProductList": True,
            "SearchPRDProductList": True,
            "SearchMyCompany": False,
            "BQAApprovalStatusId": -1,
            "BQALockStatusId": -1,
            "MaxResults": max_results,
            "IncludeTestData": False
        }
        
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "Python/BluetoothAPI Client"
        }
        
        try:
            response = requests.post(
                self.base_url,
                json=payload,
                headers=headers,
                timeout=self.timeout
            )
            
            response.raise_for_status()
            
            data = response.json()
            
            # Handle different response structures
            if isinstance(data, dict) and "Results" in data:
                return data["Results"]
            elif isinstance(data, dict) and "results" in data:
                return data["results"]
            elif isinstance(data, list):
                return data
            else:
                return []
                
        except requests.exceptions.RequestException as e:
            print(f"API Error: {e}")
            return None
        except json.JSONDecodeError as e:
            print(f"JSON Decode Error: {e}")
            return None
    
    def extract_product_data(self, result: Dict) -> Dict:
        """
        Extract standardized product data from API result
        Prioritizes Products array data over top-level fields
        
        Args:
            result: Single result item from API
            
        Returns:
            Standardized product dictionary with keys:
            - company_name: Company/manufacturer name
            - product_name: Product marketing name
            - model_number: Model identifier
            - description: Product description
            - publish_date: Qualification/publish date
            - raw_data: Original API response
        """
        
        # Get company name
        company = result.get("CompanyName") or result.get("MemberCompany") or "N/A"
        
        # Prioritize Products[0] data if available
        product_name = "N/A"
        model_number = "N/A"
        description = "N/A"
        publish_date = None
        
        if result.get("Products") and len(result["Products"]) > 0:
            product = result["Products"][0]
            product_name = product.get("MarketingName", "").strip() or product_name
            model_number = product.get("Model", "").strip() or model_number
            description = product.get("Description", "").strip() or description
            publish_date = product.get("PublishDate")
        
        # Fallback to top-level fields if Products data not available
        if product_name == "N/A":
            product_name = result.get("Name") or result.get("ProductName") or "N/A"
        
        if model_number == "N/A":
            model_number = result.get("ModelNumber") or result.get("Model") or "N/A"
        
        if description == "N/A":
            description = result.get("Description") or "N/A"
        
        if not publish_date:
            publish_date = result.get("QualificationDate")
        
        return {
            "company_name": company,
            "product_name": product_name,
            "model_number": model_number,
            "description": description,
            "publish_date": publish_date,
            "raw_data": result  # Keep raw data for additional fields
        }


def main():
    """Command-line interface"""
    parser = argparse.ArgumentParser(
        description="Search Bluetooth SIG Qualified Products"
    )
    parser.add_argument(
        "--search", "-s",
        required=True,
        help="Search term (company, product, or model)"
    )
    parser.add_argument(
        "--max-results", "-m",
        type=int,
        default=100,
        help="Maximum number of results (default: 100)"
    )
    parser.add_argument(
        "--json", "-j",
        action="store_true",
        help="Output raw JSON instead of formatted text"
    )
    parser.add_argument(
        "--sort-by-date",
        action="store_true",
        help="Sort results by publish date (newest first)"
    )
    
    args = parser.parse_args()
    
    # Create API client and search
    api = BluetoothQualifiedProductsAPI()
    print(f"Searching for: {args.search}")
    
    results = api.search(args.search, args.max_results)
    
    if results is None:
        print("Error: API request failed")
        return 1
    
    if len(results) == 0:
        print("No results found")
        return 0
    
    print(f"Found {len(results)} results\n")
    
    # Extract and optionally sort
    products = [api.extract_product_data(r) for r in results]
    
    if args.sort_by_date:
        products.sort(key=lambda x: x.get('publish_date') or '', reverse=True)
    
    # Output
    if args.json:
        print(json.dumps(products, indent=2))
    else:
        for i, product in enumerate(products, 1):
            print(f"{i}. {product['company_name']}")
            print(f"   Product: {product['product_name']}")
            print(f"   Model: {product['model_number']}")
            print(f"   Date: {product['publish_date']}")
            if product['description'] != "N/A":
                desc = product['description'][:100]
                print(f"   Description: {desc}{'...' if len(product['description']) > 100 else ''}")
            print()
    
    return 0


if __name__ == "__main__":
    exit(main())
