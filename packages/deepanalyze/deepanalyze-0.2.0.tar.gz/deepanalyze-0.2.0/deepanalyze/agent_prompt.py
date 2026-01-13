from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Optional

from .agent_settings import DeepAnalyzeAgentSettings


DEFAULT_DEEPANALYZE_8B_SYSTEM_PROMPT = """\
# Role

You are DeepAnalyze, a powerful AI Agent designed to analyze data automatically. 

You are **Explorer, Not Builder**, your primary goal is to **analyze, code, and understand**. Treat your work as a scientific investigation, not a software engineering task. Your process should be iterative and guided by curiosity.

Your main goal is to follow the USER's instructions, autonomously resolve the query to the best of your ability and deliver a high-quality final report(<Answer>...</Answer>).

# Constraints

You are Working on Jupyter Notebook, all the codes are executed in Jupyter Kernel(IPython), so the data and packages exists along with different execution. You don't need to reload the data or packages between different code.

## Reuse the Data and Packages loaded in previous code

<Code>
# Load Packages and Data
import pandas as pd
import numpy as np
df = pd.read_csv('data.csv')
df.head()
</Code>

<Code>
# Reuse the Data loaded in previous code
print(np.sum(df["Age"]))
df.describe()
</Code>

## Show Plot Directly In Notebook

<Code>
plt.figure(figsize=(12,6))
sns.boxplot(data=simpson_df, x='dept', y='income', hue='age_group')
plt.title('Income Distribution by Department and Age Group')
plt.savefig('income_distribution.png', dpi=300, bbox_inches='tight')
plt.show()
</Code>

"""


def _default_prompt_path() -> Path:
    return Path(__file__).resolve().parent / "prompts" / "deepanalyze_8b.md"

def _default_prompt_index_path() -> Path:
    return Path(__file__).resolve().parent / "prompts" / "index.json"


@lru_cache(maxsize=8)
def _read_text_file(path: str) -> str:
    p = Path(path).expanduser()
    return p.read_text(encoding="utf-8")

@lru_cache(maxsize=4)
def _load_prompt_index(index_path: str) -> dict:
    p = Path(index_path).expanduser()
    raw = p.read_text(encoding="utf-8")
    return json.loads(raw)


def _resolve_prompt_path_by_name(*, name: str, index_path: Path) -> Optional[Path]:
    n = str(name or "").strip()
    if not n:
        return None
    if not index_path.exists():
        return None
    try:
        data = _load_prompt_index(str(index_path))
    except Exception:  # noqa: BLE001
        return None
    items = data.get("prompts") if isinstance(data, dict) else None
    if not isinstance(items, list):
        return None
    for it in items:
        if not isinstance(it, dict):
            continue
        if str(it.get("name") or "").strip() != n:
            continue
        rel = str(it.get("path") or "").strip()
        if not rel:
            return None
        return (index_path.parent / rel).resolve()
    return None


def load_system_prompt(settings: DeepAnalyzeAgentSettings) -> str:
    """
    按配置加载 system prompt。

    优先级：
    1) settings.system_prompt_path（若存在且可读）
    2) settings.system_prompt_name（若存在且可在 prompts/index.json 中找到）
    3) 包内默认模板文件 deepanalyze/prompts/deepanalyze_8b.md（若存在且可读）
    4) 内置 DEFAULT_DEEPANALYZE_8B_SYSTEM_PROMPT
    """

    configured = (settings.system_prompt_path or "").strip()
    if configured:
        try:
            return _read_text_file(configured)
        except Exception:  # noqa: BLE001
            pass

    prompt_name = (getattr(settings, "system_prompt_name", "") or "").strip()
    if prompt_name:
        index_path = _default_prompt_index_path()
        resolved = _resolve_prompt_path_by_name(name=prompt_name, index_path=index_path)
        if resolved and resolved.exists():
            try:
                return resolved.read_text(encoding="utf-8")
            except Exception:  # noqa: BLE001
                pass

    default_path = _default_prompt_path()
    if default_path.exists():
        try:
            return default_path.read_text(encoding="utf-8")
        except Exception:  # noqa: BLE001
            pass

    return DEFAULT_DEEPANALYZE_8B_SYSTEM_PROMPT
