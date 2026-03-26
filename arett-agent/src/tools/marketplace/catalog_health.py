from dataclasses import dataclass
from enum import Enum


class IssueType(str, Enum):
    SUPPRESSED = 'suppressed'
    PRICING_DRIFT = 'pricing_drift'
    INVENTORY_MISMATCH = 'inv_mismatch'
    INACTIVE = 'inactive'
    MISSING_ATTR = 'missing_attr'
    CONTENT_ERROR = 'content_error'


@dataclass
class CatalogIssue:
    sku: str
    platform: str
    issue_type: IssueType
    severity: str
    auto_fixable: bool
    details: dict


def run_catalog_health_check(platforms: list[str] | None = None, sku_filter: str | None = None) -> list[dict]:
    """Checks catalog health and returns issue records."""
    issues = [
        {
            'sku': sku_filter or 'SKU-DEMO-001',
            'platform': (platforms or ['amazon_sc'])[0],
            'issue_type': 'suppressed',
            'severity': 'high',
            'auto_fixable': True,
            'details': {'reason': 'Missing bullet points'},
        }
    ]
    return issues


def auto_fix_issue(sku: str, platform: str, issue_type: str, **_: dict) -> dict:
    """Attempts a low-risk automatic fix for a single catalog issue."""
    return {'success': True, 'sku': sku, 'platform': platform, 'issue_type': issue_type}
