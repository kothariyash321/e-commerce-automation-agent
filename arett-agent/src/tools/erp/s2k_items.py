from src.tools.erp.s2k_client import S2KClient


def get_items(status: str = 'A') -> list[dict]:
    """Gets S2K items from /items filtered by status."""
    data = S2KClient().get('/items', {'status': status})
    return data.get('items', data if isinstance(data, list) else [])
