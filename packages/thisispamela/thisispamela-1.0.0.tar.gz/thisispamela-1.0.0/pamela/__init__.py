"""
Pamela B2B Voice API SDK for Python
"""

from pamela.client import PamelaClient
from pamela.webhooks import verify_webhook_signature

__all__ = ["PamelaClient", "verify_webhook_signature"]
__version__ = "1.0.0"

