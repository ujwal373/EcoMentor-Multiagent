from utils.logger import log_to_file

def log_event(event: str, details: dict | None = None):
    entry = {"event": event, "details": details or {}}
    log_to_file(entry)
