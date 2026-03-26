from datetime import date, timedelta

from src.tools.erp.s2k_client import S2KClient


def get_sku_performance(sku: str, days: int = 90) -> dict:
    """Calculates SKU metrics from S2K sales history response."""
    today = date.today()
    history = S2KClient().get('/analytics/sales/history', {
        'itemNumber': sku,
        'dateFrom': (today - timedelta(days=days)).isoformat(),
        'dateTo': today.isoformat(),
    })
    rows = history.get('rows', history if isinstance(history, list) else [])
    units = sum(float(r.get('qtyShipped', 0)) for r in rows)
    revenue = sum(float(r.get('extPrice', 0)) for r in rows)
    cost = sum(float(r.get('cost', 0)) for r in rows)
    margin_pct = ((revenue - cost) / revenue * 100) if revenue else 0.0
    avg_weekly_velocity = units / max(days / 7, 1)
    return {
        'sku': sku,
        'total_units_sold': int(units),
        'total_revenue': round(revenue, 2),
        'total_cost': round(cost, 2),
        'gross_margin_pct': round(margin_pct, 2),
        'avg_weekly_velocity': round(avg_weekly_velocity, 2),
    }


def detect_slow_movers(threshold_weeks: int = 12) -> list[dict]:
    """Returns slow movers stub dataset."""
    return [{'sku': 'SKU-DEMO-001', 'days_of_supply': threshold_weeks * 8}]


def detect_stockout_risk(days_ahead: int = 30) -> list[dict]:
    """Returns stockout risk stub dataset."""
    return [{'sku': 'SKU-DEMO-002', 'days_of_supply': max(days_ahead - 5, 0)}]
