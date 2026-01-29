"""Type definitions for StateSet Sandbox SDK."""

from datetime import datetime
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Union

from pydantic import BaseModel, ConfigDict, Field


def _to_camel(value: str) -> str:
    parts = value.split("_")
    return parts[0] + "".join(word.capitalize() for word in parts[1:])


API_MODEL_CONFIG = ConfigDict(
    populate_by_name=True,
    alias_generator=_to_camel,
    extra="ignore",
)

STREAM_MODEL_CONFIG = ConfigDict(
    populate_by_name=True,
    alias_generator=_to_camel,
    extra="ignore",
    arbitrary_types_allowed=True,
)


class ApiModel(BaseModel):
    model_config = API_MODEL_CONFIG


class SandboxStatus(str, Enum):
    """Sandbox lifecycle states."""
    CREATING = "creating"
    RUNNING = "running"
    TERMINATING = "terminating"
    TERMINATED = "terminated"
    ERROR = "error"


class Sandbox(ApiModel):
    """Sandbox instance details."""
    sandbox_id: str
    org_id: str
    session_id: str
    status: SandboxStatus
    pod_ip: Optional[str] = None
    created_at: datetime
    expires_at: datetime
    cpus: Optional[str] = None
    memory: Optional[str] = None


class CreateSandboxOptions(ApiModel):
    """Options for creating a sandbox."""
    cpus: Optional[str] = None
    memory: Optional[str] = None
    timeout_seconds: Optional[int] = None
    env: Optional[Dict[str, str]] = None
    template: Optional[str] = None


class ExecuteOptions(ApiModel):
    """Options for executing a command."""
    command: Union[str, List[str]]
    timeout: Optional[int] = None
    env: Optional[Dict[str, str]] = None
    cwd: Optional[str] = None


class ExecuteResult(ApiModel):
    """Result of command execution."""
    exit_code: int
    stdout: str
    stderr: str


class FileWrite(ApiModel):
    """File to write to sandbox."""
    path: str
    content: str  # Base64 encoded


class FileRead(ApiModel):
    """File read from sandbox."""
    path: str
    content: str  # Base64 encoded
    size: int


class StreamEvent(ApiModel):
    """Event from streaming execution."""
    type: str
    data: Optional[str] = None
    code: Optional[int] = None
    error: Optional[str] = None


class StreamCallbacks(ApiModel):
    """Callbacks for streaming execution."""
    on_stdout: Optional[Callable[[str], None]] = None
    on_stderr: Optional[Callable[[str], None]] = None
    on_exit: Optional[Callable[[int], None]] = None
    on_error: Optional[Callable[[Exception], None]] = None

    model_config = STREAM_MODEL_CONFIG


# Registration types
class RegistrationRequest(ApiModel):
    """Request to register a new organization."""
    email: str
    organization_name: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    use_case: Optional[str] = None


class Organization(ApiModel):
    """Organization details."""
    id: str
    name: str
    slug: str
    plan: str


class User(ApiModel):
    """User details."""
    id: str
    email: str
    role: str


class ApiKeyInfo(ApiModel):
    """API key information."""
    key: str
    key_prefix: str
    name: str


class RegistrationResponse(ApiModel):
    """Response from registration."""
    organization: Organization
    user: User
    api_key: ApiKeyInfo


# API Key Management
class ApiKey(ApiModel):
    """API key details."""
    id: str
    name: str
    key_prefix: str
    scopes: List[str]
    last_used_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None
    created_at: datetime


class CreateApiKeyOptions(ApiModel):
    """Options for creating an API key."""
    name: str
    expires_in_days: Optional[int] = None
    scopes: Optional[List[str]] = None


class CreateApiKeyResponse(ApiModel):
    """Response from creating an API key."""
    api_key: ApiKey
    key: str  # Full key (only shown once)


# Usage types
class UsageSummary(ApiModel):
    """Usage summary for billing period."""
    period_start: datetime
    period_end: datetime
    cpu_hours: float
    memory_gb_hours: float
    network_gb: float
    sandbox_creations: int
    estimated_cost_cents: int
    breakdown: Dict[str, int]


class UsageDataPoint(ApiModel):
    """Single usage data point."""
    period_start: datetime
    period_end: datetime
    cpu_hours: float
    memory_gb_hours: float
    network_gb: float
    sandbox_creations: int


class UsageHistoryResponse(ApiModel):
    """Usage history response."""
    granularity: str
    start_date: datetime
    end_date: datetime
    data: List[UsageDataPoint]


# Billing types
class Subscription(ApiModel):
    """Subscription details."""
    id: str
    status: str
    plan: str
    current_period_start: datetime
    current_period_end: datetime
    cancel_at_period_end: bool


class SubscriptionResponse(ApiModel):
    """Subscription response."""
    subscription: Optional[Subscription] = None
    plan: str


class Invoice(ApiModel):
    """Invoice details."""
    id: str
    number: Optional[str] = None
    amount_due: int
    amount_paid: int
    status: str
    created: datetime
    period_start: datetime
    period_end: datetime
    pdf_url: Optional[str] = None


# Secret types
class Secret(ApiModel):
    """Secret details (value not included)."""
    id: str
    name: str
    scope: str
    allowed_sandbox_patterns: Optional[List[str]] = None
    expires_at: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None


class CreateSecretOptions(ApiModel):
    """Options for creating a secret."""
    name: str
    value: str
    scope: str = "sandbox"


# Checkpoint types
class Checkpoint(ApiModel):
    """Checkpoint details."""
    id: str
    sandbox_id: str
    org_id: str
    name: str
    description: Optional[str] = None
    created_at: datetime
    size: int
    file_count: int
    checksum: str
    metadata: Dict[str, Any] = Field(default_factory=dict)


class CreateCheckpointOptions(ApiModel):
    """Options for creating a checkpoint."""
    name: str
    description: Optional[str] = None
    include_paths: Optional[List[str]] = None
    exclude_paths: Optional[List[str]] = None
    include_env: bool = False


# Artifact types
class Artifact(ApiModel):
    """Artifact details."""
    id: str
    sandbox_id: str
    org_id: str
    path: str
    remote_path: str
    size: int
    checksum: str
    content_type: str
    created_at: datetime
    expires_at: Optional[datetime] = None
    metadata: Dict[str, str] = Field(default_factory=dict)


class UploadArtifactOptions(ApiModel):
    """Options for uploading an artifact."""
    path: str
    content_type: Optional[str] = None
    expires_in: Optional[int] = None
    metadata: Optional[Dict[str, str]] = None


# Webhook types
class WebhookEvent(str, Enum):
    """Webhook event types."""
    SANDBOX_CREATED = "sandbox.created"
    SANDBOX_READY = "sandbox.ready"
    SANDBOX_STOPPED = "sandbox.stopped"
    SANDBOX_ERROR = "sandbox.error"
    SANDBOX_TIMEOUT = "sandbox.timeout"
    COMMAND_STARTED = "command.started"
    COMMAND_COMPLETED = "command.completed"
    COMMAND_FAILED = "command.failed"
    FILE_WRITTEN = "file.written"
    ARTIFACT_UPLOADED = "artifact.uploaded"
    CHECKPOINT_CREATED = "checkpoint.created"
    CHECKPOINT_RESTORED = "checkpoint.restored"


class Webhook(ApiModel):
    """Webhook configuration."""
    id: str
    url: str
    events: Union[List[WebhookEvent], str]  # List or "*"
    secret: Optional[str] = None
    enabled: bool
    headers: Optional[Dict[str, str]] = None
    retry_count: int = 3
    retry_delay_ms: int = 1000
    timeout_ms: int = 30000
    created_at: datetime


class CreateWebhookOptions(ApiModel):
    """Options for creating a webhook."""
    url: str
    events: Union[List[WebhookEvent], str] = "*"
    secret: Optional[str] = None
    headers: Optional[Dict[str, str]] = None
    retry_count: int = 3
    retry_delay_ms: int = 1000
    timeout_ms: int = 30000


class WebhookDelivery(ApiModel):
    """Webhook delivery record."""
    id: str
    webhook_id: str
    event: str
    status: str
    attempts: int
    last_attempt_at: Optional[datetime] = None
    response_status: Optional[int] = None
    error: Optional[str] = None
    created_at: datetime


# Audit types
class AuditAction(str, Enum):
    """Audit action types."""
    SANDBOX_CREATE = "sandbox.create"
    SANDBOX_STOP = "sandbox.stop"
    SANDBOX_DELETE = "sandbox.delete"
    FILE_WRITE = "file.write"
    FILE_READ = "file.read"
    FILE_DELETE = "file.delete"
    COMMAND_EXECUTE = "command.execute"
    MCP_START = "mcp.start"
    MCP_STOP = "mcp.stop"
    ARTIFACT_UPLOAD = "artifact.upload"
    ARTIFACT_DOWNLOAD = "artifact.download"
    SECRET_INJECT = "secret.inject"
    SECRET_ACCESS = "secret.access"
    CHECKPOINT_CREATE = "checkpoint.create"
    CHECKPOINT_RESTORE = "checkpoint.restore"


class AuditEvent(ApiModel):
    """Audit event record."""
    id: str
    timestamp: datetime
    sandbox_id: str
    org_id: str
    user_id: Optional[str] = None
    session_id: str
    action: str
    resource: str
    details: Dict[str, Any]
    outcome: str
    error_message: Optional[str] = None
    duration: Optional[int] = None


class AuditSummary(ApiModel):
    """Audit summary for a sandbox."""
    total_events: int
    commands_executed: int
    files_written: int
    files_read: int
    secrets_accessed: int
    errors: int
    duration: int
