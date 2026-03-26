from src.tools.marketplace.catalog_health import auto_fix_issue, run_catalog_health_check
from src.tools.erp.s2k_inventory import get_s2k_inventory
from src.tools.analytics.sku_performance import get_sku_performance
from src.tools.automation.chargeback import run_chargeback_reconciliation, submit_chargeback_dispute
from src.tools.automation.notifications import send_alert
from src.tools.analytics.channel_performance import get_channel_performance


TOOL_REGISTRY = [
    {
        'name': 'get_catalog_health',
        'description': 'Checks listing health and returns suppressions, content issues, and auto-fixability.',
        'input_schema': {'type': 'object', 'properties': {'platforms': {'type': 'array', 'items': {'type': 'string'}}, 'sku_filter': {'type': 'string'}}},
    },
    {
        'name': 'auto_fix_issue',
        'description': 'Attempts to auto-fix one catalog issue using exact fields from get_catalog_health output.',
        'input_schema': {'type': 'object', 'required': ['sku', 'platform', 'issue_type'], 'properties': {'sku': {'type': 'string'}, 'platform': {'type': 'string'}, 'issue_type': {'type': 'string'}}},
    },
    {
        'name': 'get_s2k_inventory',
        'description': 'Pulls current S2K inventory and uses qtyAvailable for marketplace sync.',
        'input_schema': {'type': 'object', 'properties': {'sku_list': {'type': 'array', 'items': {'type': 'string'}}}},
    },
    {
        'name': 'get_sku_performance',
        'description': 'Returns SKU performance metrics including velocity and gross margin.',
        'input_schema': {'type': 'object', 'required': ['sku'], 'properties': {'sku': {'type': 'string'}, 'days': {'type': 'integer', 'default': 90}}},
    },
    {
        'name': 'run_chargeback_reconciliation',
        'description': 'Runs chargeback workflow and auto-disputes eligible reasons.',
        'input_schema': {'type': 'object', 'properties': {'lookback_days': {'type': 'integer', 'default': 30}}},
    },
    {
        'name': 'submit_chargeback_dispute',
        'description': 'Submits one chargeback dispute with required evidence payload.',
        'input_schema': {'type': 'object', 'required': ['chargeback_id', 'evidence'], 'properties': {'chargeback_id': {'type': 'string'}, 'evidence': {'type': 'object'}}},
    },
    {
        'name': 'send_alert',
        'description': 'Sends alerts to Teams or email channels with severity and impacted items.',
        'input_schema': {'type': 'object', 'required': ['channel', 'severity'], 'properties': {'channel': {'type': 'string'}, 'severity': {'type': 'string'}, 'items': {'type': 'array', 'items': {'type': 'object'}}, 'message': {'type': 'string'}}},
    },
]


TOOL_FUNCTIONS = {
    'get_catalog_health': run_catalog_health_check,
    'auto_fix_issue': auto_fix_issue,
    'get_s2k_inventory': get_s2k_inventory,
    'get_sku_performance': get_sku_performance,
    'run_chargeback_reconciliation': run_chargeback_reconciliation,
    'submit_chargeback_dispute': submit_chargeback_dispute,
    'send_alert': send_alert,
    'get_channel_performance': get_channel_performance,
}
