import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool


class UpdateProduct(Tool):
    """Updates product information."""

    @staticmethod
    def invoke(
        data: Dict[str, Any],
        product_id: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        supplier_id: Optional[str] = None,
        unit_price: Optional[float] = None,
    ) -> str:

        # Validate data structure
        if not isinstance(data, dict):
            return json.dumps({"success": False, "error": "Invalid data format"})

        products = data.get("products", {})
        suppliers = data.get("suppliers", {})

        # Validate required field
        if not product_id:
            return json.dumps({"success": False, "error": "product_id is required"})

        # Find product
        product = products.get(str(product_id))
        if not product:
            return json.dumps({
                "success": False,
                "error": f"Product with ID '{product_id}' not found"
            })

        # Check if any update field provided
        has_update = any([
            name is not None,
            description is not None,
            supplier_id is not None,
            unit_price is not None,
        ])
        if not has_update:
            return json.dumps({"success": False, "error": "No update fields provided"})

        # Verify new supplier exists if supplier_id is being updated
        if supplier_id and str(supplier_id) not in suppliers:
            return json.dumps({
                "success": False,
                "error": f"Supplier with ID '{supplier_id}' not found"
            })

        # Validate unit_price if provided
        if unit_price is not None and unit_price <= 0:
            return json.dumps({"success": False, "error": "unit_price must be a positive number"})

        # Apply updates (with trimming for text fields)
        if name is not None:
            product["name"] = name.strip()
        if description is not None:
            product["description"] = description.strip()
        if supplier_id is not None:
            product["supplier_id"] = str(supplier_id)
        if unit_price is not None:
            product["unit_price"] = round(float(unit_price), 2)

        return json.dumps({"success": True, "product": product})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_product",
                "description": "Updates product information.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "product_id": {
                            "type": "string",
                            "description": "The product's unique identifier.",
                        },
                        "name": {
                            "type": "string",
                            "description": "New product name.",
                        },
                        "description": {
                            "type": "string",
                            "description": "New description.",
                        },
                        "supplier_id": {
                            "type": "string",
                            "description": "New supplier ID.",
                        },
                        "unit_price": {
                            "type": "number",
                            "description": "New unit price.",
                        },
                    },
                    "required": ["product_id"],
                },
            },
        }
