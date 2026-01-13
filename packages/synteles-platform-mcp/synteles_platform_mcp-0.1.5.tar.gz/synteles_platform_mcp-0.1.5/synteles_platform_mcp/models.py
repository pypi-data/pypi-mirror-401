"""Pydantic models for request/response validation."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field

# ================================
# Request Models
# ================================


class CreateAgentletRequest(BaseModel):
    """Request model for creating an agentlet."""

    id: str = Field(..., pattern=r"^[a-zA-Z_][a-zA-Z0-9_]*$", description="Agentlet identifier")
    description: str | None = Field(None, description="Optional description")
    YAML: str | None = Field(None, description="Optional YAML configuration")


class UpdateAgentletRequest(BaseModel):
    """Request model for updating an agentlet."""

    description: str | None = Field(None, description="Updated description")
    YAML: str | None = Field(None, description="Updated YAML configuration")


class CreateAPIKeyRequest(BaseModel):
    """Request model for creating an API key."""

    key_name: str = Field(..., description="Descriptive name for the API key")


class CreateExecutionRequest(BaseModel):
    """Request model for creating an execution."""

    cloud_provider: str = Field("gcp", pattern=r"^(gcp|azure)$", description="Cloud provider (gcp or azure)")
    prompt: str | None = Field(None, description="Optional task description")
    timeout: int = Field(3600, ge=1, le=86400, description="Timeout in seconds (1-86400)")


# ================================
# Response Models
# ================================


class UserProfile(BaseModel):
    """User profile response model."""

    sub: str = Field(..., description="Cognito user UUID")
    email: str = Field(..., description="User's email address")
    name: str = Field(..., description="User's full name")
    given_name: str = Field(..., description="User's first name")
    family_name: str = Field(..., description="User's last name")
    picture: str | None = Field(None, description="Profile picture URL")
    org_id: str | None = Field(None, description="Organization UUID")
    org_name: str | None = Field(None, description="Organization name")


class Organization(BaseModel):
    """Organization response model."""

    org_name: str = Field(..., description="Organization name")
    users: list[str] = Field(..., description="List of user UUIDs")


class AgentletSummary(BaseModel):
    """Agentlet summary (without YAML)."""

    id: str = Field(..., description="Agentlet identifier")
    description: str | None = Field(None, description="Agentlet description")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")


class AgentletDetail(BaseModel):
    """Complete agentlet with YAML."""

    description: str | None = Field(None, description="Agentlet description")
    YAML: str | None = Field(None, description="YAML configuration")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")


class APIKeySummary(BaseModel):
    """API key summary response."""

    key_id: str = Field(..., description="API key UUID")
    key_name: str = Field(..., description="API key name")
    created_at: datetime = Field(..., description="Creation timestamp")
    last_used: datetime | None = Field(None, description="Last usage timestamp")


class APIKeyDetail(BaseModel):
    """API key creation response (includes actual key)."""

    key_id: str = Field(..., description="API key UUID")
    key: str = Field(..., description="The actual API key (43 characters)")
    key_name: str = Field(..., description="API key name")
    created_at: datetime = Field(..., description="Creation timestamp")


class ExecutionSummary(BaseModel):
    """Execution summary response."""

    execution_id: str = Field(..., description="Execution UUID")
    agentlet_id: str = Field(..., description="Agentlet identifier")
    status: str = Field(..., description="Execution status")
    cloud_provider: str = Field(..., description="Cloud provider used")
    created_at: datetime = Field(..., description="Creation timestamp")
    completed_at: datetime | None = Field(None, description="Completion timestamp")
    logs_s3_uri: str | None = Field(None, description="S3 URI for logs")
    elapsed_seconds: int | None = Field(None, description="Total execution time")


class PaginatedResponse(BaseModel):
    """Generic paginated response wrapper."""

    count: int = Field(..., description="Number of items in current response")
    next_token: str | None = Field(None, description="Token for next page (if available)")


class PaginatedAgentletResponse(PaginatedResponse):
    """Paginated agentlet list response."""

    agentlets: list[dict[str, Any]] = Field(..., description="List of agentlets")


class PaginatedAPIKeyResponse(PaginatedResponse):
    """Paginated API key list response."""

    api_keys: list[dict[str, Any]] = Field(..., description="List of API keys")


class PaginatedExecutionResponse(PaginatedResponse):
    """Paginated execution list response."""

    executions: list[dict[str, Any]] = Field(..., description="List of executions")
