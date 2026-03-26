from src.agent.core import run_agent


def test_agent_catalog_fallback_path():
    result = run_agent('run catalog health check now')
    assert 'Catalog check complete' in result
