import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool


class AddPurchaseOrderItem(Tool):
    """Adds item to purchase order."""

    @staticmethod
    def invoke(
        data: Dict[str, Any],
        purchase_order_id: str,
        product_id: str,
        quantity: int,
        unit_cost: float,
    ) -> str:

        # Validate data structure
        if not isinstance(data, dict):
            return json.dumps({"success": False, "error": "Invalid data format"})

        purchase_orders = data.get("purchase_orders", {})
        purchase_order_items = data.get("purchase_order_items", {})
        products = data.get("products", {})

        # Validate required fields
        if not purchase_order_id:
            return json.dumps({"success": False, "error": "purchase_order_id is required"})
        if not product_id:
            return json.dumps({"success": False, "error": "product_id is required"})
        if quantity is None or quantity <= 0:
            return json.dumps({"success": False, "error": "quantity must be a positive integer"})
        if unit_cost is None or unit_cost <= 0:
            return json.dumps({"success": False, "error": "unit_cost must be a positive number"})

        # Verify purchase order exists
        po = purchase_orders.get(str(purchase_order_id))
        if not po:
            return json.dumps({
                "success": False,
                "error": f"Purchase order with ID '{purchase_order_id}' not found"
            })

        # Check PO status - cannot add items to finalized orders
        po_status = (po.get("status") or "").lower()
        if po_status in {"cancelled", "received"}:
            return json.dumps({
                "success": False,
                "error": f"Cannot add items when PO status is '{po_status}'"
            })

        # Verify product exists
        product = products.get(str(product_id))
        if not product:
            return json.dumps({
                "success": False,
                "error": f"Product with ID '{product_id}' not found"
            })

        # Verify product belongs to the same supplier as the PO
        po_supplier_id = po.get("supplier_id")
        product_supplier_id = product.get("supplier_id")
        if po_supplier_id != product_supplier_id:
            return json.dumps({
                "success": False,
                "error": f"Product '{product_id}' belongs to supplier '{product_supplier_id}', but PO is for supplier '{po_supplier_id}'"
            })

        # Check if item already exists in this PO
        for item in purchase_order_items.values():
            if (isinstance(item, dict) and 
                item.get("purchase_order_id") == str(purchase_order_id) and
                item.get("product_id") == str(product_id)):
                return json.dumps({
                    "success": False,
                    "error": f"Product '{product_id}' already exists in this purchase order"
                })

        # Generate new po_item_id
        if purchase_order_items:
            new_id = str(max(int(k) for k in purchase_order_items.keys()) + 1)
        else:
            new_id = "1"

        # Create new item
        new_item = {
            "po_item_id": new_id,
            "purchase_order_id": str(purchase_order_id),
            "product_id": str(product_id),
            "quantity": int(quantity),
            "unit_cost": round(float(unit_cost), 2),
        }

        # Add to data
        purchase_order_items[new_id] = new_item
        data["purchase_order_items"] = purchase_order_items

        return json.dumps({"success": True, "item": new_item})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "add_purchase_order_item",
                "description": "Adds a line item to a purchase order.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "purchase_order_id": {
                            "type": "string",
                            "description": "The purchase order to add item to.",
        },
                        "product_id": {
                            "type": "string",
                            "description": "The product to add.",
        },
                        "quantity": {
                            "type": "integer",
                            "description": "Quantity ordered.",
        },
                        "unit_cost": {
                            "type": "number",
                            "description": "Cost per unit.",
        },
        },
                    "required": ["purchase_order_id", "product_id", "quantity", "unit_cost"],
        },
        },
        }
