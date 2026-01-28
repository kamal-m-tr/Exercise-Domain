import json
from datetime import datetime
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool


class UpdateShipping(Tool):
    """Updates shipping information."""

    @staticmethod
    def invoke(
        data: Dict[str, Any],
        shipping_id: str,
        status: Optional[str] = None,
        tracking_number: Optional[str] = None,
        real_deliver_date: Optional[str] = None,
    ) -> str:

        # Validate data structure
        if not isinstance(data, dict):
            return json.dumps({"success": False, "error": "Invalid data format"})

        shipping = data.get("shipping", {})

        if not isinstance(shipping, dict):
            return json.dumps({"success": False, "error": "Invalid shipping data structure"})

        # Validate required field
        if not shipping_id:
            return json.dumps({"success": False, "error": "shipping_id is required"})

        # Check if any update field provided
        if not status and not tracking_number and not real_deliver_date:
            return json.dumps({
                "success": False,
                "error": "At least one of (status, tracking_number, real_deliver_date) must be provided"
            })

        # Validate status if provided
        valid_statuses = ["pending", "in_transit", "out_for_delivery", "delivered", "failed", "returned"]
        if status and status.lower() not in valid_statuses:
            return json.dumps({
                "success": False,
                "error": f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
            })

        # Validate date format if provided
        if real_deliver_date:
            try:
                datetime.strptime(real_deliver_date, "%Y-%m-%d")
            except ValueError:
                return json.dumps({
                    "success": False,
                    "error": "real_deliver_date must be in YYYY-MM-DD format"
                })

        # Find shipping record
        ship = shipping.get(str(shipping_id))
        if not ship:
            return json.dumps({
                "success": False,
                "error": f"Shipping record with ID '{shipping_id}' not found"
            })

        # Validate status transitions
        if status:
            current_status = ship.get("status", "").lower()
            new_status = status.lower()
            
            valid_transitions = {
                "pending": ["in_transit"],
                "in_transit": ["out_for_delivery"],
                "out_for_delivery": ["delivered", "failed"],
                "failed": ["returned", "in_transit"],
                "delivered": [],
                "returned": [],
            }
            
            if current_status in valid_transitions:
                if new_status not in valid_transitions.get(current_status, []) and new_status != current_status:
                    return json.dumps({
                        "success": False,
                        "error": f"Invalid status transition from '{current_status}' to '{new_status}'"
                    })

            # Tracking number required for in_transit, out_for_delivery, delivered
            if new_status in {"in_transit", "out_for_delivery", "delivered"}:
                existing_tracking = ship.get("tracking_number")
                if not tracking_number and not existing_tracking:
                    return json.dumps({
                        "success": False,
                        "error": f"tracking_number is required when status is '{new_status}'"
                    })

            # real_deliver_date required for delivered status
            if new_status == "delivered":
                existing_date = ship.get("real_deliver_date")
                if not real_deliver_date and not existing_date:
                    return json.dumps({
                        "success": False,
                        "error": "real_deliver_date is required when marking as delivered"
                    })

        # Update fields
        if status:
            ship["status"] = status.lower()
        if tracking_number:
            ship["tracking_number"] = tracking_number
        if real_deliver_date:
            ship["real_deliver_date"] = real_deliver_date

        return json.dumps({"success": True, "shipping": ship})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_shipping",
                "description": "Updates shipping information.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "shipping_id": {
                            "type": "string",
                            "description": "The shipping record's unique identifier.",
                        },
                        "status": {
                            "type": "string",
                            "description": "New status (pending, in_transit, out_for_delivery, delivered, failed, returned).",
                        },
                        "tracking_number": {
                            "type": "string",
                            "description": "Carrier tracking number.",
                        },
                        "real_deliver_date": {
                            "type": "string",
                            "description": "Actual delivery date (YYYY-MM-DD).",
                        },
                    },
                    "required": ["shipping_id"],
                },
            },
        }
