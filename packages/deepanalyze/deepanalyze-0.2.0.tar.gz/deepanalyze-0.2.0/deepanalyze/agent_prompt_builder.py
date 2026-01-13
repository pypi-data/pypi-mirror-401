from __future__ import annotations

from typing import Any, Dict, List, Tuple

from .agent_settings import DeepAnalyzeAgentSettings
from .agent_workspace_scanner import list_workspace_files


def build_user_prompt(*, user_message: str, data_block: str) -> str:
    instruction = str(user_message or "").strip()
    if not instruction:
        instruction = "(empty)"
    if data_block:
        return f"# Instruction\n{instruction}\n\n# Data\n{data_block}"
    return f"# Instruction\n{instruction}"


async def build_vllm_messages(
    *,
    settings: DeepAnalyzeAgentSettings,
    contents_manager: Any,
    workspace_dir: str,
    user_message: str,
) -> Tuple[List[Dict[str, str]], str, List[Dict[str, Any]]]:
    """
    构造 vLLM messages，并返回：
    - messages: OpenAI-style messages
    - data_block: 注入到 # Data 的文本（用于调试/展示）
    - files: 结构化文件元信息数组
    """

    data_block, files = await list_workspace_files(
        contents_manager=contents_manager,
        workspace_dir=workspace_dir,
        settings=settings,
    )
    messages = [
        {"role": "user", "content": build_user_prompt(user_message=user_message, data_block=data_block)},
    ]
    return messages, data_block, files
