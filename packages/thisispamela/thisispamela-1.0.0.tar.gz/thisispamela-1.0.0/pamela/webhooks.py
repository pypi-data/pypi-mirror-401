"""
Webhook verification utilities for Pamela B2B.
"""

import hmac
import hashlib
import json
from typing import Union, Dict, Any


def verify_webhook_signature(
    payload: Union[str, Dict[str, Any]],
    signature: str,
    secret: str,
) -> bool:
    """
    Verify webhook signature.

    Args:
        payload: Webhook payload (dict or JSON string)
        signature: Signature from X-Pamela-Signature header
        secret: Webhook secret

    Returns:
        True if signature is valid
    """
    if isinstance(payload, dict):
        payload_str = json.dumps(payload, sort_keys=True)
    else:
        payload_str = payload

    expected_signature = hmac.new(
        secret.encode("utf-8"),
        payload_str.encode("utf-8"),
        hashlib.sha256
    ).hexdigest()

    return hmac.compare_digest(expected_signature, signature)


def create_tool_handler(secret: str):
    """
    Create a decorator for FastAPI/Flask tool webhook handlers.

    Example:
        @create_tool_handler(WEBHOOK_SECRET)
        async def handle_tool(request):
            tool_name = request.json["tool_name"]
            arguments = request.json["arguments"]
            # Execute tool and return result
            return {"result": "..."}
    """
    def decorator(handler):
        async def wrapper(request):
            signature = request.headers.get("X-Pamela-Signature")
            payload = request.json if hasattr(request, "json") else request.get_json()

            if not verify_webhook_signature(payload, signature, secret):
                return {"error": "Invalid signature"}, 401

            return await handler(payload)

        return wrapper
    return decorator

