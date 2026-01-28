import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool


class AddSalesOrderItem(Tool):
    """Adds item to sales order."""

    @staticmethod
    def invoke(
        data: Dict[str, Any],
        sales_order_id: str,
        product_id: str,
        quantity: int,
    ) -> str:

        # Validate data structure
        if not isinstance(data, dict):
            return json.dumps({"success": False, "error": "Invalid data format"})

        sales_orders = data.get("sales_orders", {})
        sales_order_items = data.get("sales_order_items", {})
        products = data.get("products", {})

        # Validate required fields
        if not sales_order_id:
            return json.dumps({"success": False, "error": "sales_order_id is required"})
        if not product_id:
            return json.dumps({"success": False, "error": "product_id is required"})
        if quantity is None or quantity <= 0:
            return json.dumps({"success": False, "error": "quantity must be a positive integer"})

        # Verify sales order exists
        so = sales_orders.get(str(sales_order_id))
        if not so:
            return json.dumps({
                "success": False,
                "error": f"Sales order with ID '{sales_order_id}' not found"
            })

        # Check order status - cannot add items to finalized orders
        status = (so.get("status") or "").lower()
        if status in {"cancelled", "shipped", "delivered"}:
            return json.dumps({
                "success": False,
                "error": f"Cannot add items when order status is '{status}'"
            })

        # Verify product exists
        product = products.get(str(product_id))
        if not product:
            return json.dumps({
                "success": False,
                "error": f"Product with ID '{product_id}' not found"
            })

        # Check if item already exists in this SO
        for item in sales_order_items.values():
            if (isinstance(item, dict) and 
                item.get("sales_order_id") == str(sales_order_id) and
                item.get("product_id") == str(product_id)):
                return json.dumps({
                    "success": False,
                    "error": f"Product '{product_id}' already exists in this sales order"
                })

        # Generate new so_item_id
        if sales_order_items:
            new_id = str(max(int(k) for k in sales_order_items.keys()) + 1)
        else:
            new_id = "1"

        # Create new item
        new_item = {
            "so_item_id": new_id,
            "sales_order_id": str(sales_order_id),
            "product_id": str(product_id),
            "quantity": int(quantity),
        }

        # Add to data
        sales_order_items[new_id] = new_item
        data["sales_order_items"] = sales_order_items

        return json.dumps({"success": True, "item": new_item})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "add_sales_order_item",
                "description": "Adds a line item to a sales order.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "sales_order_id": {
                            "type": "string",
                            "description": "The sales order to add item to.",
        },
                        "product_id": {
                            "type": "string",
                            "description": "The product to add.",
        },
                        "quantity": {
                            "type": "integer",
                            "description": "Quantity ordered.",
        },
        },
                    "required": ["sales_order_id", "product_id", "quantity"],
        },
        },
        }
