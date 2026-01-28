import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool


class GetShippingInfo(Tool):
    """Retrieves shipping records."""

    @staticmethod
    def invoke(
        data: Dict[str, Any],
        shipping_id: Optional[str] = None,
        sales_order_id: Optional[str] = None,
        status: Optional[str] = None,
    ) -> str:
        # Validate data structure
        if not isinstance(data, dict):
            return json.dumps({"success": False, "error": "Invalid data format"})

        shipping = data.get("shipping", {})

        if not isinstance(shipping, dict):
            return json.dumps({"success": False, "error": "Invalid shipping data structure"})

        # Search by shipping_id (exact match)
        if shipping_id:
            ship = shipping.get(str(shipping_id))
            if ship:
                return json.dumps({"success": True, "shipping": ship})
            return json.dumps({
                "success": False,
                "error": f"Shipping record with ID '{shipping_id}' not found"
            })

        # Filter shipping records
        matching_shipments = list(shipping.values())

        # Filter by sales_order_id
        if sales_order_id:
            matching_shipments = [
                s for s in matching_shipments
                if isinstance(s, dict) and s.get("sales_order_id") == str(sales_order_id)
            ]

        # Filter by status
        if status:
            valid_statuses = ["pending", "in_transit", "out_for_delivery", "delivered", "failed", "returned"]
            if status.lower() not in valid_statuses:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
                })
            matching_shipments = [
                s for s in matching_shipments
                if isinstance(s, dict) and s.get("status", "").lower() == status.lower()
            ]

        if not matching_shipments:
            return json.dumps({
                "success": False,
                "error": "No shipping records found matching the criteria"
            })

        if len(matching_shipments) == 1:
            return json.dumps({"success": True, "shipping": matching_shipments[0]})

        return json.dumps({"success": True, "shipments": matching_shipments})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_shipping_info",
                "description": "Retrieves shipping records with optional filters.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "shipping_id": {
                            "type": "string",
                            "description": "The shipping record's unique identifier.",
                        },
                        "sales_order_id": {
                            "type": "string",
                            "description": "Filter by sales order ID.",
                        },
                        "status": {
                            "type": "string",
                            "description": "Filter by status (pending, in_transit, out_for_delivery, delivered, failed, returned).",
                        },
                    },
                    "required": [],
                },
            },
        }
