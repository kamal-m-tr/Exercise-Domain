import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool


class UpdateSalesOrder(Tool):
    """Updates sales order status."""

    @staticmethod
    def invoke(
        data: Dict[str, Any],
        sales_order_id: str,
        status: Optional[str] = None,
        cancel_reason: Optional[str] = None,
    ) -> str:

        # Validate data structure
        if not isinstance(data, dict):
            return json.dumps({"success": False, "error": "Invalid data format"})

        sales_orders = data.get("sales_orders", {})

        # Validate required field
        if not sales_order_id:
            return json.dumps({"success": False, "error": "sales_order_id is required"})

        # Check if any update field provided
        if not status and not cancel_reason:
            return json.dumps({"success": False, "error": "At least one of (status, cancel_reason) must be provided"})

        # Validate status if provided
        valid_statuses = ["pending", "confirmed", "processing", "shipped", "delivered", "cancelled"]
        if status and status.lower() not in valid_statuses:
            return json.dumps({
                "success": False,
                "error": f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
            })

        # Find sales order
        so = sales_orders.get(str(sales_order_id))
        if not so:
            return json.dumps({
                "success": False,
                "error": f"Sales order with ID '{sales_order_id}' not found"
            })

        # If status is cancelled, cancel_reason should be provided
        if status and status.lower() == "cancelled" and not cancel_reason:
            return json.dumps({
                "success": False,
                "error": "cancel_reason is required when cancelling an order"
            })

        # cancel_reason can only be set if order is being cancelled or already cancelled
        current_status = (so.get("status") or "").lower()
        new_status = (status or "").lower() if status else current_status
        if cancel_reason and new_status != "cancelled" and current_status != "cancelled":
            return json.dumps({
                "success": False,
                "error": "cancel_reason can only be set for cancelled orders"
            })

        # Update fields
        if status:
            so["status"] = status.lower()
        if cancel_reason:
            so["cancel_reason"] = cancel_reason

        return json.dumps({"success": True, "sales_order": so})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_sales_order",
                "description": "Updates sales order status.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "sales_order_id": {
                            "type": "string",
                            "description": "The sales order's unique identifier.",
                        },
                        "status": {
                            "type": "string",
                            "description": "New status (pending, confirmed, processing, shipped, delivered, cancelled).",
                        },
                        "cancel_reason": {
                            "type": "string",
                            "description": "Reason for cancellation (required if status is 'cancelled').",
                        },
                    },
                    "required": ["sales_order_id"],
                },
            },
        }
