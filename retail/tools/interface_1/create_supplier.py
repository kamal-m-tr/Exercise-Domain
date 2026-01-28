import json
import re
from typing import Any, Dict
from tau_bench.envs.tool import Tool


class CreateSupplier(Tool):
    """Creates a new supplier."""

    @staticmethod
    def invoke(
        data: Dict[str, Any],
        name: str,
        contact_email: str,
        address: str,
        city: str,
        state: str,
        zip_code: str,
        country: str,
    ) -> str:

        # Validate data structure
        if not isinstance(data, dict):
            return json.dumps({"success": False, "error": "Invalid data format"})

        suppliers = data.get("suppliers", {})

        # Validate required fields
        if not all([name, contact_email, address, city, state, zip_code, country]):
            return json.dumps({"success": False, "error": "All fields are required"})

        # Validate email format
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, contact_email):
            return json.dumps({"success": False, "error": "Invalid email format"})

        # Trim whitespace from text fields
        name = name.strip()
        address = address.strip()
        city = city.strip()
        state = state.strip()
        zip_code = zip_code.strip()
        country = country.strip()

        # Check for duplicate supplier name
        for sid, supplier in suppliers.items():
            if isinstance(supplier, dict) and supplier.get("name", "").lower() == name.lower():
                return json.dumps({
                    "success": False,
                    "error": f"Supplier with name '{name}' already exists (ID: {sid})"
                })

        # Generate new supplier_id
        if suppliers:
            new_id = str(max(int(k) for k in suppliers.keys()) + 1)
        else:
            new_id = "1"

        # Create new supplier
        new_supplier = {
            "supplier_id": new_id,
            "name": name,
            "contact_email": contact_email,
            "address": address,
            "city": city,
            "state": state,
            "zip_code": zip_code,
            "country": country,
        }

        # Add to data
        suppliers[new_id] = new_supplier
        data["suppliers"] = suppliers

        return json.dumps({"success": True, "supplier": new_supplier})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_supplier",
                "description": "Creates a new supplier in the system.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "Supplier company name.",
        },
                        "contact_email": {
                            "type": "string",
                            "description": "Supplier contact email.",
        },
                        "address": {
                            "type": "string",
                            "description": "Street address.",
        },
                        "city": {
                            "type": "string",
                            "description": "City.",
        },
                        "state": {
                            "type": "string",
                            "description": "State/Province.",
        },
                        "zip_code": {
                            "type": "string",
                            "description": "ZIP/Postal code.",
        },
                        "country": {
                            "type": "string",
                            "description": "Country.",
        },
        },
                    "required": ["name", "contact_email", "address", "city", "state", "zip_code", "country"],
        },
        },
        }
