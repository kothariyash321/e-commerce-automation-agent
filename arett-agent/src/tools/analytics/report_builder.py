from datetime import date
from pathlib import Path

from src.tools.analytics.channel_performance import get_channel_performance
from src.tools.analytics.sku_performance import detect_slow_movers, detect_stockout_risk


def build_weekly_ecomm_report() -> str:
    """Builds a weekly report and returns local file path."""
    rows = get_channel_performance(days=7)
    try:
        import openpyxl  # type: ignore

        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = 'Executive Summary'
        ws.append(['channel', 'revenue', 'units', 'margin_pct', 'returns', 'net_revenue'])
        for row in rows:
            ws.append([row['channel'], row['revenue'], row['units'], row['margin_pct'], row['returns'], row['net_revenue']])

        ws2 = wb.create_sheet('Inventory Alerts')
        ws2.append(['type', 'sku', 'days_of_supply'])
        for r in detect_stockout_risk():
            ws2.append(['stockout_risk', r['sku'], r['days_of_supply']])
        for r in detect_slow_movers():
            ws2.append(['slow_mover', r['sku'], r['days_of_supply']])

        out = Path('/tmp') / f'weekly_ecomm_{date.today().isoformat()}.xlsx'
        wb.save(out)
        return str(out)
    except Exception:
        out = Path('/tmp') / f'weekly_ecomm_{date.today().isoformat()}.csv'
        lines = ['channel,revenue,units,margin_pct,returns,net_revenue']
        for row in rows:
            lines.append(
                f"{row['channel']},{row['revenue']},{row['units']},{row['margin_pct']},{row['returns']},{row['net_revenue']}"
            )
        out.write_text('\\n'.join(lines), encoding='utf-8')
        return str(out)
