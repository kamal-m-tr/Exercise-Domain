import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool


class GetSalesOrderInfo(Tool):
    """Retrieves sales orders with filters."""

    @staticmethod
    def invoke(
        data: Dict[str, Any],
        sales_order_id: Optional[str] = None,
        user_id: Optional[str] = None,
        status: Optional[str] = None,
    ) -> str:
        # Validate data structure
        if not isinstance(data, dict):
            return json.dumps({"success": False, "error": "Invalid data format"})

        sales_orders = data.get("sales_orders", {})

        if not isinstance(sales_orders, dict):
            return json.dumps({"success": False, "error": "Invalid sales_orders data structure"})

        # Search by sales_order_id (exact match)
        if sales_order_id:
            so = sales_orders.get(str(sales_order_id))
            if so:
                return json.dumps({"success": True, "sales_order": so})
            return json.dumps({
                "success": False,
                "error": f"Sales order with ID '{sales_order_id}' not found"
            })

        # Filter sales orders
        matching_sos = list(sales_orders.values())

        # Filter by user_id
        if user_id:
            matching_sos = [
                so for so in matching_sos
                if isinstance(so, dict) and so.get("user_id") == str(user_id)
            ]

        # Filter by status
        if status:
            valid_statuses = ["pending", "confirmed", "processing", "shipped", "delivered", "cancelled"]
            if status.lower() not in valid_statuses:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
                })
            matching_sos = [
                so for so in matching_sos
                if isinstance(so, dict) and so.get("status", "").lower() == status.lower()
            ]

        if not matching_sos:
            return json.dumps({
                "success": False,
                "error": "No sales orders found matching the criteria"
            })

        if len(matching_sos) == 1:
            return json.dumps({"success": True, "sales_order": matching_sos[0]})

        return json.dumps({"success": True, "sales_orders": matching_sos})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_sales_order_info",
                "description": "Retrieves sales orders with optional filters.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "sales_order_id": {
                            "type": "string",
                            "description": "The sales order's unique identifier.",
                        },
                        "user_id": {
                            "type": "string",
                            "description": "Filter by user ID.",
                        },
                        "status": {
                            "type": "string",
                            "description": "Filter by status (pending, confirmed, processing, shipped, delivered, cancelled).",
                        },
                    },
                    "required": [],
                },
            },
        }
