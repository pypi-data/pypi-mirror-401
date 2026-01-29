"""
Contexere - LLM Tracing and Context Engineering for Production AI Agents

A lightweight Python library for tracing LLM applications and agent workflows.
"""

from contexere.config import init
from contexere.op import op
from contexere.openai_instrumentation import instrument_openai
from contexere.query import Query
from contexere.models import (
    Agent,
    AgentVersion,
    Prompts,
    Diff,
    FeedbackItem,
    AgentStats,
    VersionStats,
    SpanItem,
)

__version__ = "0.3.1"

__all__ = [
    "init",
    "op",
    "instrument_openai",
    "Query",
    "Agent",
    "AgentVersion",
    "Prompts",
    "Diff",
    "FeedbackItem",
    "AgentStats",
    "VersionStats",
    "SpanItem",
]
