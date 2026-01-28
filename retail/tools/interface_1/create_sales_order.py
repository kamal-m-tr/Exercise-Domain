import json
from datetime import date, datetime
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool


class CreateSalesOrder(Tool):
    """Creates a new sales order."""

    @staticmethod
    def invoke(
        data: Dict[str, Any],
        user_id: str,
        payment_method: str,
        order_date: Optional[str] = None,
        status: Optional[str] = None,
    ) -> str:
        default_date = date.today().isoformat()

        # Validate data structure
        if not isinstance(data, dict):
            return json.dumps({"success": False, "error": "Invalid data format"})

        sales_orders = data.get("sales_orders", {})
        users = data.get("users", {})

        # Validate required fields
        if not user_id:
            return json.dumps({"success": False, "error": "user_id is required"})
        if not payment_method:
            return json.dumps({"success": False, "error": "payment_method is required"})

        # Validate date format if provided
        if order_date:
            try:
                datetime.strptime(order_date, "%Y-%m-%d")
            except ValueError:
                return json.dumps({
                    "success": False,
                    "error": "order_date must be in YYYY-MM-DD format"
                })

        # Verify user exists
        if str(user_id) not in users:
            return json.dumps({
                "success": False,
                "error": f"User with ID '{user_id}' not found"
            })

        # Validate payment_method
        valid_payment_methods = ["credit_card", "debit_card", "paypal", "bank_transfer", "cash_on_delivery"]
        if payment_method.lower() not in valid_payment_methods:
            return json.dumps({
                "success": False,
                "error": f"Invalid payment_method. Must be one of: {', '.join(valid_payment_methods)}"
            })

        # Validate status if provided
        valid_statuses = ["pending", "confirmed", "processing", "shipped", "delivered", "cancelled"]
        if status and status.lower() not in valid_statuses:
            return json.dumps({
                "success": False,
                "error": f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
            })

        # Generate new sales_order_id
        if sales_orders:
            new_id = str(max(int(k) for k in sales_orders.keys()) + 1)
        else:
            new_id = "1"

        # Create new sales order
        new_so = {
            "sales_order_id": new_id,
            "user_id": str(user_id),
            "order_date": order_date or default_date,
            "status": (status or "pending").lower(),
            "payment_method": payment_method.lower(),
            "cancel_reason": "",
        }

        # Add to data
        sales_orders[new_id] = new_so
        data["sales_orders"] = sales_orders

        return json.dumps({"success": True, "sales_order": new_so})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_sales_order",
                "description": "Creates a new sales order for a customer.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {
                            "type": "string",
                            "description": "Customer placing the order.",
                        },
                        "payment_method": {
                            "type": "string",
                            "description": "Payment method (credit_card, debit_card, paypal, bank_transfer, cash_on_delivery).",
                        },
                        "order_date": {
                            "type": "string",
                            "description": "Order date (YYYY-MM-DD). Defaults to current date.",
                        },
                        "status": {
                            "type": "string",
                            "description": "Initial status. Defaults to 'pending'.",
                        },
                    },
                    "required": ["user_id", "payment_method"],
                },
            },
        }
