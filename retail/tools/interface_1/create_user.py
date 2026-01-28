import json
import re
from typing import Any, Dict
from tau_bench.envs.tool import Tool


class CreateUser(Tool):
    """Creates a new user account."""

    @staticmethod
    def invoke(
        data: Dict[str, Any],
        first_name: str,
        last_name: str,
        email: str,
        address: str,
        city: str,
        state: str,
        zip_code: str,
        country: str,
    ) -> str:

        # Validate data structure
        if not isinstance(data, dict):
            return json.dumps({"success": False, "error": "Invalid data format"})

        users = data.get("users", {})

        # Validate required fields
        if not all([first_name, last_name, email, address, city, state, zip_code, country]):
            return json.dumps({"success": False, "error": "All fields are required"})

        # Validate email format
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            return json.dumps({"success": False, "error": "Invalid email format"})

        # Trim whitespace from text fields
        first_name = first_name.strip()
        last_name = last_name.strip()
        address = address.strip()
        city = city.strip()
        state = state.strip()
        zip_code = zip_code.strip()
        country = country.strip()

        # Check for duplicate email
        for uid, user in users.items():
            if isinstance(user, dict) and user.get("email", "").lower() == email.lower():
                return json.dumps({
                    "success": False,
                    "error": f"User with email '{email}' already exists (ID: {uid})"
                })

        # Generate new user_id
        if users:
            new_id = str(max(int(k) for k in users.keys()) + 1)
        else:
            new_id = "1"

        # Create new user
        new_user = {
            "user_id": new_id,
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "address": address,
            "city": city,
            "state": state,
            "zip_code": zip_code,
            "country": country,
        }

        # Add to data
        users[new_id] = new_user
        data["users"] = users

        return json.dumps({"success": True, "user": new_user})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_user",
                "description": "Creates a new user account.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "first_name": {
                            "type": "string",
                            "description": "User's first name.",
        },
                        "last_name": {
                            "type": "string",
                            "description": "User's last name.",
        },
                        "email": {
                            "type": "string",
                            "description": "User's email (unique).",
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
                    "required": ["first_name", "last_name", "email", "address", "city", "state", "zip_code", "country"],
        },
        },
        }
