TASK_CATALOG_HEALTH_CHECK = """
Run a full catalog health check.
1. Call get_catalog_health().
2. Auto-fix auto_fixable issues with auto_fix_issue().
3. Build escalation list and summary.
4. Send Teams escalation if needed.
"""

TASK_INVENTORY_SYNC = """
Sync S2K inventory to all platforms from qtyAvailable.
Track synced/skipped/errors by platform and send alerts for low stock.
"""

TASK_CHARGEBACK_RECONCILIATION = """
Run daily chargeback reconciliation, auto-dispute eligible reasons,
and escalate non-eligible reasons to finance.
"""
