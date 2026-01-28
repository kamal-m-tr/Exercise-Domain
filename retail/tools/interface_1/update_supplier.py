import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool


class UpdateSupplier(Tool):
    """Updates supplier information."""

    @staticmethod
    def invoke(
        data: Dict[str, Any],
        supplier_id: str,
        name: Optional[str] = None,
        contact_email: Optional[str] = None,
        address: Optional[str] = None,
        city: Optional[str] = None,
        state: Optional[str] = None,
        zip_code: Optional[str] = None,
        country: Optional[str] = None,
    ) -> str:

        # Validate data structure
        if not isinstance(data, dict):
            return json.dumps({"success": False, "error": "Invalid data format"})

        suppliers = data.get("suppliers", {})

        # Validate required field
        if not supplier_id:
            return json.dumps({"success": False, "error": "supplier_id is required"})

        # Find supplier
        supplier = suppliers.get(str(supplier_id))
        if not supplier:
            return json.dumps({
                "success": False,
                "error": f"Supplier with ID '{supplier_id}' not found"
            })

        # Check if any update field provided
        update_fields = {
            "name": name,
            "contact_email": contact_email,
            "address": address,
            "city": city,
            "state": state,
            "zip_code": zip_code,
            "country": country,
        }

        has_update = any(v is not None for v in update_fields.values())
        if not has_update:
            return json.dumps({"success": False, "error": "No update fields provided"})

        # Check for duplicate name if name is being updated
        if name:
            for sid, s in suppliers.items():
                if sid != str(supplier_id) and isinstance(s, dict) and s.get("name", "").lower() == name.lower():
                    return json.dumps({
                        "success": False,
                        "error": f"Supplier with name '{name}' already exists (ID: {sid})"
                    })

        # Apply updates
        for field, value in update_fields.items():
            if value is not None:
                supplier[field] = value

        return json.dumps({"success": True, "supplier": supplier})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_supplier",
                "description": "Updates supplier information.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "supplier_id": {
                            "type": "string",
                            "description": "The supplier's unique identifier.",
                        },
                        "name": {
                            "type": "string",
                            "description": "New supplier name.",
                        },
                        "contact_email": {
                            "type": "string",
                            "description": "New contact email.",
                        },
                        "address": {
                            "type": "string",
                            "description": "New street address.",
                        },
                        "city": {
                            "type": "string",
                            "description": "New city.",
                        },
                        "state": {
                            "type": "string",
                            "description": "New state.",
                        },
                        "zip_code": {
                            "type": "string",
                            "description": "New ZIP code.",
                        },
                        "country": {
                            "type": "string",
                            "description": "New country.",
                        },
                    },
                    "required": ["supplier_id"],
                },
            },
        }
