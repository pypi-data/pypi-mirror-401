"""
Data models for VibeKit sync operations.

These models represent the data structures synced between local and SaaS.
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class TaskPriority(str, Enum):
    """Task priority levels."""

    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class TaskStatusEnum(str, Enum):
    """Task status values."""

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    BLOCKED = "blocked"


class RequirementType(str, Enum):
    """Requirement types aligned with conventional commits."""

    FEAT = "feat"
    FIX = "fix"
    REFACTOR = "refactor"
    PERF = "perf"
    DOCS = "docs"
    TEST = "test"
    CHORE = "chore"


# ============================================================================
# Project Configuration
# ============================================================================


class TechStack(BaseModel):
    """Technology stack configuration."""

    languages: list[str] = Field(default_factory=list)
    frameworks: list[str] = Field(default_factory=list)
    databases: list[str] = Field(default_factory=list)
    tools: list[str] = Field(default_factory=list)


class ProjectConfig(BaseModel):
    """
    Project configuration synced from SaaS.

    Stored locally at: .vk/config.yaml
    """

    project_id: str
    name: str
    description: str | None = None
    tech_stack: TechStack = Field(default_factory=TechStack)
    objectives: list[str] = Field(default_factory=list)
    success_criteria: list[str] = Field(default_factory=list)
    created_at: datetime | None = None
    updated_at: datetime | None = None


# ============================================================================
# Sprint Configuration
# ============================================================================


class Task(BaseModel):
    """Individual task within a sprint."""

    task_id: str
    title: str
    description: str | None = None
    requirement_id: str | None = None
    status: TaskStatusEnum = TaskStatusEnum.PENDING
    priority: TaskPriority = TaskPriority.MEDIUM
    estimate: int | None = None  # Story points or hours
    assignee: str | None = None
    commit_sha: str | None = None
    started_at: datetime | None = None
    completed_at: datetime | None = None


class Requirement(BaseModel):
    """Requirement within a sprint."""

    requirement_id: str
    title: str
    description: str | None = None
    type: RequirementType = RequirementType.FEAT
    priority: TaskPriority = TaskPriority.MEDIUM
    status: TaskStatusEnum = TaskStatusEnum.PENDING
    tasks: list[Task] = Field(default_factory=list)
    created_at: datetime | None = None


class SprintConfig(BaseModel):
    """
    Sprint configuration synced from SaaS.

    Stored locally at: .vk/sprints/current.yaml
    """

    sprint_id: str
    name: str
    goal: str | None = None
    status: str = "planning"  # planning, active, completed
    start_date: datetime | None = None
    end_date: datetime | None = None
    requirements: list[Requirement] = Field(default_factory=list)
    created_at: datetime | None = None


# ============================================================================
# Rules Configuration
# ============================================================================


class CodingRule(BaseModel):
    """Individual coding rule."""

    rule_id: str
    title: str
    description: str
    category: str  # style, architecture, security, testing
    severity: str = "warning"  # error, warning, info
    examples: list[str] = Field(default_factory=list)


class RulesConfig(BaseModel):
    """
    Project rules synced from SaaS.

    Stored locally at: .vk/rules/*.md
    API returns rules as string arrays, not CodingRule objects.
    """

    coding_standards: list = Field(default_factory=list)  # Can be strings or CodingRule
    architecture_rules: list = Field(default_factory=list)
    security_rules: list = Field(default_factory=list)
    testing_rules: list = Field(default_factory=list)


# ============================================================================
# Roadmap Configuration
# ============================================================================


class MilestoneConfig(BaseModel):
    """Milestone within a roadmap phase."""

    id: str
    name: str
    completed: bool = False


class PhaseConfig(BaseModel):
    """
    Roadmap phase configuration synced from SaaS.

    Stored locally at: .vk/roadmap/phases.yaml
    """

    phase_id: str
    phase_number: int = 1
    name: str
    description: str | None = None
    status: str = "planned"  # planned, in_progress, completed
    milestones: list[MilestoneConfig] = Field(default_factory=list)
    target_date: datetime | None = None
    started_at: datetime | None = None
    completed_at: datetime | None = None


# ============================================================================
# Agent Configuration
# ============================================================================


class AgentConfig(BaseModel):
    """
    Agent configuration synced from SaaS.

    Stored locally at: .vk/agents/*.yaml
    """

    agent_id: str
    name: str
    description: str
    enabled: bool = True
    priority: int = 0
    triggers: list[str] = Field(default_factory=list)  # Events that trigger this agent
    rules: list[str] = Field(default_factory=list)  # Rules this agent must follow
    settings: dict = Field(default_factory=dict)


# ============================================================================
# Tools Configuration
# ============================================================================


class LSPConfig(BaseModel):
    """LSP tool configuration."""

    enabled: bool = True
    languages: list[str] = Field(default_factory=list)
    symbol_operations: bool = True
    auto_import: bool = True
    settings: dict = Field(default_factory=dict)


class LinterConfig(BaseModel):
    """Linter tool configuration."""

    name: str
    enabled: bool = True
    config_file: str | None = None
    settings: dict = Field(default_factory=dict)


class QualityGate(BaseModel):
    """Quality gate configuration."""

    name: str
    enabled: bool = True
    required: bool = False  # Block commit if fails
    command: str | None = None
    settings: dict = Field(default_factory=dict)


class DocsConfig(BaseModel):
    """Documentation tool configuration (context7-style)."""

    enabled: bool = True
    sources: list[str] = Field(default_factory=list)  # Doc sources to include
    auto_fetch: bool = True
    cache_ttl: int = 3600  # Seconds


class ToolsConfig(BaseModel):
    """
    Tools configuration synced from SaaS.

    Stored locally at: .vk/tools/*.yaml
    """

    lsp: LSPConfig = Field(default_factory=LSPConfig)
    linters: list[LinterConfig] = Field(default_factory=list)
    quality_gates: list[QualityGate] = Field(default_factory=list)
    docs: DocsConfig = Field(default_factory=DocsConfig)


# ============================================================================
# Sync Operations
# ============================================================================


class TaskStatus(BaseModel):
    """Task status update for push operations."""

    task_id: str
    status: TaskStatusEnum
    commit_sha: str | None = None
    started_at: datetime | None = None
    completed_at: datetime | None = None


class SyncResult(BaseModel):
    """Result of a sync operation."""

    success: bool
    operation: str  # "pull" or "push"
    files_synced: list[str] = Field(default_factory=list)
    errors: list[str] = Field(default_factory=list)
    timestamp: datetime = Field(default_factory=datetime.now)


# ============================================================================
# Full Sync Payload
# ============================================================================


class PullPayload(BaseModel):
    """Complete payload received from SaaS on pull."""

    project: ProjectConfig
    sprint: SprintConfig | None = None
    roadmap: list[PhaseConfig] = Field(default_factory=list)
    rules: RulesConfig = Field(default_factory=RulesConfig)
    agents: list[AgentConfig] = Field(default_factory=list)
    tools: ToolsConfig = Field(default_factory=ToolsConfig)


class PushPayload(BaseModel):
    """Payload sent to SaaS on push."""

    project_id: str
    task_updates: list[TaskStatus] = Field(default_factory=list)
    metrics: dict = Field(default_factory=dict)
    git_refs: dict = Field(default_factory=dict)  # commit hashes for tasks
    # Bidirectional sync: local changes pushed to SaaS
    rules: dict | None = None  # coding_standards, architecture_rules, etc.
    agents: list[dict] | None = None  # Agent configs
    tools: dict | None = None  # LSP, linters, quality_gates, docs
