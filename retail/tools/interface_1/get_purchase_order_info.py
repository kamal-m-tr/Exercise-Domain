import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool


class GetPurchaseOrderInfo(Tool):
    """Retrieves purchase orders with filters."""

    @staticmethod
    def invoke(
        data: Dict[str, Any],
        purchase_order_id: Optional[str] = None,
        supplier_id: Optional[str] = None,
        status: Optional[str] = None,
    ) -> str:
        # Validate data structure
        if not isinstance(data, dict):
            return json.dumps({"success": False, "error": "Invalid data format"})

        purchase_orders = data.get("purchase_orders", {})

        if not isinstance(purchase_orders, dict):
            return json.dumps({"success": False, "error": "Invalid purchase_orders data structure"})

        # Search by purchase_order_id (exact match)
        if purchase_order_id:
            po = purchase_orders.get(str(purchase_order_id))
            if po:
                return json.dumps({"success": True, "purchase_order": po})
            return json.dumps({
                "success": False,
                "error": f"Purchase order with ID '{purchase_order_id}' not found"
            })

        # Filter purchase orders
        matching_pos = list(purchase_orders.values())

        # Filter by supplier_id
        if supplier_id:
            matching_pos = [
                po for po in matching_pos
                if isinstance(po, dict) and po.get("supplier_id") == str(supplier_id)
            ]

        # Filter by status
        if status:
            valid_statuses = ["pending", "approved", "shipped", "received", "cancelled"]
            if status.lower() not in valid_statuses:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
                })
            matching_pos = [
                po for po in matching_pos
                if isinstance(po, dict) and po.get("status", "").lower() == status.lower()
            ]

        if not matching_pos:
            return json.dumps({
                "success": False,
                "error": "No purchase orders found matching the criteria"
            })

        if len(matching_pos) == 1:
            return json.dumps({"success": True, "purchase_order": matching_pos[0]})

        return json.dumps({"success": True, "purchase_orders": matching_pos})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_purchase_order_info",
                "description": "Retrieves purchase orders with optional filters.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "purchase_order_id": {
                            "type": "string",
                            "description": "The purchase order's unique identifier.",
                        },
                        "supplier_id": {
                            "type": "string",
                            "description": "Filter by supplier ID.",
                        },
                        "status": {
                            "type": "string",
                            "description": "Filter by status (pending, approved, shipped, received, cancelled).",
                        },
                    },
                    "required": [],
                },
            },
        }
