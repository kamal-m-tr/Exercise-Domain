import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool


class GetProductInfo(Tool):
    """Retrieves product records with optional filters."""

    @staticmethod
    def invoke(
        data: Dict[str, Any],
        product_id: Optional[str] = None,
        name: Optional[str] = None,
        supplier_id: Optional[str] = None,
    ) -> str:
        # Validate data structure
        if not isinstance(data, dict):
            return json.dumps({"success": False, "error": "Invalid data format"})

        products = data.get("products", {})

        if not isinstance(products, dict):
            return json.dumps({"success": False, "error": "Invalid products data structure"})

        # Search by product_id (exact match)
        if product_id:
            product = products.get(str(product_id))
            if product:
                return json.dumps({"success": True, "product": product})
            return json.dumps({
                "success": False,
                "error": f"Product with product_id '{product_id}' not found"
            })

        # Filter products
        matching_products = list(products.values())

        # Filter by name (partial match, case-insensitive)
        if name:
            name_lower = name.lower()
            matching_products = [
                p for p in matching_products
                if isinstance(p, dict) and name_lower in p.get("name", "").lower()
            ]

        # Filter by supplier_id
        if supplier_id:
            matching_products = [
                p for p in matching_products
                if isinstance(p, dict) and p.get("supplier_id") == str(supplier_id)
            ]

        if not matching_products:
            return json.dumps({
                "success": False,
                "error": "No products found matching the criteria"
            })

        if len(matching_products) == 1:
            return json.dumps({"success": True, "product": matching_products[0]})

        return json.dumps({"success": True, "products": matching_products})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_product_info",
                "description": "Retrieves product records with optional filters. Returns single product or list.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "product_id": {
                            "type": "string",
                            "description": "The product's unique identifier.",
                        },
                        "name": {
                            "type": "string",
                            "description": "The product's name (partial match, case-insensitive).",
                        },
                        "supplier_id": {
                            "type": "string",
                            "description": "Filter by supplier ID.",
                        },
                    },
                    "required": [],
                },
            },
        }
