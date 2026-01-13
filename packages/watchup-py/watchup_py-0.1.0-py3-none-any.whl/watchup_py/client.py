import uuid
import datetime
import traceback
import requests

DEFAULT_BASE_URL = "https://watchup-server.vercel.app"

class WatchupClient:
    def __init__(self, project_id: str, api_key: str, base_url: str = None):
        self.project_id = project_id
        self.api_key = api_key
        self.base_url = base_url or DEFAULT_BASE_URL
        self.authenticated = False

    def login(self):
        """Perform SDK auth and mark client as initialized."""
        if self.authenticated:
            return

        url = f"{self.base_url}/system/sdk/auth"
        headers = {
            "Content-Type": "application/json",
            "X-Watchup-Project": self.project_id,
            "X-Watchup-Key": self.api_key
        }

        try:
            resp = requests.post(url, headers=headers, json={}, timeout=20)
            resp.raise_for_status()
            self.authenticated = True
        except Exception as e:
            # Fail silently but log
            print(f"[WatchupClient] Auth failed: {e}")
            self.authenticated = False

    def capture_exception(self, exc: Exception, context: dict = None):
        """
        Send exception details to /v1/capture with required headers.
        Performs auth first if needed.
        """
        if not self.authenticated:
            self.login()

        context = context or {}
        timestamp = context.get("timestamp")
        started_at = datetime.datetime.now()
        if timestamp:
            try:
                started_at = datetime.datetime.fromisoformat(timestamp)
            except Exception:
                pass

        payload = {
            "type": type(exc).__name__,
            "message": str(exc),
            "stack": traceback.format_exc(),
            "componentStack": context.get("componentStack", ""),
            "url": context.get("url", ""),
            "userAgent": context.get("userAgent", ""),
            "timestamp": started_at.isoformat()
        }

        headers = {
            "Content-Type": "application/json",
            "X-Watchup-Project": self.project_id,
            "X-Watchup-Key": self.api_key
        }

        try:
            resp = requests.post(f"{self.base_url}/v1/capture", headers=headers, json=payload, timeout=20)
            resp.raise_for_status()
            return resp.json()  # Returns {"ok": True, "id": "<incident_id>"}
        except Exception as e:
            print(f"[WatchupClient] Failed to capture exception: {e}")
            return None
