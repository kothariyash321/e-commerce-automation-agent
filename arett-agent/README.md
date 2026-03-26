# 🛒 E-Commerce AI Agent

> An open-source, production-ready AI agent that automates multi-channel e-commerce operations — catalog health, inventory sync, analytics, chargeback reconciliation, and cross-department workflows — using Claude (Anthropic), Python, and MCP.

---

## What This Is

This repo is a **complete, implementation-ready blueprint** for building an AI agent that can run the operational backbone of any multi-channel e-commerce distributor or retailer. It connects your ERP, your marketplace platforms, and your internal tools into a single intelligent system that monitors, fixes, reports, and alerts — automatically.

Built to be handed directly to [Cursor](https://cursor.sh) or any AI-assisted IDE and built from scratch. Every section contains exact file paths, function signatures, data models, API endpoints, and environment variable names.

---

## What It Automates

| Domain | What the agent does |
|---|---|
| **Marketplace operations** | Monitors catalog health across Amazon (VC + SC), Walmart, Wayfair, Home Depot, Lowes, BestBuy — auto-fixes suppressions, syncs inventory, confirms orders |
| **ERP integration** | Reads live inventory, pricing, orders, and AR/AP data from your ERP (VAI S2K or adaptable to any REST ERP) |
| **Analytics** | SKU performance, channel revenue, margin analysis, demand velocity, slow-mover detection, stockout prediction |
| **Finance automation** | Chargeback reconciliation — auto-disputes eligible chargebacks, escalates the rest with evidence pre-gathered |
| **Purchasing alerts** | Detects PO gaps and stockout risk, fires alerts to the purchasing team before you run out |
| **Reporting** | Builds weekly Excel reports, uploads to SharePoint, emails stakeholders |
| **MCP server** | Exposes all capabilities to Claude Desktop so anyone can invoke workflows with natural language |

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│           Orchestration Layer — Agent Core                  │
│     Claude API · task decomposition · tool routing          │
└──────────────┬───────────────────┬──────────────────────────┘
               │                   │                   │
    ┌──────────▼──────┐  ┌─────────▼──────┐  ┌────────▼────────┐
    │ Marketplace     │  │ Analytics      │  │ Automation      │
    │ Tools           │  │ Tools          │  │ Tools           │
    │ Amazon · Walmart│  │ SQL · ERP      │  │ Power Automate  │
    │ Wayfair · HD    │  │ exports · BI   │  │ Python · APIs   │
    └──────────┬──────┘  └─────────┬──────┘  └────────┬────────┘
               └──────────────┬────┘──────────────────┘
                    ┌──────────▼────────────────────────┐
                    │  Shared Infrastructure             │
                    │  MCP server · vector memory        │
                    │  ERP connector · audit log         │
                    └──────────┬────────────────────────┘
                               │
                    ┌──────────▼────────────────────────┐
                    │  External Systems                  │
                    │  Marketplace APIs · ERP · M365     │
                    └───────────────────────────────────┘
```

---

## Table of Contents

1. [Repository Structure](#1-repository-structure)
2. [Environment Variables & Dependencies](#2-environment-variables--dependencies)
3. [ERP Integration (VAI S2K)](#3-erp-integration-vai-s2k)
4. [Marketplace Tools](#4-marketplace-tools)
5. [Analytics Tools](#5-analytics-tools)
6. [Automation Tools](#6-automation-tools)
7. [Agent Core](#7-agent-core)
8. [MCP Server](#8-mcp-server-claude-desktop-integration)
9. [Database Schema](#9-database-schema)
10. [Scheduler](#10-scheduler)
11. [Prompt Library](#11-prompt-library)
12. [Testing](#12-testing)
13. [Build Order](#13-build-order-for-cursor)
14. [Pre-Build Checklist](#14-pre-build-checklist)

---

## 1. Repository Structure

```
ecomm-agent/
  .env.example                  # All env vars documented here (never commit .env)
  .env                          # Local secrets — gitignored
  requirements.txt
  README.md

  src/
    agent/
      __init__.py
      core.py                   # Main agent loop (plan → tool → observe)
      planner.py                # Task decomposition using Claude API
      memory.py                 # Short-term + long-term memory management
      router.py                 # Routes tasks to sub-agents
      prompts/
        system.py               # SYSTEM_PROMPT constant
        tasks.py                # Per-workflow task prompts
        tools.py                # Tool description strings for registry
        outputs.py              # Email/Teams/Slack output templates

    tools/
      __init__.py
      registry.py               # Central tool registry with JSON schemas
      marketplace/
        __init__.py
        amazon_vc.py            # Amazon Vendor Central SP-API
        amazon_sc.py            # Amazon Seller Central SP-API
        walmart.py              # Walmart Marketplace API
        wayfair.py              # Wayfair Supplier Portal API (GraphQL)
        home_depot.py           # Home Depot Supplier Gateway API
        lowes.py                # Lowes Item Management API
        bestbuy.py              # BestBuy Marketplace API
        catalog_health.py       # Cross-platform health monitor
      erp/
        __init__.py
        erp_client.py           # Generic ERP REST client (auth, retry, rate-limit)
        erp_inventory.py        # Inventory queries
        erp_orders.py           # Order queries
        erp_items.py            # Item/product master queries
        erp_pricing.py          # Pricing tier queries
        erp_ar.py               # Accounts Receivable queries
        erp_ap.py               # Accounts Payable queries
        erp_export.py           # Scheduled CSV/EDI export ingestion
      analytics/
        __init__.py
        sku_performance.py      # SKU-level margin, velocity, sell-through
        channel_performance.py  # Per-channel revenue, returns, trends
        anomaly_detection.py    # Price drift, stockout prediction, demand spikes
        report_builder.py       # Generates Excel/PDF reports
      automation/
        __init__.py
        chargeback.py           # Finance: chargeback reconciliation workflow
        po_alerts.py            # Purchasing: PO gap detection and alerts
        m365.py                 # Power Automate / SharePoint / Outlook integration
        notifications.py        # Multi-channel alert routing (email, Teams, Slack)

    mcp_server/
      __init__.py
      server.py                 # MCP server exposing all tools to Claude Desktop
      schemas/                  # JSON schema files for each tool

    db/
      __init__.py
      models.py                 # SQLAlchemy models
      migrations/               # Alembic migrations
      connection.py             # DB connection pool

    scheduler/
      __init__.py
      jobs.py                   # APScheduler job definitions
      cron.py                   # Entry point for scheduled runs

    utils/
      __init__.py
      logger.py                 # Structured logging
      retry.py                  # Exponential backoff decorator
      cache.py                  # Redis/in-memory caching

  tests/
    unit/
    integration/
    fixtures/

  scripts/
    seed_test_data.py
    backfill_history.py
```

---

## 2. Environment Variables & Dependencies

### `.env.example`

```bash
# ── Anthropic / LLM ──────────────────────────────────────────
ANTHROPIC_API_KEY=sk-ant-...
CLAUDE_MODEL=claude-sonnet-4-20250514
CLAUDE_MAX_TOKENS=4096

# ── ERP (VAI S2K — adapt base URL for your instance) ─────────
ERP_BASE_URL=https://your-instance.erp-provider.net/api/v1
ERP_API_KEY=                          # Bearer token
ERP_CLIENT_ID=                        # OAuth client ID (if OAuth flow)
ERP_CLIENT_SECRET=
ERP_COMPANY_CODE=01
ERP_WAREHOUSE_CODE=01
ERP_EXPORT_SFTP_HOST=
ERP_EXPORT_SFTP_USER=
ERP_EXPORT_SFTP_KEY_PATH=./keys/erp_sftp.pem
ERP_EXPORT_DROP_PATH=./data/erp_exports/

# ── Amazon Vendor Central (SP-API) ───────────────────────────
AMAZON_VC_CLIENT_ID=
AMAZON_VC_CLIENT_SECRET=
AMAZON_VC_REFRESH_TOKEN=
AMAZON_VC_MARKETPLACE_ID=ATVPDKIKX0DER
AMAZON_VC_VENDOR_CODE=

# ── Amazon Seller Central (SP-API) ───────────────────────────
AMAZON_SC_CLIENT_ID=
AMAZON_SC_CLIENT_SECRET=
AMAZON_SC_REFRESH_TOKEN=
AMAZON_SC_MARKETPLACE_ID=ATVPDKIKX0DER
AMAZON_SC_SELLER_ID=

# ── Walmart Marketplace ───────────────────────────────────────
WALMART_CLIENT_ID=
WALMART_CLIENT_SECRET=
WALMART_CHANNEL_TYPE=WALMART_US

# ── Wayfair ───────────────────────────────────────────────────
WAYFAIR_CLIENT_ID=
WAYFAIR_CLIENT_SECRET=
WAYFAIR_SUPPLIER_ID=

# ── Home Depot ────────────────────────────────────────────────
HOME_DEPOT_API_KEY=
HOME_DEPOT_VENDOR_ID=

# ── Lowes ─────────────────────────────────────────────────────
LOWES_API_KEY=
LOWES_VENDOR_ID=

# ── BestBuy ───────────────────────────────────────────────────
BESTBUY_API_KEY=
BESTBUY_VENDOR_ID=

# ── Database ──────────────────────────────────────────────────
DATABASE_URL=postgresql://user:password@localhost:5432/ecomm_agent
REDIS_URL=redis://localhost:6379/0

# ── Microsoft 365 ─────────────────────────────────────────────
M365_TENANT_ID=
M365_CLIENT_ID=
M365_CLIENT_SECRET=
M365_SHAREPOINT_SITE_ID=
POWER_AUTOMATE_WEBHOOK_URL=

# ── Notifications ─────────────────────────────────────────────
SLACK_WEBHOOK_URL=
TEAMS_WEBHOOK_URL=
ALERT_EMAIL_FROM=agent@yourdomain.com
ALERT_EMAIL_TO=ops@yourdomain.com

# ── MCP Server ────────────────────────────────────────────────
MCP_SERVER_HOST=0.0.0.0
MCP_SERVER_PORT=8765
MCP_AUTH_TOKEN=
```

### `requirements.txt`

```
# LLM & Agent
anthropic>=0.49.0
langchain>=0.3.0
langgraph>=0.2.0

# MCP Server
mcp>=1.0.0

# HTTP & API
httpx>=0.27.0
requests>=2.31.0
python-amazon-sp-api>=1.0.0

# Database
sqlalchemy>=2.0.0
alembic>=1.13.0
psycopg2-binary>=2.9.0
redis>=5.0.0

# Data processing
pandas>=2.2.0
numpy>=1.26.0
openpyxl>=3.1.0

# Scheduling
APScheduler>=3.10.0

# M365
msal>=1.28.0
O365>=2.0.35

# Utilities
python-dotenv>=1.0.0
pydantic>=2.6.0
structlog>=24.0.0
tenacity>=8.3.0
paramiko>=3.4.0

# Testing
pytest>=8.0.0
pytest-asyncio>=0.23.0
respx>=0.21.0
```

---

## 3. ERP Integration (VAI S2K)

This system is built against **VAI S2K Enterprise** (REST API with Bearer token auth, JSON responses). The ERP client pattern is generic enough to adapt to any REST ERP — just swap the base URL and field name mappings in `erp_client.py`.

### Base Client (`src/tools/erp/erp_client.py`)

```python
import httpx
import os
from tenacity import retry, stop_after_attempt, wait_exponential

class ERPClient:
    BASE_URL = os.getenv("ERP_BASE_URL")
    API_KEY  = os.getenv("ERP_API_KEY")

    def __init__(self):
        self.client = httpx.Client(
            base_url=self.BASE_URL,
            headers={
                "Authorization": f"Bearer {self.API_KEY}",
                "Content-Type": "application/json",
                "Accept": "application/json",
            },
            timeout=30.0,
        )

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=10))
    def get(self, path: str, params: dict = None) -> dict:
        resp = self.client.get(path, params=params)
        resp.raise_for_status()
        return resp.json()

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=10))
    def post(self, path: str, body: dict) -> dict:
        resp = self.client.post(path, json=body)
        resp.raise_for_status()
        return resp.json()
```

### ERP Endpoints & Data Fields

> **Note:** All paths below are relative to `ERP_BASE_URL`. These follow VAI S2K REST connector conventions. Confirm exact paths against your ERP instance's API documentation.

#### Inventory

| Endpoint | Method | Key Response Fields | Used For |
|---|---|---|---|
| `/inventory/items` | GET | `itemNumber, warehouseCode, qtyOnHand, qtyCommitted, qtyAvailable, qtyOnOrder, reorderPoint, reorderQty, unitCost, lastReceiptDate` | Real-time stock levels for marketplace sync |
| `/inventory/items/{itemNumber}` | GET | Same + `lotNumber, expirationDate, binLocation, weight, dimensions` | Single-SKU lookup |
| `/inventory/adjustments` | POST | `itemNumber, warehouseCode, adjustQty, reason, referenceNumber` | Record manual adjustments |
| `/inventory/transfers` | GET | `fromWarehouse, toWarehouse, itemNumber, qty, transferDate, status` | In-transit inventory |

#### Items / Product Master

| Endpoint | Method | Key Response Fields | Used For |
|---|---|---|---|
| `/items` | GET | `itemNumber, itemDescription, vendorItemNumber, upc, ean, productClass, productLine, weight, height, length, width, listPrice, stdCost, status (A/I)` | Catalog master data for marketplace listings |
| `/items/{itemNumber}` | GET | Full record + `extendedDescription, keywords, imageURL, countryOfOrigin, harmonizedCode` | Detailed product data |
| `/items/{itemNumber}/pricing` | GET | `priceLevel (1-9), unitPrice, effectiveDate, breakQuantity` | Price tier lookups |
| `/items/search` | GET | Params: `keyword, productClass, vendorNumber, status` | Bulk catalog queries |

#### Orders — Sales

| Endpoint | Method | Key Response Fields | Used For |
|---|---|---|---|
| `/orders/sales` | GET | `orderNumber, customerNumber, orderDate, shipDate, status, lines[itemNumber, qty, unitPrice, extPrice, shipQty, backorderQty]` | Pull open/recent sales orders |
| `/orders/sales/{orderNumber}` | GET | Full order + `shipmentTracking, freightCharges, promisedDate` | Fulfillment confirmation |
| `/orders/sales` | POST | Body: `customerNumber, poNumber, shipToAddress, lines[]` | Create order from marketplace import |
| `/orders/returns` | GET | `rmaNumber, originalOrderNumber, itemNumber, returnQty, reason, creditAmount` | Return and credit memo data |

#### Orders — Purchase

| Endpoint | Method | Key Response Fields | Used For |
|---|---|---|---|
| `/orders/purchase` | GET | `poNumber, vendorNumber, orderDate, expectedDate, status, lines[itemNumber, qtyOrdered, qtyReceived, unitCost]` | Open POs for inventory forecasting |
| `/orders/purchase/{poNumber}/receipts` | GET | `receiptDate, itemNumber, qtyReceived, lotNumber, binLocation` | Receiving data |

#### Accounts Receivable

| Endpoint | Method | Key Response Fields | Used For |
|---|---|---|---|
| `/ar/invoices` | GET | `invoiceNumber, customerNumber, invoiceDate, dueDate, amount, balance, status, poNumber, orderNumber` | Invoice matching for chargeback reconciliation |
| `/ar/chargebacks` | GET | `chargebackId, customerNumber, invoiceNumber, chargebackDate, amount, reason, status` | Open chargebacks |
| `/ar/chargebacks/{id}/dispute` | POST | Body: `responseText, attachments[], disputeReason` | Submit dispute |

#### Analytics

| Endpoint | Method | Key Response Fields | Used For |
|---|---|---|---|
| `/analytics/sales/history` | GET | Params: `itemNumber, dateFrom, dateTo`; Returns: `invoiceDate, itemNumber, qtyShipped, unitPrice, extPrice, cost, margin` | SKU performance |
| `/analytics/inventory/turnover` | GET | `itemNumber, avgQtyOnHand, totalCOGS, turnoverRate, daysOnHand` | Slow-mover identification |
| `/analytics/sales/byChannel` | GET | `customerNumber, channel, totalRevenue, totalUnits, avgOrderValue` | Channel-level performance |

### Channel → ERP Customer Number Mapping

Map each marketplace to its corresponding ERP customer number. Store this in your database and populate `CHANNEL_BUYER_MAP` in `channel_performance.py`:

```python
CHANNEL_BUYER_MAP = {
    'amazon_vc':   os.getenv('ERP_AMAZON_VC_CUSTOMER'),
    'amazon_sc':   os.getenv('ERP_AMAZON_SC_CUSTOMER'),
    'walmart':     os.getenv('ERP_WALMART_CUSTOMER'),
    'wayfair':     os.getenv('ERP_WAYFAIR_CUSTOMER'),
    'home_depot':  os.getenv('ERP_HD_CUSTOMER'),
    'lowes':       os.getenv('ERP_LOWES_CUSTOMER'),
    'bestbuy':     os.getenv('ERP_BESTBUY_CUSTOMER'),
}
```

### Scheduled CSV/EDI Export Fallback

If REST API access is limited, most ERPs can export flat files via SFTP. This is the fallback pipeline:

| Export File | Key Fields | Refresh Frequency |
|---|---|---|
| `INVBAL.csv` | `ITEM_NO, WHSE, QTY_ON_HAND, QTY_AVAIL, QTY_COMMIT, QTY_ON_ORDER, UNIT_COST` | Every 2 hours |
| `ITMAST.csv` | `ITEM_NO, DESCR, UPC, VENDOR_ITEM, PROD_CLASS, LIST_PRICE, STD_COST, STATUS, WEIGHT, DIM_H/L/W` | Daily at 2am |
| `SLSHIST.csv` | `INVOICE_NO, ITEM_NO, CUST_NO, INV_DATE, QTY_SHIP, UNIT_PRICE, EXT_PRICE, COST, MARGIN_PCT` | Daily at 3am |
| `OPNORD.csv` | `ORD_NO, CUST_NO, ORD_DATE, SHIP_DATE, STATUS, ITEM_NO, QTY_ORD, QTY_SHIP, QTY_BO` | Every 30 minutes |
| `AROPEN.csv` | `INVOICE_NO, CUST_NO, INV_DATE, DUE_DATE, AMOUNT, BALANCE, PO_NO` | Daily at 4am |
| `CHGBK.csv` | `CHGBK_ID, CUST_NO, INV_NO, CHGBK_DATE, AMOUNT, REASON, STATUS` | Daily at 5am |

```python
# src/tools/erp/erp_export.py
import paramiko, pandas as pd, os

EXPORT_FILES = {
    "INVBAL":  "inventory_balances",
    "ITMAST":  "item_master",
    "SLSHIST": "sales_history",
    "OPNORD":  "open_orders",
    "AROPEN":  "ar_open",
    "CHGBK":   "chargebacks",
}

def sync_exports():
    sftp = _connect_sftp()
    for filename, table in EXPORT_FILES.items():
        local = _download(sftp, filename)
        df = pd.read_csv(local)
        _upsert(df, table)
```

---

## 4. Marketplace Tools

### Amazon SP-API (Vendor Central + Seller Central)

Uses the `python-amazon-sp-api` library. Both VC and SC share the same OAuth flow.

| Function | SP-API Endpoint | Purpose |
|---|---|---|
| `get_vc_orders()` | `vendor/orders/v1/purchaseOrders` | Pull open POs from Amazon VC |
| `acknowledge_vc_order(po_number)` | `vendor/orders/v1/purchaseOrders/acknowledgement` | Send EDI 855 acknowledgment |
| `confirm_vc_shipment(po_number, tracking)` | `vendor/directFulfillment/shipping/v1/shippingLabels` | Confirm shipment with tracking |
| `get_sc_listings()` | `listings/2021-08-01/items/{sellerId}` | Get all active SC listings |
| `fix_sc_suppression(sku, attrs)` | `listings/2021-08-01/items/{sellerId}/{sku}` | PATCH listing to resolve suppression |
| `update_sc_inventory(sku, qty)` | `feeds/2021-06-30/feeds` (Inventory feed) | Update FBM inventory quantity |
| `get_sc_performance()` | `sales/v1/orderMetrics` | Sales metrics by ASIN |

```python
# src/tools/marketplace/amazon_vc.py
from sp_api.api import Vendors
from sp_api.base import Marketplaces, Credentials
import os

CREDS = Credentials(
    refresh_token=os.getenv('AMAZON_VC_REFRESH_TOKEN'),
    lwa_app_id=os.getenv('AMAZON_VC_CLIENT_ID'),
    lwa_client_secret=os.getenv('AMAZON_VC_CLIENT_SECRET'),
)

def get_vc_orders(status='UNACKNOWLEDGED') -> list[dict]:
    """Returns open POs from Amazon Vendor Central."""
    api = Vendors(credentials=CREDS, marketplace=Marketplaces.US)
    resp = api.get_purchase_orders(purchaseOrderState=status, limit=100)
    return resp.payload.get('orders', [])

def acknowledge_vc_order(po_number: str, accepted: bool = True) -> dict:
    """Sends EDI 855 acknowledgment for a VC purchase order."""
    api = Vendors(credentials=CREDS, marketplace=Marketplaces.US)
    return api.submit_acknowledgement(purchaseOrders=[{
        'purchaseOrderNumber': po_number,
        'vendorOrderNumber': po_number,
        'acknowledgementDate': datetime.utcnow().isoformat(),
        'acknowledgementCode': 'ACCEPTED' if accepted else 'REJECTED',
    }])
```

### Walmart Marketplace API

| Function | Endpoint | Purpose |
|---|---|---|
| `get_walmart_items()` | `GET /v3/items` | All listings and publish status |
| `update_walmart_item(sku, attrs)` | `PUT /v3/items/{sku}` | Update item attributes |
| `update_walmart_inventory(sku, qty)` | `PUT /v3/inventory?sku={sku}` | Push inventory quantity |
| `update_walmart_price(sku, price)` | `PUT /v3/price` | Update item price |
| `get_walmart_orders(status)` | `GET /v3/orders?status={status}` | Fetch orders by status |
| `acknowledge_walmart_order(order_id)` | `POST /v3/orders/{orderId}/acknowledge` | Acknowledge order |
| `ship_walmart_order(order_id, tracking)` | `POST /v3/orders/{orderId}/shipping` | Confirm shipment |

### Wayfair Supplier API (GraphQL)

Wayfair uses GraphQL, not REST. Base URL: `https://api.wayfair.com`

```graphql
# Get open purchase orders
query {
  purchaseOrders(limit: 50, offset: 0, hasResponse: false) {
    poNumber  poDate  status
    products { supplierId  quantity  price  estimatedShipDate }
  }
}

# Register PO (acknowledge)
mutation RegisterPO($poNumber: String!, $products: [ProductInput!]!) {
  register(poNumber: $poNumber, products: $products) { id  status }
}

# Send ASN
mutation SendASN($poNumber: String!, $tracking: TrackingInput!) {
  sendShipmentNotice(poNumber: $poNumber, tracking: $tracking) { id }
}

# Update inventory
mutation UpdateInventory($supplierId: String!, $qty: Int!) {
  updateInventory(supplierId: $supplierId, quantityOnHand: $qty) {
    supplierId  quantityOnHand
  }
}
```

### Home Depot, Lowes, BestBuy

Each uses a supplier-specific portal. API access is granted per-vendor. Core operations needed for all three:

- `get_listings()` — retrieve all listings
- `update_inventory(sku, qty)` — push stock levels
- `update_price(sku, price)` — update pricing
- `get_orders()` — pull open orders
- `acknowledge_order(id)` — confirm receipt
- `ship_order(id, tracking)` — confirm shipment
- `get_suppressed_items()` — items with listing errors

### Catalog Health Monitor (`src/tools/marketplace/catalog_health.py`)

```python
from dataclasses import dataclass
from enum import Enum

class IssueType(Enum):
    SUPPRESSED        = 'suppressed'
    PRICING_DRIFT     = 'pricing_drift'       # Platform price deviates from ERP list price
    INVENTORY_MISMATCH = 'inv_mismatch'       # Platform qty != ERP available qty
    INACTIVE          = 'inactive'            # Listing inactive but item active in ERP
    MISSING_ATTR      = 'missing_attr'        # Required attribute empty
    CONTENT_ERROR     = 'content_error'       # Platform-reported content error

@dataclass
class CatalogIssue:
    sku: str
    platform: str
    issue_type: IssueType
    severity: str       # 'low' | 'medium' | 'high'
    auto_fixable: bool
    details: dict

def run_catalog_health_check() -> list[CatalogIssue]:
    """
    Runs across all platforms. Returns list of issues.
    Scheduler calls this every 4 hours.
    Agent auto-fixes auto_fixable=True items; escalates the rest.
    """
    issues = []
    erp = ERPClient()
    erp_inventory = erp.get('/inventory/items')  # Ground truth
    erp_items = erp.get('/items')
    # ... compare against each platform and append issues
    return issues
```

---

## 5. Analytics Tools

### SKU Performance (`src/tools/analytics/sku_performance.py`)

```python
def get_sku_performance(sku: str, days: int = 90) -> dict:
    """
    Returns:
      total_units_sold, total_revenue, total_cost, gross_margin_pct,
      avg_weekly_velocity (units/week),
      sell_through_rate (units sold / (units sold + ending inventory)),
      days_of_supply (qtyAvailable / avg_weekly_velocity * 7),
      channel_mix (% revenue by marketplace),
      return_rate (return qty / shipped qty)
    """

def detect_slow_movers(threshold_weeks: int = 12) -> list[dict]:
    """Items with days_of_supply > threshold_weeks * 7. Flag for markdown."""

def detect_stockout_risk(days_ahead: int = 30) -> list[dict]:
    """Items where days_of_supply < days_ahead. Triggers PO alert."""
```

### Channel Performance (`src/tools/analytics/channel_performance.py`)

```python
def get_channel_performance(days: int = 30) -> pd.DataFrame:
    """
    Returns DataFrame:
      channel | revenue | units | margin_pct | returns | net_revenue | yoy_growth_pct
    Source: ERP /analytics/sales/byChannel filtered by buyer code
    """
```

### Report Builder (`src/tools/analytics/report_builder.py`)

```python
def build_weekly_ecomm_report() -> str:
    """
    Generates Excel workbook with 4 sheets:
      1. Executive Summary (channel revenue, units, margin, WoW/YoY)
      2. SKU Performance (top 50 + bottom 20 by revenue)
      3. Inventory Alerts (stockout risk + slow movers)
      4. Catalog Health (suppression count by platform vs. prior week)
    Uploads to SharePoint, returns SharePoint URL.
    """
```

---

## 6. Automation Tools

### Chargeback Reconciliation (`src/tools/automation/chargeback.py`)

```python
CHARGEBACK_REASON_MAP = {
    # Map reason codes to dispute strategy
    'SHORTAGE':           'auto_dispute',   # Dispute with BOL/tracking evidence
    'EARLY_SHIP':         'auto_dispute',   # Dispute with PO date proof
    'LATE_SHIP':          'review',         # Check carrier data first
    'ROUTING':            'auto_dispute',   # Dispute with routing confirmation
    'LABEL_ERROR':        'review',         # Needs human: pull original label
    'PRICE_DISCREPANCY':  'review',         # Needs human: ERP price vs PO price
    'DUPLICATE_PAYMENT':  'auto_dispute',
}

def run_chargeback_reconciliation() -> dict:
    """
    1. GET /ar/chargebacks?status=OPEN from ERP
    2. For each chargeback:
       a. GET /ar/invoices/{invoiceNumber} — original invoice
       b. GET /orders/sales/{orderNumber} — shipment + tracking
       c. Classify by reason code using CHARGEBACK_REASON_MAP
       d. If auto_dispute: gather evidence, POST /ar/chargebacks/{id}/dispute
       e. If review: add to escalation report
    3. Email Finance with summary + escalation list
    Returns: {auto_disputed: n, escalated: n, total_amount_disputed: float}
    """
```

### Purchase Order Gap Alerts (`src/tools/automation/po_alerts.py`)

```python
def run_po_gap_detection() -> list[dict]:
    """
    Flags items where:
    - days_of_supply < 30 AND no open PO exists in ERP, OR
    - Open PO expected receipt date is after projected stockout date

    Steps:
    1. GET /inventory/items (all items with qtyAvailable)
    2. Calculate days_of_supply from 90-day sales velocity
    3. GET /orders/purchase?status=OPEN (all open POs)
    4. Cross-reference: flag items with gaps
    5. send_alert(channel='teams_purchasing', severity='high', items=gap_items)
    """
```

### M365 Integration (`src/tools/automation/m365.py`)

```python
from O365 import Account
import httpx, os

def get_m365_account() -> Account:
    """Authenticates using client credentials (app-only) flow."""
    credentials = (os.getenv('M365_CLIENT_ID'), os.getenv('M365_CLIENT_SECRET'))
    account = Account(credentials, auth_flow_type='credentials',
                      tenant_id=os.getenv('M365_TENANT_ID'))
    account.authenticate()
    return account

def upload_to_sharepoint(local_path: str, folder: str) -> str:
    """Uploads file to SharePoint, returns web URL."""
    account = get_m365_account()
    sp = account.sharepoint()
    site = sp.get_site(os.getenv('M365_SHAREPOINT_SITE_ID'))
    drive = site.get_default_document_library()
    uploaded = drive.get_item_by_path(folder).upload_file(local_path)
    return uploaded.web_url

def trigger_power_automate(flow_webhook: str, payload: dict) -> bool:
    """Triggers a Power Automate flow via HTTP trigger webhook."""
    resp = httpx.post(flow_webhook, json=payload)
    return resp.status_code == 202

def send_email(to: list, subject: str, body_html: str, attachments: list = None):
    """Sends email via M365 mailbox."""
    account = get_m365_account()
    m = account.new_message()
    m.to.add(to)
    m.subject = subject
    m.body = body_html
    if attachments:
        for path in attachments:
            m.attachments.add(path)
    m.send()
```

---

## 7. Agent Core

### Tool Registry (`src/tools/registry.py`)

Every tool exposed to the agent must be registered with a JSON schema following the [Anthropic tool use spec](https://docs.anthropic.com/en/docs/build-with-claude/tool-use).

```python
TOOL_REGISTRY = [
  {
    "name": "get_catalog_health",
    "description": "Check catalog health across all marketplace platforms. Returns list of issues with severity and whether they are auto-fixable.",
    "input_schema": {
      "type": "object",
      "properties": {
        "platforms": {
          "type": "array",
          "items": {"type": "string"},
          "description": "Platforms to check. Defaults to all."
        },
        "sku_filter": {
          "type": "string",
          "description": "Optional: check specific SKU only"
        }
      }
    }
  },
  {
    "name": "get_sku_performance",
    "description": "Get sales performance metrics for a SKU: velocity, margin, sell-through, days of supply, channel mix.",
    "input_schema": {
      "type": "object",
      "required": ["sku"],
      "properties": {
        "sku": {"type": "string"},
        "days": {"type": "integer", "default": 90}
      }
    }
  },
  {
    "name": "run_chargeback_reconciliation",
    "description": "Run chargeback reconciliation against ERP AR. Auto-disputes eligible chargebacks and returns summary.",
    "input_schema": {"type": "object", "properties": {}}
  },
  {
    "name": "sync_inventory_to_platforms",
    "description": "Push current ERP inventory levels to all marketplace platforms.",
    "input_schema": {
      "type": "object",
      "properties": {
        "sku_list": {
          "type": "array",
          "items": {"type": "string"},
          "description": "SKUs to sync. Defaults to all active items."
        }
      }
    }
  },
  # ... register all tools from marketplace/, analytics/, automation/
]
```

### Agent Loop (`src/agent/core.py`)

```python
import anthropic
from tools.registry import TOOL_REGISTRY
from tools import execute_tool
from agent.prompts.system import SYSTEM_PROMPT

client = anthropic.Anthropic()

def run_agent(task: str, conversation_history: list = None) -> str:
    """Main agent loop. Runs until task complete or human input needed."""
    messages = conversation_history or []
    messages.append({'role': 'user', 'content': task})

    while True:
        response = client.messages.create(
            model=os.getenv('CLAUDE_MODEL', 'claude-sonnet-4-20250514'),
            max_tokens=int(os.getenv('CLAUDE_MAX_TOKENS', 4096)),
            system=SYSTEM_PROMPT,
            tools=TOOL_REGISTRY,
            messages=messages,
        )

        if response.stop_reason == 'end_turn':
            return response.content[0].text

        if response.stop_reason == 'tool_use':
            tool_results = []
            for block in response.content:
                if block.type == 'tool_use':
                    result = execute_tool(block.name, block.input)
                    tool_results.append({
                        'type': 'tool_result',
                        'tool_use_id': block.id,
                        'content': str(result)
                    })
            messages.append({'role': 'assistant', 'content': response.content})
            messages.append({'role': 'user', 'content': tool_results})
            continue

        break
    return 'Agent loop ended unexpectedly'
```

---

## 8. MCP Server (Claude Desktop Integration)

Once running, users can open Claude Desktop and say _"Check Amazon for suppressed listings and fix them"_ — the agent handles it end-to-end.

### Server (`src/mcp_server/server.py`)

```python
from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
import mcp.types as types
from tools.registry import TOOL_REGISTRY
from tools import execute_tool

server = Server('ecomm-agent')

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name=t['name'],
            description=t['description'],
            inputSchema=t['input_schema']
        ) for t in TOOL_REGISTRY
    ]

@server.call_tool()
async def handle_call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    result = execute_tool(name, arguments)
    return [types.TextContent(type='text', text=str(result))]

async def main():
    async with stdio_server() as (read, write):
        await server.run(read, write, InitializationOptions(
            server_name='ecomm-agent',
            server_version='1.0.0',
        ))

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
```

### Claude Desktop Config

Add to `~/.config/claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "ecomm-agent": {
      "command": "python",
      "args": ["/path/to/ecomm-agent/src/mcp_server/server.py"],
      "env": {
        "ANTHROPIC_API_KEY": "sk-ant-...",
        "ERP_BASE_URL": "https://your-instance.erp.net/api/v1",
        "ERP_API_KEY": "..."
      }
    }
  }
}
```

---

## 9. Database Schema

PostgreSQL. All ERP export data is mirrored locally for fast querying and cross-source analytics. Use Alembic for migrations.

```sql
-- Item master — mirrors ERP ITMAST export
CREATE TABLE item_master (
    item_number       VARCHAR(30) PRIMARY KEY,
    description       TEXT,
    upc               VARCHAR(20),
    vendor_item_no    VARCHAR(30),
    product_class     VARCHAR(10),
    list_price        NUMERIC(10,2),
    std_cost          NUMERIC(10,2),
    status            CHAR(1),          -- A=active, I=inactive
    weight            NUMERIC(8,3),
    dim_h             NUMERIC(8,3),
    dim_l             NUMERIC(8,3),
    dim_w             NUMERIC(8,3),
    last_synced       TIMESTAMP DEFAULT NOW()
);

-- Inventory balances — mirrors ERP INVBAL export
CREATE TABLE inventory_balances (
    id                SERIAL PRIMARY KEY,
    item_number       VARCHAR(30) REFERENCES item_master(item_number),
    warehouse_code    VARCHAR(10),
    qty_on_hand       INTEGER,
    qty_available     INTEGER,
    qty_committed     INTEGER,
    qty_on_order      INTEGER,
    unit_cost         NUMERIC(10,4),
    last_receipt_date DATE,
    snapshot_time     TIMESTAMP DEFAULT NOW()
);

-- Marketplace listing status per platform
CREATE TABLE marketplace_listings (
    id            SERIAL PRIMARY KEY,
    item_number   VARCHAR(30) REFERENCES item_master(item_number),
    platform      VARCHAR(30),   -- amazon_vc, amazon_sc, walmart, wayfair, etc.
    platform_sku  VARCHAR(100),
    asin          VARCHAR(20),
    status        VARCHAR(30),   -- active, suppressed, inactive, error
    issues        JSONB,
    last_checked  TIMESTAMP DEFAULT NOW()
);

-- Catalog health issues log
CREATE TABLE catalog_issues (
    id            SERIAL PRIMARY KEY,
    item_number   VARCHAR(30),
    platform      VARCHAR(30),
    issue_type    VARCHAR(50),
    severity      VARCHAR(10),
    auto_fixable  BOOLEAN,
    resolved      BOOLEAN DEFAULT FALSE,
    details       JSONB,
    detected_at   TIMESTAMP DEFAULT NOW(),
    resolved_at   TIMESTAMP
);

-- Agent audit log — every tool call and result
CREATE TABLE agent_audit_log (
    id            SERIAL PRIMARY KEY,
    tool_name     VARCHAR(100),
    inputs        JSONB,
    result        JSONB,
    success       BOOLEAN,
    error_msg     TEXT,
    duration_ms   INTEGER,
    executed_at   TIMESTAMP DEFAULT NOW()
);

-- Chargebacks
CREATE TABLE chargebacks (
    chargeback_id     VARCHAR(50) PRIMARY KEY,
    customer_number   VARCHAR(20),
    invoice_number    VARCHAR(30),
    chargeback_date   DATE,
    amount            NUMERIC(12,2),
    reason_code       VARCHAR(30),
    status            VARCHAR(20),   -- open, disputed, resolved
    dispute_strategy  VARCHAR(30),   -- auto_dispute, review
    disputed_at       TIMESTAMP,
    dispute_result    VARCHAR(20)
);
```

---

## 10. Scheduler

```python
# src/scheduler/jobs.py
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger

scheduler = BlockingScheduler()

scheduler.add_job(sync_erp_exports,        IntervalTrigger(hours=2),             id='erp_sync')
scheduler.add_job(run_catalog_health,      IntervalTrigger(hours=4),             id='catalog_health')
scheduler.add_job(sync_inventory,          IntervalTrigger(hours=2),             id='inv_sync')
scheduler.add_job(run_po_gap_detection,    CronTrigger(hour=7, minute=0),        id='po_gaps')
scheduler.add_job(run_chargeback_recon,    CronTrigger(hour=8, minute=0),        id='chargebacks')
scheduler.add_job(build_weekly_report,     CronTrigger(day_of_week='mon', hour=9), id='weekly_report')
scheduler.add_job(check_price_drift,       IntervalTrigger(hours=6),             id='price_drift')

if __name__ == '__main__':
    scheduler.start()
```

| Job | Schedule | What it does | Alert on failure |
|---|---|---|---|
| `sync_erp_exports` | Every 2 hours | Downloads ERP SFTP exports, upserts to Postgres | Teams webhook |
| `run_catalog_health` | Every 4 hours | Checks all platforms, auto-fixes low-severity issues | Teams + email |
| `sync_inventory` | Every 2 hours | Pushes ERP available qty to all marketplace platforms | Teams webhook |
| `run_po_gap_detection` | Daily 7am | Detects stockout risk, alerts Purchasing | Email to purchasing@ |
| `run_chargeback_recon` | Daily 8am | AR chargeback workflow, auto-disputes eligible items | Email to finance@ |
| `build_weekly_report` | Monday 9am | Excel report → SharePoint → email stakeholders | Email to leadership@ |
| `check_price_drift` | Every 6 hours | Flags platform prices deviating >5% from ERP list price | Teams webhook |

---

## 11. Prompt Library

All prompts live in `src/agent/prompts/`. There are four layers:

| Layer | File | When used |
|---|---|---|
| System prompt | `prompts/system.py` | Every single agent API call |
| Task prompts | `prompts/tasks.py` | When a scheduled job or user triggers a workflow |
| Tool descriptions | `prompts/tools.py` | Injected into each tool's `description` field in the registry |
| Output templates | `prompts/outputs.py` | When the agent generates emails, Teams messages, or escalations |

### System Prompt (`src/agent/prompts/system.py`)

```python
SYSTEM_PROMPT = '''
You are an AI Operations Agent for an e-commerce distribution company.
You are connected to the company ERP, marketplace platforms (Amazon, Walmart,
Wayfair, Home Depot, Lowes, BestBuy), and internal tools (M365, Slack, Teams).

REASONING PROCESS — follow this for every task:
1. State what you understand the task to be.
2. List the tools you plan to use and in what order.
3. Execute the tools.
4. Interpret the results — cite specific numbers, SKUs, order numbers.
5. State the outcome clearly: what was fixed, what needs human attention.

DATA STANDARDS:
- Always use the ERP as the source of truth for inventory, pricing, and cost.
- If a marketplace value conflicts with the ERP, flag it. Do not silently accept it.
- Currency: always USD. Never omit dollar signs on financial figures.
- Dates: always YYYY-MM-DD format.
- Quantities: integers only.
- Margins: express as percentage (e.g. 42.3%), not decimal.

ACTION RULES:
LOW-RISK — take automatically, no human approval needed:
  - Update item attributes (title, description, bullet points, images)
  - Sync inventory quantities from ERP to marketplace platforms
  - Acknowledge marketplace purchase orders
  - Send shipping confirmations with tracking numbers
  - Relist a suppressed item when the fix is a clear attribute correction
  - Submit chargeback disputes where reason = SHORTAGE, EARLY_SHIP, ROUTING,
    or DUPLICATE_PAYMENT and evidence is available in the ERP
  - Send scheduled reports and alerts

HIGH-RISK — ALWAYS require human confirmation first:
  - Price changes of more than 5% on any SKU
  - Cancelling or rejecting any customer purchase order
  - Creating new purchase orders in the ERP
  - Writing off inventory or adjusting cost
  - Chargeback disputes where reason = PRICE_DISCREPANCY, LABEL_ERROR, or LATE_SHIP
  - Deleting or deactivating any item from the ERP

OUTPUT FORMAT for reports to humans:
  - Lead with the headline number (e.g. "14 suppressions fixed, 2 escalated")
  - Structure: Actions Taken | Issues Found | Needs Attention
  - Include specific identifiers: SKU numbers, order numbers, dollar amounts
  - End with a clear next-step if human action is needed

CONSTRAINTS:
  - Never fabricate data. If a tool returns no results, say so.
  - Never guess inventory levels, prices, or order statuses. Always pull live data.
  - If a tool call fails after retries, escalate with the error message.
  - Every action is automatically logged. Do not skip logging.
'''
```

### Task Prompts (selected examples)

#### Catalog Health Check

```python
TASK_CATALOG_HEALTH_CHECK = '''
Run a full catalog health check across all marketplace platforms.

Steps:
1. Call get_catalog_health() for all platforms.
2. Group results by severity (high/medium/low) and by platform.
3. For every issue where auto_fixable = True:
   - Call auto_fix_issue(sku, platform, issue_type) immediately.
   - Log whether it succeeded or failed.
4. For issues where auto_fixable = False:
   - Collect into an escalation list.
   - Each entry must include: SKU, platform, issue_type, severity,
     and a plain-English explanation of what a human needs to do.
5. Report format:

   CATALOG HEALTH SUMMARY — {run_date}
   ─────────────────────────────────────
   Total issues found: {n}
   Auto-fixed: {n_fixed}
   Escalated to human: {n_escalated}

   By platform:
   {platform}: {n} issues ({n_fixed} fixed, {n_escalated} escalated)

   Escalation list:
   [{sku}] {platform} — {issue_type} — {severity} — {human_action_needed}

6. Send summary to Teams #ecommerce-ops if n_escalated > 0.
'''
```

#### Chargeback Reconciliation

```python
TASK_CHARGEBACK_RECONCILIATION = '''
Run the daily chargeback reconciliation for the Finance department.

Steps:
1. Call get_open_chargebacks() from ERP AR.
2. For each chargeback:
   a. Call get_invoice(invoice_number) for the original invoice.
   b. Call get_order(order_number) for shipment and tracking data.
   c. Classify by reason code:
      SHORTAGE      → auto_dispute (BOL/carrier scan confirms delivery)
      EARLY_SHIP    → auto_dispute (ship date matches PO window)
      ROUTING       → auto_dispute (routing confirmation exists)
      DUPLICATE     → auto_dispute (payment already applied)
      LATE_SHIP     → review (check carrier data first)
      PRICE_DISCREPANCY → escalate (needs Finance sign-off)
      LABEL_ERROR   → escalate (pull original label for review)
   d. auto_dispute: call submit_chargeback_dispute(id, evidence)
   e. escalate: add to escalation list with all evidence gathered
3. Email Finance with:
   - Summary (total | auto-disputed | escalated | dollar amounts)
   - Escalation table (id | customer | amount | reason | action needed)
4. Upload full CSV to SharePoint at Reports/Chargebacks/
'''
```

#### PO Gap Detection

```python
TASK_PO_GAP_DETECTION = '''
Identify inventory gaps and alert the Purchasing department.

Steps:
1. Call get_inventory_with_velocity() — returns for each active item:
   - qtyAvailable, avg_weekly_units_sold, days_of_supply,
     open_po_qty, next_po_expected_date

2. Flag items:
   CRITICAL: days_of_supply < 14 AND open_po_qty = 0
   WARNING:  days_of_supply < 30 AND next_po_expected_date > 21 days away
   SLOW MOVER: days_of_supply > 180 (overstock risk)

3. Alert format:
   CRITICAL: {sku} | {description} | {days_supply} days | ${weekly_revenue}/wk
   WARNING:  {sku} | {description} | {days_supply} days | PO expected {date}
   SLOW:     {sku} | {description} | {days_supply} days | ${inventory_value} on hand

4. Send to Teams #purchasing + email purchasing@yourdomain.com
'''
```

### Tool Description Examples (for registry)

```python
# These go into the "description" field of each tool in TOOL_REGISTRY

TOOL_DESC_GET_CATALOG_HEALTH = """
Checks the health of product listings across one or more marketplace platforms.
Call this tool FIRST before any attempt to fix or update listings — never assume
there is a problem without checking. Pass platforms=[] for all platforms or specify
e.g. ['amazon_sc', 'walmart'] to scope the check. Returns a list of CatalogIssue
objects with severity and auto_fixable flags. After calling this, call
auto_fix_issue for each auto_fixable=True result immediately.
"""

TOOL_DESC_SYNC_INVENTORY = """
Pushes current ERP inventory levels to a specific marketplace platform.
Always pull the latest inventory from the ERP immediately before calling this —
do not cache quantities across tool calls. Pass the platform name and a list of
{sku, qty_available} dicts. If qty_available = 0, the item will be set to
out-of-stock on the platform — this is expected behaviour.
"""

TOOL_DESC_SUBMIT_DISPUTE = """
Submits a chargeback dispute to ERP AR for a specific chargeback ID.
ONLY call this for chargebacks in the auto_dispute category (SHORTAGE, EARLY_SHIP,
ROUTING, DUPLICATE_PAYMENT). You must pass evidence: at minimum the order number,
ship date, tracking number, and carrier code. If the reason is PRICE_DISCREPANCY,
LABEL_ERROR, or LATE_SHIP — do NOT call this tool. Escalate to Finance instead.
"""

TOOL_DESC_SEND_ALERT = """
Sends an alert message to a department channel or email address.
Channel options:
  teams_ecomm      → E-Commerce team Microsoft Teams channel
  teams_purchasing → Purchasing team Microsoft Teams channel
  teams_warehouse  → Warehouse operations Teams channel
  email_finance    → finance@yourdomain.com
  email_purchasing → purchasing@yourdomain.com
severity: low | medium | high | critical
Always include: what happened, how many items/dollars affected,
and the specific action you need the human to take.
"""
```

### Output Templates (`src/agent/prompts/outputs.py`)

```python
# Email to Finance — daily chargeback report
EMAIL_CHARGEBACK_SUBJECT = (
    "Chargeback Reconciliation — {run_date} | "
    "{n_disputed} Auto-Disputed | {n_escalated} Need Review"
)

EMAIL_CHARGEBACK_BODY = """
Hi Finance team,

Here is the daily chargeback reconciliation summary for {run_date}.

SUMMARY
─────────────────────────────────────────────────────
Total open chargebacks reviewed:  {n_total}
Automatically disputed:           {n_disputed}  (${disputed_amount})
Escalated — needs your action:    {n_escalated}  (${escalated_amount})

ITEMS NEEDING YOUR REVIEW
─────────────────────────────────────────────────────
{escalation_rows}
(Full detail: {sharepoint_url})

AUTO-DISPUTED (for your records)
─────────────────────────────────────────────────────
{auto_dispute_rows}
"""

# Teams message — purchasing alert
TEAMS_PO_ALERT = """
⚠️ PURCHASING ALERT — {run_date}

CRITICAL (order now — <14 days supply):
{critical_items}

WARNING (order this week — <30 days supply):
{warning_items}

Total weekly revenue at risk if critical items stock out: ${revenue_at_risk}
"""

# Teams message — catalog health escalation
TEAMS_CATALOG_ESCALATION = """
🔴 CATALOG HEALTH — ACTION NEEDED — {run_date}

{n_fixed} issues were auto-fixed.
The following {n_escalated} require manual review:

{escalation_table}

Platform with most issues: {top_platform} ({n_top_issues} open)
Full log: {audit_log_url}
"""
```

---

## 12. Testing

```python
# tests/unit/test_prompts.py — Example test: verify agent calls correct tools

def test_catalog_health_prompt_calls_correct_tools():
    """
    Given TASK_CATALOG_HEALTH_CHECK, the agent should:
    1. Call get_catalog_health first
    2. Call auto_fix_issue for each auto_fixable result
    3. Mention the specific SKU in its output
    """
    mock_tools = {
        'get_catalog_health': MagicMock(return_value=[
            {'sku': 'SKU001', 'platform': 'amazon_sc',
             'issue_type': 'suppressed', 'auto_fixable': True, 'severity': 'high'},
        ]),
        'auto_fix_issue': MagicMock(return_value={'success': True}),
        'send_alert': MagicMock(return_value={'sent': True}),
    }
    with patch('agent.core.execute_tool',
               side_effect=lambda name, args: mock_tools[name](args)):
        result = run_agent(TASK_CATALOG_HEALTH_CHECK)
    mock_tools['get_catalog_health'].assert_called_once()
    mock_tools['auto_fix_issue'].assert_called_once()
    assert 'SKU001' in result
```

| Test Type | Location | What to test | Tools |
|---|---|---|---|
| Unit | `tests/unit/` | Each tool with mocked HTTP responses | pytest + respx |
| Integration | `tests/integration/` | Tool → real ERP sandbox → verify data shape | pytest + real creds |
| Agent loop | `tests/unit/test_agent.py` | Mock all tools, verify agent selects correct tools per task | pytest + anthropic mock |
| Scheduler | `tests/unit/test_scheduler.py` | All jobs registered with correct triggers | pytest + APScheduler |

---

## 13. Build Order for Cursor

Hand Cursor the relevant section number alongside this README for each sprint.

### Sprint 1 — Foundation (Days 1–5)
1. Set up repo structure exactly as shown in [Section 1](#1-repository-structure)
2. Create `.env` from `.env.example`, fill in all credentials
3. `pip install -r requirements.txt`
4. Create Postgres DB, run Alembic migration with schema from [Section 9](#9-database-schema)
5. Build `erp_client.py` ([Section 3](#3-erp-integration-vai-s2k)) and test against your ERP
6. Build `erp_export.py` SFTP downloader as fallback
7. Write unit tests for ERP client with mocked responses

### Sprint 2 — Marketplace Tools (Days 6–15)
1. Build `amazon_vc.py` and `amazon_sc.py` ([Section 4](#4-marketplace-tools))
2. Build `walmart.py`
3. Build `wayfair.py` (GraphQL client)
4. Build `home_depot.py`, `lowes.py`, `bestbuy.py`
5. Build `catalog_health.py` monitor
6. Register all marketplace tools in `registry.py`

### Sprint 3 — Analytics (Days 16–22)
1. Build `sku_performance.py` with all metrics
2. Build `channel_performance.py` with buyer code mapping
3. Build `anomaly_detection.py`: slow movers and stockout risk
4. Build `report_builder.py` with Excel output and SharePoint upload

### Sprint 4 — Automation & Agent Core (Days 23–32)
1. Build `chargeback.py` full workflow
2. Build `po_alerts.py`
3. Build `m365.py` and `notifications.py`
4. Build agent `core.py` loop with full tool registry
5. Add all prompts from [Section 11](#11-prompt-library)
6. Set up scheduler with all jobs

### Sprint 5 — MCP Server & QA (Days 33–40)
1. Build MCP server (`src/mcp_server/server.py`)
2. Configure Claude Desktop and test natural language invocation
3. Write full test suite
4. Document every function in `src/tools/` with docstrings covering: what it calls, what it returns, known edge cases

---

## 14. Pre-Build Checklist

Before writing a line of code, resolve these:

| # | Item | Who | Priority |
|---|---|---|---|
| 1 | Obtain ERP REST API base URL and credentials (bearer token or OAuth) from your ERP vendor | IT / ERP admin | **CRITICAL** |
| 2 | Confirm ERP company code and warehouse code(s) | IT | **CRITICAL** |
| 3 | Map ERP customer numbers for each marketplace (Amazon, Walmart, Wayfair, HD, Lowes, BestBuy) | Finance / E-Commerce | **CRITICAL** |
| 4 | Set up Amazon SP-API developer app, obtain refresh tokens for Vendor Central and Seller Central | IT / Amazon admin | **CRITICAL** |
| 5 | Confirm ERP SFTP export schedule and format; request sample CSV exports | IT / ERP vendor | **HIGH** |
| 6 | Obtain API credentials for Walmart, Wayfair, Home Depot, Lowes, BestBuy | E-Commerce team | **HIGH** |
| 7 | Register Azure AD application for M365 (SharePoint, Outlook) | IT | **HIGH** |
| 8 | Confirm which chargeback reason codes you receive most from each marketplace | Finance | **MEDIUM** |
| 9 | Confirm Power Automate webhook URLs for Finance and Purchasing notification flows | IT | **MEDIUM** |
| 10 | Decide hosting: on-prem, cloud VM, or managed container | Leadership / IT | **MEDIUM** |

---

## Stack Summary

| Layer | Choice |
|---|---|
| Agent framework | Python + LangGraph (or custom loop) |
| LLM | Claude via Anthropic API (`claude-sonnet-4-20250514`) |
| Memory | pgvector long-term + conversation history short-term |
| MCP server | Python `mcp` SDK |
| Automation | Power Automate for M365, Python scripts for everything else |
| Database | PostgreSQL + Redis cache |
| Scheduling | APScheduler |
| Observability | structlog → structured DB logging |
| Testing | pytest + respx |

---

## Adapting to a Different ERP

This system is built against VAI S2K but the ERP layer is isolated in `src/tools/erp/`. To adapt:

1. Replace `ERP_BASE_URL` with your ERP's REST base URL
2. Update field name mappings in `erp_inventory.py`, `erp_items.py`, `erp_orders.py`, `erp_ar.py`
3. If your ERP uses a different auth method (API key header, OAuth2 etc.), update `erp_client.py`
4. If no REST API is available, use the CSV export fallback in `erp_export.py` — most ERPs can schedule flat file exports via SFTP
5. Update `CHANNEL_BUYER_MAP` with your ERP's customer numbers for each marketplace

All analytics, automation, agent core, MCP server, and scheduler code remains unchanged.

---

## License

MIT

---

## Contributing

PRs welcome. If you adapt this for a different ERP or add a new marketplace connector, please open a PR with the new files in `src/tools/erp/` or `src/tools/marketplace/` and update this README's endpoint tables.
