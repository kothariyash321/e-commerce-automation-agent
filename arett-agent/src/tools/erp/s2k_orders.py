from src.tools.erp.s2k_client import S2KClient


def get_sales_orders(status: str = 'OPEN') -> list[dict]:
    """Reads sales orders from S2K /orders/sales."""
    data = S2KClient().get('/orders/sales', {'status': status})
    return data.get('orders', data if isinstance(data, list) else [])
