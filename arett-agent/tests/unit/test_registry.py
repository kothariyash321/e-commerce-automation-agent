from src.tools import execute_tool


def test_execute_tool_catalog_health():
    result = execute_tool('get_catalog_health', {})
    assert isinstance(result, list)
    assert result
