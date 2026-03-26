def get_vc_orders(status: str = 'UNACKNOWLEDGED') -> list[dict]:
    """Gets open VC purchase orders (stub; wire SP-API credentials)."""
    return []


def acknowledge_vc_order(po_number: str, accepted: bool = True) -> dict:
    """Acknowledges a VC purchase order (stub)."""
    return {'po_number': po_number, 'accepted': accepted, 'ok': True}
