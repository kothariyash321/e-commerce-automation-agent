from src.tools.erp.s2k_client import S2KClient


def get_s2k_inventory(sku_list: list[str] | None = None) -> list[dict]:
    """Gets inventory from S2K /inventory/items and optional SKU filter."""
    data = S2KClient().get('/inventory/items')
    items = data.get('items', data if isinstance(data, list) else [])
    if sku_list:
        return [i for i in items if i.get('itemNumber') in set(sku_list)]
    return items
