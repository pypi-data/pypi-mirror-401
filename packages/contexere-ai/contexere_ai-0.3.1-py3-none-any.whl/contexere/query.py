"""
Contexere Query API

Provides programmatic access to agents, versions, feedback, and stats.
"""

from typing import Optional, List, Dict, Any
from datetime import datetime

from contexere.http_client import QueryClient
from contexere.models import (
    Agent, AgentVersion, Prompts, Diff,
    FeedbackItem, AgentStats, VersionStats, SpanItem
)
from contexere.dataframe import feedback_to_dataframe, stats_to_dataframe, spans_to_dataframe

try:
    import pandas as pd
    HAS_PANDAS = True
except ImportError:
    HAS_PANDAS = False


def _parse_datetime(value: Optional[str]) -> Optional[datetime]:
    """Parse datetime string to datetime object"""
    if not value:
        return None
    try:
        # Handle ISO format with timezone
        if "T" in value:
            return datetime.fromisoformat(value.replace("Z", "+00:00"))
        return datetime.fromisoformat(value)
    except (ValueError, TypeError):
        return None


class FeedbackResult:
    """Result of a feedback query with DataFrame conversion"""

    def __init__(self, items: List[Dict[str, Any]], total_count: int, limit: int, offset: int):
        self._items = items
        self.total_count = total_count
        self.limit = limit
        self.offset = offset

    @property
    def items(self) -> List[FeedbackItem]:
        """Get feedback items as FeedbackItem objects"""
        return [
            FeedbackItem(
                review_id=item.get("review_id"),
                span_id=item.get("span_id"),
                agent_name=item.get("agent_name"),
                agent_id=item.get("agent_id"),
                version_label=item.get("version_label"),
                version_id=item.get("version_id"),
                schema_id=item.get("schema_id"),
                schema_name=item.get("schema_name"),
                labeler_id=item.get("labeler_id"),
                answers=item.get("answers"),
                written_feedback=item.get("written_feedback"),
                status=item.get("status"),
                reviewed_at=_parse_datetime(item.get("reviewed_at")),
                system_prompt=item.get("system_prompt"),
                user_prompt=item.get("user_prompt"),
                context=item.get("context"),
                output=item.get("output")
            )
            for item in self._items
        ]

    def to_dataframe(
        self,
        expand_answers: bool = True,
        expand_context: bool = False,
        include_prompts: bool = True,
        truncate_text: int = 0
    ) -> "pd.DataFrame":
        """
        Convert to pandas DataFrame.

        Args:
            expand_answers: Flatten answers dict to columns
            expand_context: Flatten context dict to columns
            include_prompts: Include prompt columns
            truncate_text: Max chars for text fields (0 = no truncation)

        Returns:
            pandas DataFrame
        """
        return feedback_to_dataframe(
            self._items,
            expand_answers=expand_answers,
            expand_context=expand_context,
            include_prompts=include_prompts,
            truncate_text=truncate_text
        )

    def __len__(self) -> int:
        return len(self._items)

    def __iter__(self):
        return iter(self.items)


class SpanResult:
    """Result of a span query with DataFrame conversion"""

    def __init__(self, items: List[Dict[str, Any]], total_count: int, limit: int, offset: int):
        self._items = items
        self.total_count = total_count
        self.limit = limit
        self.offset = offset

    @property
    def items(self) -> List[SpanItem]:
        """Get span items as SpanItem objects"""
        return [
            SpanItem(
                id=item.get("id"),
                name=item.get("name"),
                agent_id=item.get("agent_id"),
                agent_name=item.get("agent_name"),
                agent_version_id=item.get("agent_version_id"),
                version_label=item.get("version_label"),
                system_prompt=item.get("system_prompt"),
                user_prompt=item.get("user_prompt"),
                context=item.get("context"),
                inputs=item.get("inputs"),
                output=item.get("output"),
                error=item.get("error"),
                duration_ms=item.get("duration_ms"),
                review_status=item.get("review_status"),
                created_at=_parse_datetime(item.get("created_at"))
            )
            for item in self._items
        ]

    def to_dataframe(
        self,
        expand_context: bool = False,
        expand_inputs: bool = False,
        include_prompts: bool = True,
        truncate_text: int = 0
    ) -> "pd.DataFrame":
        """
        Convert to pandas DataFrame.

        Args:
            expand_context: Flatten context dict to columns
            expand_inputs: Flatten inputs dict to columns
            include_prompts: Include prompt columns
            truncate_text: Max chars for text fields (0 = no truncation)

        Returns:
            pandas DataFrame
        """
        return spans_to_dataframe(
            self._items,
            expand_context=expand_context,
            expand_inputs=expand_inputs,
            include_prompts=include_prompts,
            truncate_text=truncate_text
        )

    def __len__(self) -> int:
        return len(self._items)

    def __iter__(self):
        return iter(self.items)


class AgentQuery:
    """Query methods for agents and versions"""

    def __init__(self, client: QueryClient):
        self._client = client

    def list(self) -> List[Agent]:
        """
        List all agents in the project.

        Returns:
            List of Agent objects
        """
        data = self._client.get("/query/agents")
        return [
            Agent(
                id=item["id"],
                name=item["name"],
                description=item.get("description"),
                project_id=item.get("project_id"),
                current_version_id=item.get("current_version_id"),
                current_version_label=item.get("current_version_label"),
                latest_major_version=item.get("latest_major_version", 0),
                created_at=_parse_datetime(item.get("created_at")),
                updated_at=_parse_datetime(item.get("updated_at"))
            )
            for item in data
        ]

    def get(self, name: Optional[str] = None, id: Optional[str] = None) -> Agent:
        """
        Get a single agent by name or ID.

        Args:
            name: Agent name (searches in project)
            id: Agent UUID

        Returns:
            Agent object

        Raises:
            ValueError: If agent not found
        """
        if id:
            data = self._client.get(f"/query/agents/{id}")
            return Agent(
                id=data["id"],
                name=data["name"],
                description=data.get("description"),
                project_id=data.get("project_id"),
                current_version_id=data.get("current_version_id"),
                current_version_label=data.get("current_version_label"),
                latest_major_version=data.get("latest_major_version", 0),
                created_at=_parse_datetime(data.get("created_at")),
                updated_at=_parse_datetime(data.get("updated_at"))
            )
        elif name:
            # Search by name in the list
            agents = self.list()
            for agent in agents:
                if agent.name == name:
                    return agent
            raise ValueError(f"Agent '{name}' not found")
        else:
            raise ValueError("Must provide either 'name' or 'id'")

    def versions(self, name: Optional[str] = None, id: Optional[str] = None) -> List[AgentVersion]:
        """
        Get all versions for an agent.

        Args:
            name: Agent name
            id: Agent UUID

        Returns:
            List of AgentVersion objects (newest first)
        """
        if name and not id:
            agent = self.get(name=name)
            id = agent.id

        if not id:
            raise ValueError("Must provide either 'name' or 'id'")

        data = self._client.get(f"/query/agents/{id}/versions")
        return [
            AgentVersion(
                id=item["id"],
                agent_id=item["agent_id"],
                version_label=item["version_label"],
                major_version=item["major_version"],
                minor_version=item["minor_version"],
                system_prompt=item.get("system_prompt"),
                user_prompt_template=item.get("user_prompt_template"),
                context_schema=item.get("context_schema"),
                source=item.get("source", "code"),
                change_summary=item.get("change_summary"),
                created_by=item.get("created_by"),
                created_at=_parse_datetime(item.get("created_at"))
            )
            for item in data
        ]

    def version(
        self,
        name: Optional[str] = None,
        id: Optional[str] = None,
        version: Optional[str] = None
    ) -> AgentVersion:
        """
        Get a specific version.

        Args:
            name: Agent name
            id: Agent UUID
            version: Version label (e.g., "1", "2.1"). If None, returns latest.

        Returns:
            AgentVersion object
        """
        if name and not id:
            agent = self.get(name=name)
            id = agent.id

        if not id:
            raise ValueError("Must provide either 'name' or 'id'")

        if version is None:
            # Get latest version
            versions = self.versions(id=id)
            if not versions:
                raise ValueError("No versions found for agent")
            return versions[0]

        data = self._client.get(f"/query/agents/{id}/versions/{version}")
        return AgentVersion(
            id=data["id"],
            agent_id=data["agent_id"],
            version_label=data["version_label"],
            major_version=data["major_version"],
            minor_version=data["minor_version"],
            system_prompt=data.get("system_prompt"),
            user_prompt_template=data.get("user_prompt_template"),
            context_schema=data.get("context_schema"),
            source=data.get("source", "code"),
            change_summary=data.get("change_summary"),
            created_by=data.get("created_by"),
            created_at=_parse_datetime(data.get("created_at"))
        )

    def diff(
        self,
        name: Optional[str] = None,
        id: Optional[str] = None,
        from_version: str = None,
        to_version: str = None
    ) -> Diff:
        """
        Get diff between two versions.

        Args:
            name: Agent name
            id: Agent UUID
            from_version: Source version label
            to_version: Target version label

        Returns:
            Diff object
        """
        if name and not id:
            agent = self.get(name=name)
            id = agent.id

        if not id:
            raise ValueError("Must provide either 'name' or 'id'")

        if not from_version or not to_version:
            raise ValueError("Must provide both 'from_version' and 'to_version'")

        data = self._client.get(
            f"/query/agents/{id}/diff",
            params={"from": from_version, "to": to_version}
        )

        return Diff(
            from_version=data["from_version"],
            to_version=data["to_version"],
            system_prompt_diff=data.get("system_prompt_diff"),
            user_prompt_diff=data.get("user_prompt_diff"),
            context_schema_diff=data.get("context_schema_diff")
        )


class FeedbackQuery:
    """Query methods for feedback/reviews"""

    def __init__(self, client: QueryClient):
        self._client = client
        self._agents = AgentQuery(client)

    def query(
        self,
        agent: Optional[str] = None,
        agent_id: Optional[str] = None,
        version: Optional[str] = None,
        schema: Optional[str] = None,
        status: Optional[str] = None,
        span_id: Optional[str] = None,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
        has_written_feedback: Optional[bool] = None,
        source: Optional[str] = None,
        limit: int = 100,
        offset: int = 0
    ) -> FeedbackResult:
        """
        Query feedback with filters. All filters can be combined.

        Args:
            agent: Filter by agent name
            agent_id: Filter by agent ID
            version: Filter by version label
            schema: Filter by schema name
            status: Filter by review status ('completed', 'in_progress', 'skipped')
            span_id: Filter by specific span
            from_date: Filter from date (YYYY-MM-DD)
            to_date: Filter to date (YYYY-MM-DD)
            has_written_feedback: Filter by presence of written feedback
            source: Filter by version source ('code' or 'ui')
            limit: Max results (default 100, max 1000)
            offset: Pagination offset

        Returns:
            FeedbackResult with items and to_dataframe() method
        """
        # Resolve agent name to ID if needed
        if agent and not agent_id:
            try:
                agent_obj = self._agents.get(name=agent)
                agent_id = agent_obj.id
            except ValueError:
                # Agent not found, return empty result
                return FeedbackResult([], 0, limit, offset)

        params = {
            "agent_id": agent_id,
            "version": version,
            "schema": schema,
            "status": status,
            "span_id": span_id,
            "from_date": from_date,
            "to_date": to_date,
            "has_written_feedback": has_written_feedback,
            "source": source,
            "limit": limit,
            "offset": offset
        }

        data = self._client.get("/query/feedback", params=params)

        return FeedbackResult(
            items=data.get("items", []),
            total_count=data.get("total_count", 0),
            limit=data.get("limit", limit),
            offset=data.get("offset", offset)
        )

    def for_agent(self, name: str, **kwargs) -> FeedbackResult:
        """
        Get all feedback for an agent.

        Args:
            name: Agent name
            **kwargs: Additional filters

        Returns:
            FeedbackResult
        """
        return self.query(agent=name, **kwargs)

    def for_version(self, name: str, version: str, **kwargs) -> FeedbackResult:
        """
        Get feedback for a specific version.

        Args:
            name: Agent name
            version: Version label
            **kwargs: Additional filters

        Returns:
            FeedbackResult
        """
        return self.query(agent=name, version=version, **kwargs)

    def for_span(self, span_id: str, **kwargs) -> FeedbackResult:
        """
        Get feedback for a specific span.

        Args:
            span_id: Span UUID
            **kwargs: Additional filters

        Returns:
            FeedbackResult
        """
        return self.query(span_id=span_id, **kwargs)


class SpanQuery:
    """Query methods for spans/traces"""

    def __init__(self, client: QueryClient):
        self._client = client
        self._agents = AgentQuery(client)

    def query(
        self,
        agent: Optional[str] = None,
        agent_id: Optional[str] = None,
        version: Optional[str] = None,
        version_id: Optional[str] = None,
        review_status: Optional[str] = None,
        has_feedback: Optional[bool] = None,
        has_error: Optional[bool] = None,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
        limit: int = 100,
        offset: int = 0
    ) -> SpanResult:
        """
        Query spans with filters. All filters can be combined.

        Args:
            agent: Filter by agent name
            agent_id: Filter by agent ID
            version: Filter by version label
            version_id: Filter by version ID
            review_status: Filter by review status
            has_feedback: Filter by presence of feedback
            has_error: Filter by presence of error
            from_date: Filter from date (YYYY-MM-DD)
            to_date: Filter to date (YYYY-MM-DD)
            limit: Max results (default 100, max 1000)
            offset: Pagination offset

        Returns:
            SpanResult with items and to_dataframe() method
        """
        params = {
            "agent": agent,
            "agent_id": agent_id,
            "version": version,
            "version_id": version_id,
            "review_status": review_status,
            "has_feedback": has_feedback,
            "has_error": has_error,
            "from_date": from_date,
            "to_date": to_date,
            "limit": limit,
            "offset": offset
        }

        data = self._client.get("/query/spans", params=params)

        return SpanResult(
            items=data.get("items", []),
            total_count=data.get("total_count", 0),
            limit=data.get("limit", limit),
            offset=data.get("offset", offset)
        )

    def for_agent(self, name: str, **kwargs) -> SpanResult:
        """
        Get all spans for an agent.

        Args:
            name: Agent name
            **kwargs: Additional filters

        Returns:
            SpanResult
        """
        return self.query(agent=name, **kwargs)

    def for_version(self, name: str, version: str, **kwargs) -> SpanResult:
        """
        Get spans for a specific version.

        Args:
            name: Agent name
            version: Version label
            **kwargs: Additional filters

        Returns:
            SpanResult
        """
        return self.query(agent=name, version=version, **kwargs)

    def with_errors(self, **kwargs) -> SpanResult:
        """
        Get spans that have errors.

        Args:
            **kwargs: Additional filters

        Returns:
            SpanResult
        """
        return self.query(has_error=True, **kwargs)

    def without_feedback(self, **kwargs) -> SpanResult:
        """
        Get spans that don't have feedback yet.

        Args:
            **kwargs: Additional filters

        Returns:
            SpanResult
        """
        return self.query(has_feedback=False, **kwargs)


class StatsQuery:
    """Query methods for statistics"""

    def __init__(self, client: QueryClient):
        self._client = client
        self._agents = AgentQuery(client)

    def for_agent(self, name: Optional[str] = None, id: Optional[str] = None) -> AgentStats:
        """
        Get aggregate stats for an agent.

        Args:
            name: Agent name
            id: Agent UUID

        Returns:
            AgentStats object
        """
        if name and not id:
            agent = self._agents.get(name=name)
            id = agent.id

        if not id:
            raise ValueError("Must provide either 'name' or 'id'")

        data = self._client.get(f"/query/stats/agent/{id}")

        by_version = [
            VersionStats(
                version_label=v["version_label"],
                version_id=v["version_id"],
                source=v["source"],
                spans_count=v.get("spans_count", 0),
                reviews_count=v.get("reviews_count", 0),
                completed_reviews=v.get("completed_reviews", 0),
                first_seen=_parse_datetime(v.get("first_seen")),
                last_seen=_parse_datetime(v.get("last_seen"))
            )
            for v in data.get("by_version", [])
        ]

        return AgentStats(
            agent_id=data["agent_id"],
            agent_name=data["agent_name"],
            total_spans=data.get("total_spans", 0),
            total_reviews=data.get("total_reviews", 0),
            versions_count=data.get("versions_count", 0),
            by_version=by_version
        )

    def for_version(
        self,
        name: Optional[str] = None,
        id: Optional[str] = None,
        version: Optional[str] = None
    ) -> VersionStats:
        """
        Get stats for a specific version.

        Args:
            name: Agent name
            id: Agent UUID
            version: Version label (if None, returns stats for latest version)

        Returns:
            VersionStats object
        """
        agent_stats = self.for_agent(name=name, id=id)

        if not agent_stats.by_version:
            raise ValueError("No versions found for agent")

        if version is None:
            # Return latest version stats
            return agent_stats.by_version[0]

        # Find specific version
        for v in agent_stats.by_version:
            if v.version_label == version:
                return v

        raise ValueError(f"Version '{version}' not found for agent")

    def to_dataframe(self, stats: AgentStats) -> "pd.DataFrame":
        """
        Convert agent stats to DataFrame.

        Args:
            stats: AgentStats object

        Returns:
            pandas DataFrame with one row per version
        """
        return stats_to_dataframe([
            {
                "version_label": v.version_label,
                "version_id": v.version_id,
                "source": v.source,
                "spans_count": v.spans_count,
                "reviews_count": v.reviews_count,
                "completed_reviews": v.completed_reviews,
                "first_seen": v.first_seen,
                "last_seen": v.last_seen
            }
            for v in stats.by_version
        ])


class Query:
    """
    Main entry point for Contexere Query API.

    Example:
        >>> import contexere as conte
        >>> from contexere.query import Query
        >>>
        >>> conte.init(api_key="ck_...")
        >>> q = Query()
        >>>
        >>> # List agents
        >>> agents = q.agents.list()
        >>>
        >>> # Get version history
        >>> versions = q.agents.versions("my-agent")
        >>>
        >>> # Get feedback as DataFrame
        >>> df = q.feedback.for_agent("my-agent").to_dataframe()
        >>>
        >>> # Get spans as DataFrame
        >>> df = q.spans.for_agent("my-agent").to_dataframe()
        >>>
        >>> # Get version stats
        >>> stats = q.stats.for_version("my-agent", "1")
    """

    def __init__(self, timeout: float = 30.0):
        """
        Initialize Query API.

        Args:
            timeout: HTTP request timeout in seconds
        """
        self._client = QueryClient(timeout=timeout)
        self.agents = AgentQuery(self._client)
        self.feedback = FeedbackQuery(self._client)
        self.spans = SpanQuery(self._client)
        self.stats = StatsQuery(self._client)
