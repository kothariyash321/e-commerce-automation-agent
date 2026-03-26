def route_task(task: str) -> str:
    """Routes a task to a workflow family."""
    lower = task.lower()
    if 'chargeback' in lower:
        return 'automation.chargeback'
    if 'catalog' in lower or 'suppression' in lower:
        return 'marketplace.catalog_health'
    if 'inventory' in lower:
        return 'marketplace.inventory'
    return 'general'
