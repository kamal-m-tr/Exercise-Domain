import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool


class TransferToHuman(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        reason: str,
    ) -> str:
        return json.dumps("Transfer successful")

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "transfer_to_human",
                "description": "Escalates to human support with the reason for escalation.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "reason": {
                            "type": "string",
                            "description": "The reason for escalating to human support.",
                        },
                    },
                    "required": [
                        "reason",
                    ],
                },
            },
        }
