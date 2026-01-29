"""StateSet Sandbox Python SDK.

A Python client library for the StateSet Sandbox API, enabling secure
code execution in isolated environments.

Example:
    ```python
    from stateset_sandbox import StateSetSandbox

    client = StateSetSandbox(
        base_url="https://api.sandbox.stateset.app",
        auth_token="sk-sandbox-xxx",
        org_id="org_xxx"
    )

    # Create a sandbox
    sandbox = client.create()

    # Execute a command
    result = client.execute(sandbox.sandbox_id, command=["python", "-c", "print('Hello!')"])
    print(result.stdout)

    # Clean up
    client.stop(sandbox.sandbox_id)
    ```
"""

from .client import StateSetSandbox, register
from .errors import (
    SandboxApiError,
    SandboxAuthenticationError,
    SandboxError,
    SandboxNetworkError,
    SandboxNotFoundError,
    SandboxRateLimitError,
    SandboxTimeoutError,
    SandboxValidationError,
)
from .types import (
    # API Key types
    ApiKey,
    ApiKeyInfo,
    CreateApiKeyOptions,
    CreateApiKeyResponse,
    # Artifact types
    Artifact,
    UploadArtifactOptions,
    # Audit types
    AuditAction,
    AuditEvent,
    AuditSummary,
    # Billing types
    Invoice,
    Subscription,
    SubscriptionResponse,
    # Checkpoint types
    Checkpoint,
    CreateCheckpointOptions,
    # Core sandbox types
    CreateSandboxOptions,
    ExecuteOptions,
    ExecuteResult,
    FileRead,
    FileWrite,
    Sandbox,
    SandboxStatus,
    StreamCallbacks,
    StreamEvent,
    # Organization types
    Organization,
    # Registration types
    RegistrationRequest,
    RegistrationResponse,
    # Secret types
    CreateSecretOptions,
    Secret,
    # Usage types
    UsageDataPoint,
    UsageHistoryResponse,
    UsageSummary,
    # User types
    User,
    # Webhook types
    CreateWebhookOptions,
    Webhook,
    WebhookDelivery,
    WebhookEvent,
)

__version__ = "1.0.4"

__all__ = [
    # Main client
    "StateSetSandbox",
    "register",
    # Errors
    "SandboxError",
    "SandboxApiError",
    "SandboxTimeoutError",
    "SandboxNetworkError",
    "SandboxValidationError",
    "SandboxNotFoundError",
    "SandboxAuthenticationError",
    "SandboxRateLimitError",
    # Core types
    "Sandbox",
    "SandboxStatus",
    "CreateSandboxOptions",
    "ExecuteOptions",
    "ExecuteResult",
    "StreamCallbacks",
    "StreamEvent",
    "FileWrite",
    "FileRead",
    # Registration
    "RegistrationRequest",
    "RegistrationResponse",
    "Organization",
    "User",
    "ApiKeyInfo",
    # API Keys
    "ApiKey",
    "CreateApiKeyOptions",
    "CreateApiKeyResponse",
    # Usage
    "UsageSummary",
    "UsageDataPoint",
    "UsageHistoryResponse",
    # Billing
    "Subscription",
    "SubscriptionResponse",
    "Invoice",
    # Secrets
    "Secret",
    "CreateSecretOptions",
    # Checkpoints
    "Checkpoint",
    "CreateCheckpointOptions",
    # Artifacts
    "Artifact",
    "UploadArtifactOptions",
    # Webhooks
    "Webhook",
    "WebhookEvent",
    "CreateWebhookOptions",
    "WebhookDelivery",
    # Audit
    "AuditAction",
    "AuditEvent",
    "AuditSummary",
]
