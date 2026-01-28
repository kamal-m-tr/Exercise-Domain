import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool


class CreateProduct(Tool):
    """Creates a new product."""

    @staticmethod
    def invoke(
        data: Dict[str, Any],
        name: str,
        description: str,
        supplier_id: str,
        unit_price: float,
    ) -> str:

        # Validate data structure
        if not isinstance(data, dict):
            return json.dumps({"success": False, "error": "Invalid data format"})

        products = data.get("products", {})
        suppliers = data.get("suppliers", {})

        # Validate required fields
        if not all([name, description, supplier_id]):
            return json.dumps({"success": False, "error": "name, description, and supplier_id are required"})

        if unit_price is None or unit_price <= 0:
            return json.dumps({"success": False, "error": "unit_price must be a positive number"})

        # Trim whitespace from text fields
        name = name.strip()
        description = description.strip()

        # Verify supplier exists
        if str(supplier_id) not in suppliers:
            return json.dumps({
                "success": False,
                "error": f"Supplier with ID '{supplier_id}' not found"
            })

        # Check for duplicate product (same name and supplier)
        for pid, product in products.items():
            if isinstance(product, dict):
                if (product.get("name", "").lower() == name.lower() and 
                    product.get("supplier_id") == str(supplier_id)):
                    return json.dumps({
                        "success": False,
                        "error": f"Product '{name}' already exists for this supplier (ID: {pid})"
                    })

        # Generate new product_id
        if products:
            new_id = str(max(int(k) for k in products.keys()) + 1)
        else:
            new_id = "1"

        # Create new product
        new_product = {
            "product_id": new_id,
            "name": name,
            "description": description,
            "supplier_id": str(supplier_id),
            "unit_price": round(float(unit_price), 2),
        }

        # Add to data
        products[new_id] = new_product
        data["products"] = products

        return json.dumps({"success": True, "product": new_product})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_product",
                "description": "Creates a new product in the catalog.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "Product name.",
                        },
                        "description": {
                            "type": "string",
                            "description": "Product description.",
                        },
                        "supplier_id": {
                            "type": "string",
                            "description": "Supplier providing this product.",
                        },
                        "unit_price": {
                            "type": "number",
                            "description": "Price per unit in USD.",
                        },
                    },
                    "required": ["name", "description", "supplier_id", "unit_price"],
                },
            },
        }
