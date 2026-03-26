from src.scheduler.jobs import scheduler


def test_scheduler_jobs_registered():
    ids = {job.id for job in scheduler.get_jobs()}
    assert {'s2k_sync', 'catalog_health', 'po_gaps', 'chargebacks', 'weekly_report'}.issubset(ids)
