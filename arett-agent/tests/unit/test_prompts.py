from src.agent.prompts.tasks import TASK_CATALOG_HEALTH_CHECK


def test_catalog_prompt_exists():
    assert 'get_catalog_health' in TASK_CATALOG_HEALTH_CHECK
