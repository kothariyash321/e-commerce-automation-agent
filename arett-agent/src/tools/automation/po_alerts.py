from src.tools.analytics.sku_performance import detect_stockout_risk
from src.tools.automation.notifications import send_alert


def run_po_gap_detection() -> list[dict]:
    """Finds stockout risks and emits Purchasing alert."""
    gap_items = detect_stockout_risk(days_ahead=30)
    if gap_items:
        send_alert(channel='teams_purchasing', severity='high', items=gap_items, message='PO gap risks detected')
    return gap_items
