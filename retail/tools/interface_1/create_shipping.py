import json
from datetime import datetime
from typing import Any, Dict
from tau_bench.envs.tool import Tool


class CreateShipping(Tool):
    """Creates shipping record for sales order."""

    @staticmethod
    def invoke(
        data: Dict[str, Any],
        sales_order_id: str,
        address: str,
        estimate_deliver_date: str,
        method: str,
    ) -> str:

        # Validate data structure
        if not isinstance(data, dict):
            return json.dumps({"success": False, "error": "Invalid data format"})

        sales_orders = data.get("sales_orders", {})
        shipping = data.get("shipping", {})

        # Validate required fields
        if not sales_order_id:
            return json.dumps({"success": False, "error": "sales_order_id is required"})
        if not address:
            return json.dumps({"success": False, "error": "address is required"})
        if not estimate_deliver_date:
            return json.dumps({"success": False, "error": "estimate_deliver_date is required"})
        if not method:
            return json.dumps({"success": False, "error": "method is required"})

        # Validate date format
        try:
            datetime.strptime(estimate_deliver_date, "%Y-%m-%d")
        except ValueError:
            return json.dumps({
                "success": False,
                "error": "estimate_deliver_date must be in YYYY-MM-DD format"
            })

        # Verify sales order exists
        so = sales_orders.get(str(sales_order_id))
        if not so:
            return json.dumps({
                "success": False,
                "error": f"Sales order with ID '{sales_order_id}' not found"
            })

        # Check order status - cannot create shipping for cancelled orders
        so_status = (so.get("status") or "").lower()
        if so_status == "cancelled":
            return json.dumps({
                "success": False,
                "error": "Cannot create shipping for a cancelled order"
            })

        # Validate shipping method
        valid_methods = ["standard", "express", "overnight", "economy", "priority"]
        if method.lower() not in valid_methods:
            return json.dumps({
                "success": False,
                "error": f"Invalid method. Must be one of: {', '.join(valid_methods)}"
            })

        # Check if shipping already exists for this sales order
        for ship in shipping.values():
            if isinstance(ship, dict) and ship.get("sales_order_id") == str(sales_order_id):
                return json.dumps({
                    "success": False,
                    "error": f"Shipping record already exists for sales order '{sales_order_id}'"
                })

        # Generate new shipping_id
        if shipping:
            new_id = str(max(int(k) for k in shipping.keys()) + 1)
        else:
            new_id = "1"

        # Create new shipping record
        new_shipping = {
            "shipping_id": new_id,
            "sales_order_id": str(sales_order_id),
            "address": address,
            "estimate_deliver_date": estimate_deliver_date,
            "real_deliver_date": "",
            "method": method.lower(),
            "tracking_number": "",
            "status": "pending",
        }

        # Add to data
        shipping[new_id] = new_shipping
        data["shipping"] = shipping

        return json.dumps({"success": True, "shipping": new_shipping})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_shipping",
                "description": "Creates a shipping record for a sales order.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "sales_order_id": {
                            "type": "string",
                            "description": "The sales order to ship.",
                        },
                        "address": {
                            "type": "string",
                            "description": "Shipping address.",
                        },
                        "estimate_deliver_date": {
                            "type": "string",
                            "description": "Estimated delivery date (YYYY-MM-DD).",
                        },
                        "method": {
                            "type": "string",
                            "description": "Shipping method (standard, express, overnight, economy, priority).",
                        },
                    },
                    "required": ["sales_order_id", "address", "estimate_deliver_date", "method"],
                },
            },
        }
