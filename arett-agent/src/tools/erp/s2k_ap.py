from src.tools.erp.s2k_client import S2KClient


def get_open_purchase_orders() -> list[dict]:
    """Gets open purchase orders from S2K /orders/purchase."""
    data = S2KClient().get('/orders/purchase', {'status': 'OPEN'})
    return data.get('purchaseOrders', data if isinstance(data, list) else [])
