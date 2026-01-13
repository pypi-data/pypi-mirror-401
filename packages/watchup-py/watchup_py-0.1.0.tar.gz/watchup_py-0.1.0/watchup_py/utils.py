import traceback

def format_exception(exc: Exception) -> dict:
    return {
        "type": type(exc).__name__,
        "message": str(exc),
        "traceback": traceback.format_exc(),
    }
