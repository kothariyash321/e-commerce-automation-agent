from src.tools.erp.s2k_client import S2KClient


def get_s2k_price(sku: str) -> float | None:
    """Gets list price for SKU from S2K item record."""
    data = S2KClient().get(f'/items/{sku}')
    return data.get('listPrice')
