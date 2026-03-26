def get_channel_performance(days: int = 30) -> list[dict]:
    """Returns channel performance rows as plain dicts."""
    _ = days
    return [
        {'channel': 'amazon_sc', 'revenue': 10000.0, 'units': 220, 'margin_pct': 30.2, 'returns': 12, 'net_revenue': 9500.0},
        {'channel': 'walmart', 'revenue': 7000.0, 'units': 160, 'margin_pct': 28.5, 'returns': 7, 'net_revenue': 6700.0},
    ]
