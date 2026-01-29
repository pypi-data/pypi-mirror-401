"""
Data models for Contexere Query API
"""

from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List
from datetime import datetime


@dataclass
class Prompts:
    """Prompts for an agent version"""
    system_prompt: Optional[str] = None
    user_prompt_template: Optional[str] = None
    context_schema: Optional[Dict[str, Any]] = None


@dataclass
class AgentVersion:
    """A specific version of an agent"""
    id: str
    agent_id: str
    version_label: str
    major_version: int
    minor_version: int
    system_prompt: Optional[str] = None
    user_prompt_template: Optional[str] = None
    context_schema: Optional[Dict[str, Any]] = None
    source: str = "code"  # 'code' or 'ui'
    change_summary: Optional[str] = None
    created_by: Optional[str] = None
    created_at: Optional[datetime] = None

    def prompts(self) -> Prompts:
        """Get prompts for this version"""
        return Prompts(
            system_prompt=self.system_prompt,
            user_prompt_template=self.user_prompt_template,
            context_schema=self.context_schema
        )


@dataclass
class Agent:
    """An agent definition"""
    id: str
    name: str
    description: Optional[str] = None
    project_id: Optional[str] = None
    current_version_id: Optional[str] = None
    current_version_label: Optional[str] = None
    latest_major_version: int = 0
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    # Populated when fetched with version
    current_version: Optional[AgentVersion] = None


@dataclass
class Diff:
    """Diff between two versions"""
    from_version: str
    to_version: str
    system_prompt_diff: Optional[str] = None
    user_prompt_diff: Optional[str] = None
    context_schema_diff: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "from_version": self.from_version,
            "to_version": self.to_version,
            "system_prompt_diff": self.system_prompt_diff,
            "user_prompt_diff": self.user_prompt_diff,
            "context_schema_diff": self.context_schema_diff
        }


@dataclass
class FeedbackItem:
    """A single feedback/review item"""
    review_id: str
    span_id: str
    agent_name: Optional[str] = None
    agent_id: Optional[str] = None
    version_label: Optional[str] = None
    version_id: Optional[str] = None
    schema_id: Optional[str] = None
    schema_name: Optional[str] = None
    labeler_id: Optional[str] = None
    answers: Optional[Dict[str, Any]] = None
    written_feedback: Optional[str] = None
    status: Optional[str] = None
    reviewed_at: Optional[datetime] = None
    # Span data
    system_prompt: Optional[str] = None
    user_prompt: Optional[str] = None
    context: Optional[Dict[str, Any]] = None
    output: Optional[Any] = None


@dataclass
class VersionStats:
    """Stats for a single version"""
    version_label: str
    version_id: str
    source: str
    spans_count: int = 0
    reviews_count: int = 0
    completed_reviews: int = 0
    first_seen: Optional[datetime] = None
    last_seen: Optional[datetime] = None


@dataclass
class AgentStats:
    """Aggregate stats for an agent"""
    agent_id: str
    agent_name: str
    total_spans: int = 0
    total_reviews: int = 0
    versions_count: int = 0
    by_version: List[VersionStats] = field(default_factory=list)
