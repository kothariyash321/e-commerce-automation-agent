from src.tools.erp.s2k_client import S2KClient


def get_open_chargebacks(lookback_days: int = 30) -> list[dict]:
    """Gets open chargebacks from S2K /ar/chargebacks."""
    data = S2KClient().get('/ar/chargebacks', {'status': 'OPEN', 'lookbackDays': lookback_days})
    return data.get('chargebacks', data if isinstance(data, list) else [])
