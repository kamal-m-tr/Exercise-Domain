import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool


class UpdatePurchaseOrder(Tool):
    """Updates purchase order status."""

    @staticmethod
    def invoke(
        data: Dict[str, Any],
        purchase_order_id: str,
        status: str,
    ) -> str:

        # Validate data structure
        if not isinstance(data, dict):
            return json.dumps({"success": False, "error": "Invalid data format"})

        purchase_orders = data.get("purchase_orders", {})

        # Validate required fields
        if not purchase_order_id:
            return json.dumps({"success": False, "error": "purchase_order_id is required"})

        if not status:
            return json.dumps({"success": False, "error": "status is required"})

        # Validate status
        valid_statuses = ["pending", "approved", "shipped", "received", "cancelled"]
        if status.lower() not in valid_statuses:
            return json.dumps({
                "success": False,
                "error": f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
            })

        # Find purchase order
        po = purchase_orders.get(str(purchase_order_id))
        if not po:
            return json.dumps({
                "success": False,
                "error": f"Purchase order with ID '{purchase_order_id}' not found"
            })

        # Update status
        po["status"] = status.lower()

        return json.dumps({"success": True, "purchase_order": po})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_purchase_order",
                "description": "Updates purchase order status.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "purchase_order_id": {
                            "type": "string",
                            "description": "The purchase order's unique identifier.",
                        },
                        "status": {
                            "type": "string",
                            "description": "New status (pending, approved, shipped, received, cancelled).",
                        },
                    },
                    "required": ["purchase_order_id", "status"],
                },
            },
        }
