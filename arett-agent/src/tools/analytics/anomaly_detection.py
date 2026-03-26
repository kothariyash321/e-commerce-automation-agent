from src.tools.analytics.sku_performance import detect_slow_movers, detect_stockout_risk


def run_anomaly_scan() -> dict:
    """Returns inventory anomalies including slow movers and stockout risks."""
    return {
        'slow_movers': detect_slow_movers(),
        'stockout_risks': detect_stockout_risk(),
    }
