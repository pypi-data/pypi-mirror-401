from flask import request
from watchup_py.client import WatchupClient

class WatchupErrorMiddleware:
    def __init__(self, app, client: WatchupClient):
        self.app = app
        self.client = client
        self.register_error_handler()

    def register_error_handler(self):
        @self.app.errorhandler(Exception)
        def handle_exception(e):
            context = {
                "url": request.url,
                "userAgent": request.headers.get("User-Agent", ""),
            }
            self.client.capture_exception(e, context)
            return {"error": "Internal server error"}, 500
