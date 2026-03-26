from src.tools.registry import TOOL_FUNCTIONS


def execute_tool(name: str, args: dict):
    """Executes a registered tool by name."""
    if name not in TOOL_FUNCTIONS:
        raise ValueError(f'Unknown tool: {name}')
    return TOOL_FUNCTIONS[name](**(args or {}))
