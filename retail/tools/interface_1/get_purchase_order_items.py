import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool


class GetPurchaseOrderItems(Tool):
    """Retrieves purchase order line items."""

    @staticmethod
    def invoke(
        data: Dict[str, Any],
        purchase_order_id: str,
        product_id: Optional[str] = None,
    ) -> str:
        # Validate data structure
        if not isinstance(data, dict):
            return json.dumps({"success": False, "error": "Invalid data format"})

        purchase_order_items = data.get("purchase_order_items", {})
        purchase_orders = data.get("purchase_orders", {})

        if not isinstance(purchase_order_items, dict):
            return json.dumps({"success": False, "error": "Invalid purchase_order_items data structure"})

        if not isinstance(purchase_orders, dict):
            return json.dumps({"success": False, "error": "Invalid purchase_orders data structure"})

        # Validate required parameter
        if not purchase_order_id:
            return json.dumps({"success": False, "error": "purchase_order_id is required"})

        # Verify purchase order exists
        if str(purchase_order_id) not in purchase_orders:
            return json.dumps({
                "success": False,
                "error": f"Purchase order with ID '{purchase_order_id}' not found"
            })

        # Filter items by purchase_order_id
        matching_items = [
            item for item in purchase_order_items.values()
            if isinstance(item, dict) and item.get("purchase_order_id") == str(purchase_order_id)
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
                "message": "No items found for this purchase order"
            })

        return json.dumps({"success": True, "items": matching_items})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_purchase_order_items",
                "description": "Retrieves line items for a specific purchase order.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "purchase_order_id": {
                            "type": "string",
                            "description": "The purchase order's unique identifier.",
                        },
                        "product_id": {
                            "type": "string",
                            "description": "Filter by specific product ID.",
                        },
                    },
                    "required": ["purchase_order_id"],
                },
            },
        }
