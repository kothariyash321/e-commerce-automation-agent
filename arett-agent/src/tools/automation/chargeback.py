from src.tools.erp.s2k_ar import get_open_chargebacks


CHARGEBACK_REASON_MAP = {
    'SHORTAGE': 'auto_dispute',
    'EARLY_SHIP': 'auto_dispute',
    'LATE_SHIP': 'review',
    'ROUTING': 'auto_dispute',
    'LABEL_ERROR': 'review',
    'PRICE_DISCREPANCY': 'review',
    'DUPLICATE_PAYMENT': 'auto_dispute',
}


def submit_chargeback_dispute(chargeback_id: str, evidence: dict) -> dict:
    """Submits one chargeback dispute (stub)."""
    return {'ok': True, 'chargeback_id': chargeback_id, 'evidence_keys': sorted(evidence.keys())}


def run_chargeback_reconciliation(lookback_days: int = 30) -> dict:
    """Runs chargeback workflow and returns summary counts."""
    open_items = get_open_chargebacks(lookback_days=lookback_days)
    auto_disputed = 0
    escalated = 0
    total_amount_disputed = 0.0
    for cb in open_items:
        reason = cb.get('reason') or cb.get('reason_code')
        strategy = CHARGEBACK_REASON_MAP.get(reason, 'review')
        if strategy == 'auto_dispute':
            submit_chargeback_dispute(cb.get('chargebackId', 'unknown'), {'orderNumber': cb.get('orderNumber', ''), 'tracking': cb.get('tracking', '')})
            auto_disputed += 1
            total_amount_disputed += float(cb.get('amount', 0) or 0)
        else:
            escalated += 1
    return {'auto_disputed': auto_disputed, 'escalated': escalated, 'total_amount_disputed': round(total_amount_disputed, 2)}
