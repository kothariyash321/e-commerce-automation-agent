TOOL_PROMPTS = {
    'get_catalog_health': 'Check listing health; call first before fixes; pass platforms and optional sku filter.',
    'auto_fix_issue': 'Fix one catalog issue only when auto_fixable=True from catalog health output.',
    'sync_inventory_to_platform': 'Push latest S2K qtyAvailable to one platform using sku/qty pairs.',
    'get_s2k_inventory': 'Read live S2K inventory and use qtyAvailable for sync operations.',
}
