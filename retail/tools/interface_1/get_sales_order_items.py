import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool


class GetSalesOrderItems(Tool):
    """Retrieves sales order line items."""

    @staticmethod
    def invoke(
        data: Dict[str, Any],
        sales_order_id: str,
        product_id: Optional[str] = None,
    ) -> str:
        # Validate data structure
        if not isinstance(data, dict):
            return json.dumps({"success": False, "error": "Invalid data format"})

        sales_order_items = data.get("sales_order_items", {})
        sales_orders = data.get("sales_orders", {})

        if not isinstance(sales_order_items, dict):
            return json.dumps({"success": False, "error": "Invalid sales_order_items data structure"})

        # Validate required parameter
        if not sales_order_id:
            return json.dumps({"success": False, "error": "sales_order_id is required"})

        # Verify sales order exists
        if str(sales_order_id) not in sales_orders:
            return json.dumps({
                "success": False,
                "error": f"Sales order with ID '{sales_order_id}' not found"
            })

        # Filter items by sales_order_id
        matching_items = [
            item for item in sales_order_items.values()
            if isinstance(item, dict) and item.get("sales_order_id") == str(sales_order_id)
        ]

        # Filter by product_id if provided
        if product_id:
            matching_items = [
                item for item in matching_items
                if item.get("product_id") == str(product_id)
            ]

        if not matching_items:
            return json.dumps({
                "success": True,
                "items": [],
                "message": "No items found for this sales order"
            })

        return json.dumps({"success": True, "items": matching_items})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_sales_order_items",
                "description": "Retrieves line items for a specific sales order.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "sales_order_id": {
                            "type": "string",
                            "description": "The sales order's unique identifier.",
                        },
                        "product_id": {
                            "type": "string",
                            "description": "Filter by specific product ID.",
                        },
                    },
                    "required": ["sales_order_id"],
                },
            },
        }
