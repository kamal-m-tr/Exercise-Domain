import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool


class GetUserInfo(Tool):
    """Retrieves user records by ID or email."""

    @staticmethod
    def invoke(
        data: Dict[str, Any],
        user_id: Optional[str] = None,
        email: Optional[str] = None,
    ) -> str:
        # Validate data structure
        if not isinstance(data, dict):
            return json.dumps({"success": False, "error": "Invalid data format"})

        users = data.get("users", {})

        if not isinstance(users, dict):
            return json.dumps({"success": False, "error": "Invalid users data structure"})

        # At least one identifier must be provided
        if not user_id and not email:
            return json.dumps({
                "success": False,
                "error": "At least one of (user_id, email) must be provided"
            })

        # Search by user_id
        if user_id:
            user = users.get(str(user_id))
            if user:
                return json.dumps({"success": True, "user": user})
            return json.dumps({
                "success": False,
                "error": f"User with user_id '{user_id}' not found"
            })

        # Search by email
        if email:
            for uid, user_data in users.items():
                if isinstance(user_data, dict) and user_data.get("email", "").lower() == email.lower():
                    return json.dumps({"success": True, "user": user_data})
            return json.dumps({
                "success": False,
                "error": f"User with email '{email}' not found"
            })

        return json.dumps({"success": False, "error": "No matching user found"})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_user_info",
                "description": "Retrieves user records by ID or email. At least one identifier must be provided.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {
                            "type": "string",
                            "description": "The user's unique identifier.",
                        },
                        "email": {
                            "type": "string",
                            "description": "The user's email address.",
                        },
                    },
                    "required": [],
                },
            },
        }
