try:
    from apscheduler.schedulers.blocking import BlockingScheduler
    from apscheduler.triggers.cron import CronTrigger
    from apscheduler.triggers.interval import IntervalTrigger
except Exception:  # pragma: no cover
    class _Job:
        def __init__(self, job_id: str):
            self.id = job_id

    class BlockingScheduler:  # type: ignore[override]
        def __init__(self):
            self._jobs = []

        def add_job(self, _fn, _trigger, id: str):
            self._jobs.append(_Job(id))

        def get_jobs(self):
            return self._jobs

    class CronTrigger:  # pragma: no cover
        def __init__(self, **_kwargs):
            pass

    class IntervalTrigger:  # pragma: no cover
        def __init__(self, **_kwargs):
            pass

from src.tools.erp.s2k_export import sync_exports
from src.tools.marketplace.catalog_health import run_catalog_health_check
from src.tools.automation.po_alerts import run_po_gap_detection
from src.tools.automation.chargeback import run_chargeback_reconciliation
from src.tools.analytics.report_builder import build_weekly_ecomm_report


scheduler = BlockingScheduler()

scheduler.add_job(sync_exports, IntervalTrigger(hours=2), id='s2k_sync')
scheduler.add_job(run_catalog_health_check, IntervalTrigger(hours=4), id='catalog_health')
scheduler.add_job(run_po_gap_detection, CronTrigger(hour=7, minute=0), id='po_gaps')
scheduler.add_job(run_chargeback_reconciliation, CronTrigger(hour=8, minute=0), id='chargebacks')
scheduler.add_job(build_weekly_ecomm_report, CronTrigger(day_of_week='mon', hour=9), id='weekly_report')
