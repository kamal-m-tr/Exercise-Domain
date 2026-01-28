import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool


class GetSupplierInfo(Tool):
    """Retrieves supplier records by ID or name."""

    @staticmethod
    def invoke(
        data: Dict[str, Any],
        supplier_id: Optional[str] = None,
        name: Optional[str] = None,
    ) -> str:
        # Validate data structure
        if not isinstance(data, dict):
            return json.dumps({"success": False, "error": "Invalid data format"})

        suppliers = data.get("suppliers", {})

        if not isinstance(suppliers, dict):
            return json.dumps({"success": False, "error": "Invalid suppliers data structure"})

        # At least one identifier should be provided
        if not supplier_id and not name:
            return json.dumps({
                "success": False,
                "error": "At least one of (supplier_id, name) must be provided"
            })

        # Search by supplier_id
        if supplier_id:
            supplier = suppliers.get(str(supplier_id))
            if supplier:
                return json.dumps({"success": True, "supplier": supplier})
            return json.dumps({
                "success": False,
                "error": f"Supplier with supplier_id '{supplier_id}' not found"
            })

        # Search by name (partial match, case-insensitive)
        if name:
            matching_suppliers = []
            name_lower = name.lower()
            for sid, supplier_data in suppliers.items():
                if isinstance(supplier_data, dict):
                    supplier_name = supplier_data.get("name", "").lower()
                    if name_lower in supplier_name:
                        matching_suppliers.append(supplier_data)

            if len(matching_suppliers) == 1:
                return json.dumps({"success": True, "supplier": matching_suppliers[0]})
            elif len(matching_suppliers) > 1:
                return json.dumps({"success": True, "suppliers": matching_suppliers})
            else:
                return json.dumps({
                    "success": False,
                    "error": f"No supplier found matching name '{name}'"
                })

        return json.dumps({"success": False, "error": "No matching supplier found"})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_supplier_info",
                "description": "Retrieves supplier records by ID or name (partial match supported).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "supplier_id": {
                            "type": "string",
                            "description": "The supplier's unique identifier.",
                        },
                        "name": {
                            "type": "string",
                            "description": "The supplier's name (partial match, case-insensitive).",
                        },
                    },
                    "required": [],
                },
            },
        }
