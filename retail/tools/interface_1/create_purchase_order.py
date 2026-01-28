import json
from datetime import date, datetime
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool


class CreatePurchaseOrder(Tool):
    """Creates a new purchase order."""

    @staticmethod
    def invoke(
        data: Dict[str, Any],
        supplier_id: str,
        order_date: Optional[str] = None,
        status: Optional[str] = None,
    ) -> str:
        default_date = date.today().isoformat()

        # Validate data structure
        if not isinstance(data, dict):
            return json.dumps({"success": False, "error": "Invalid data format"})

        purchase_orders = data.get("purchase_orders", {})
        suppliers = data.get("suppliers", {})

        # Validate required field
        if not supplier_id:
            return json.dumps({"success": False, "error": "supplier_id is required"})

        # Validate date format if provided
        if order_date:
            try:
                datetime.strptime(order_date, "%Y-%m-%d")
            except ValueError:
                return json.dumps({
                    "success": False,
                    "error": "order_date must be in YYYY-MM-DD format"
                })

        # Verify supplier exists
        if str(supplier_id) not in suppliers:
            return json.dumps({
                "success": False,
                "error": f"Supplier with ID '{supplier_id}' not found"
            })

        # Validate status if provided
        valid_statuses = ["pending", "approved", "shipped", "received", "cancelled"]
        if status and status.lower() not in valid_statuses:
            return json.dumps({
                "success": False,
                "error": f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
            })

        # Generate new purchase_order_id
        if purchase_orders:
            new_id = str(max(int(k) for k in purchase_orders.keys()) + 1)
        else:
            new_id = "1"

        # Create new purchase order
        new_po = {
            "purchase_order_id": new_id,
            "supplier_id": str(supplier_id),
            "order_date": order_date or default_date,
            "status": (status or "pending").lower(),
        }

        # Add to data
        purchase_orders[new_id] = new_po
        data["purchase_orders"] = purchase_orders

        return json.dumps({"success": True, "purchase_order": new_po})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_purchase_order",
                "description": "Creates a new purchase order for a supplier.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "supplier_id": {
                            "type": "string",
                            "description": "Supplier for this order.",
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
                    "required": ["supplier_id"],
                },
            },
        }
