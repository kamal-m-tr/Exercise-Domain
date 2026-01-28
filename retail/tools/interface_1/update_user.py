import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool


class UpdateUser(Tool):
    """Updates user information."""

    @staticmethod
    def invoke(
        data: Dict[str, Any],
        user_id: str,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        email: Optional[str] = None,
        address: Optional[str] = None,
        city: Optional[str] = None,
        state: Optional[str] = None,
        zip_code: Optional[str] = None,
        country: Optional[str] = None,
    ) -> str:

        # Validate data structure
        if not isinstance(data, dict):
            return json.dumps({"success": False, "error": "Invalid data format"})

        users = data.get("users", {})

        # Validate required field
        if not user_id:
            return json.dumps({"success": False, "error": "user_id is required"})

        # Find user
        user = users.get(str(user_id))
        if not user:
            return json.dumps({
                "success": False,
                "error": f"User with ID '{user_id}' not found"
            })

        # Check if any update field provided
        update_fields = {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "address": address,
            "city": city,
            "state": state,
            "zip_code": zip_code,
            "country": country,
        }

        has_update = any(v is not None for v in update_fields.values())
        if not has_update:
            return json.dumps({"success": False, "error": "No update fields provided"})

        # Check for duplicate email if email is being updated
        if email:
            for uid, u in users.items():
                if uid != str(user_id) and isinstance(u, dict) and u.get("email", "").lower() == email.lower():
                    return json.dumps({
                        "success": False,
                        "error": f"User with email '{email}' already exists (ID: {uid})"
                    })

        # Apply updates
        for field, value in update_fields.items():
            if value is not None:
                user[field] = value

        return json.dumps({"success": True, "user": user})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_user",
                "description": "Updates user information.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {
                            "type": "string",
                            "description": "The user's unique identifier.",
                        },
                        "first_name": {
                            "type": "string",
                            "description": "New first name.",
                        },
                        "last_name": {
                            "type": "string",
                            "description": "New last name.",
                        },
                        "email": {
                            "type": "string",
                            "description": "New email.",
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
                    "required": ["user_id"],
                },
            },
        }
