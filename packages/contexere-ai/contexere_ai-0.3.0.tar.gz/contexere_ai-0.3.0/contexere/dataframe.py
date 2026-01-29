"""
DataFrame conversion utilities for Contexere Query API
"""

from typing import List, Dict, Any, Optional
import json

try:
    import pandas as pd
    HAS_PANDAS = True
except ImportError:
    HAS_PANDAS = False


def _check_pandas():
    """Check if pandas is available"""
    if not HAS_PANDAS:
        raise ImportError(
            "pandas is required for DataFrame operations. "
            "Install with: pip install pandas"
        )


def _flatten_dict(d: Optional[Dict[str, Any]], prefix: str = "") -> Dict[str, Any]:
    """
    Flatten a nested dictionary.

    Args:
        d: Dictionary to flatten
        prefix: Prefix for keys

    Returns:
        Flattened dictionary
    """
    if not d:
        return {}

    items = {}
    for k, v in d.items():
        new_key = f"{prefix}{k}" if prefix else k
        if isinstance(v, dict):
            items.update(_flatten_dict(v, f"{new_key}_"))
        else:
            items[new_key] = v
    return items


def _truncate_text(text: Optional[str], max_length: int) -> Optional[str]:
    """Truncate text to max length"""
    if text is None or max_length <= 0:
        return text
    if len(text) <= max_length:
        return text
    return text[:max_length] + "..."


def feedback_to_dataframe(
    items: List[Dict[str, Any]],
    expand_answers: bool = True,
    expand_context: bool = False,
    include_prompts: bool = True,
    truncate_text: int = 0
) -> "pd.DataFrame":
    """
    Convert feedback items to pandas DataFrame.

    Args:
        items: List of feedback item dicts
        expand_answers: Flatten answers dict to columns (answer_q1, answer_q2, ...)
        expand_context: Flatten context dict to columns
        include_prompts: Include system_prompt, user_prompt columns
        truncate_text: Max chars for text fields (0 = no truncation)

    Returns:
        pandas DataFrame
    """
    _check_pandas()

    rows = []
    for item in items:
        row = {
            "review_id": item.get("review_id"),
            "span_id": item.get("span_id"),
            "agent_name": item.get("agent_name"),
            "agent_id": item.get("agent_id"),
            "version_label": item.get("version_label"),
            "version_id": item.get("version_id"),
            "schema_id": item.get("schema_id"),
            "schema_name": item.get("schema_name"),
            "labeler_id": item.get("labeler_id"),
            "status": item.get("status"),
            "reviewed_at": item.get("reviewed_at"),
            "written_feedback": item.get("written_feedback"),
        }

        # Include prompts if requested
        if include_prompts:
            system_prompt = item.get("system_prompt")
            user_prompt = item.get("user_prompt")
            if truncate_text > 0:
                system_prompt = _truncate_text(system_prompt, truncate_text)
                user_prompt = _truncate_text(user_prompt, truncate_text)
            row["system_prompt"] = system_prompt
            row["user_prompt"] = user_prompt

        # Handle output
        output = item.get("output")
        if isinstance(output, (dict, list)):
            row["output"] = json.dumps(output)
        else:
            row["output"] = output

        # Expand or keep answers as JSON
        answers = item.get("answers")
        if expand_answers and answers:
            for k, v in answers.items():
                row[f"answer_{k}"] = v
        else:
            row["answers"] = json.dumps(answers) if answers else None

        # Expand or keep context as JSON
        context = item.get("context")
        if expand_context and context:
            for k, v in _flatten_dict(context, "context_").items():
                row[k] = v
        else:
            row["context"] = json.dumps(context) if context else None

        rows.append(row)

    return pd.DataFrame(rows)


def stats_to_dataframe(by_version: List[Dict[str, Any]]) -> "pd.DataFrame":
    """
    Convert version stats to pandas DataFrame.

    Args:
        by_version: List of version stats dicts

    Returns:
        pandas DataFrame with one row per version
    """
    _check_pandas()

    rows = []
    for v in by_version:
        rows.append({
            "version_label": v.get("version_label"),
            "version_id": v.get("version_id"),
            "source": v.get("source"),
            "spans_count": v.get("spans_count", 0),
            "reviews_count": v.get("reviews_count", 0),
            "completed_reviews": v.get("completed_reviews", 0),
            "first_seen": v.get("first_seen"),
            "last_seen": v.get("last_seen"),
        })

    return pd.DataFrame(rows)
