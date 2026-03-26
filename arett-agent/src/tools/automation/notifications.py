def send_alert(channel: str, severity: str, items: list[dict] | None = None, message: str | None = None) -> dict:
    """Sends an alert payload to configured channel (stub)."""
    return {
        'sent': True,
        'channel': channel,
        'severity': severity,
        'item_count': len(items or []),
        'message': message,
    }
