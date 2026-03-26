import os
from typing import Any

from dotenv import load_dotenv

from src.agent.prompts.system import SYSTEM_PROMPT
from src.tools import execute_tool
from src.tools.registry import TOOL_REGISTRY
from src.utils.logger import get_logger

try:
    import anthropic
except Exception:  # pragma: no cover
    anthropic = None


load_dotenv()
logger = get_logger(__name__)


def _tools_map() -> dict[str, Any]:
    return {t['name']: t for t in TOOL_REGISTRY}


def run_agent(task: str, conversation_history: list | None = None) -> str:
    """Main agent loop using Anthropic tool calling when configured."""
    if anthropic is None or not os.getenv('ANTHROPIC_API_KEY'):
        # deterministic fallback path for local development
        if 'catalog' in task.lower():
            issues = execute_tool('get_catalog_health', {})
            fixed = 0
            for issue in issues:
                if issue.get('auto_fixable'):
                    execute_tool('auto_fix_issue', issue)
                    fixed += 1
            return f"Catalog check complete: {len(issues)} issues, {fixed} auto-fixed."
        return 'Agent offline mode completed. Set ANTHROPIC_API_KEY for live tool-planning loop.'

    client = anthropic.Anthropic()
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
            text_blocks = [b.text for b in response.content if getattr(b, 'type', '') == 'text']
            return '\n'.join(text_blocks) or 'Completed.'

        if response.stop_reason == 'tool_use':
            tool_results = []
            for block in response.content:
                if block.type == 'tool_use':
                    result = execute_tool(block.name, block.input)
                    tool_results.append({'type': 'tool_result', 'tool_use_id': block.id, 'content': str(result)})
            messages.append({'role': 'assistant', 'content': response.content})
            messages.append({'role': 'user', 'content': tool_results})
            continue

        return 'Agent loop completed unexpectedly.'
