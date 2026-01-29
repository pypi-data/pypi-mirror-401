"""StateSet Sandbox client implementation."""

import base64
import uuid
from typing import Any, Callable, Dict, List, Optional, Union

import httpx

from .errors import (
    SandboxApiError,
    SandboxNetworkError,
    SandboxTimeoutError,
    SandboxValidationError,
)
from .types import (
    ApiKey,
    Artifact,
    AuditEvent,
    AuditSummary,
    Checkpoint,
    CreateApiKeyOptions,
    CreateApiKeyResponse,
    CreateCheckpointOptions,
    CreateSandboxOptions,
    CreateSecretOptions,
    CreateWebhookOptions,
    ExecuteOptions,
    ExecuteResult,
    FileRead,
    Invoice,
    RegistrationRequest,
    RegistrationResponse,
    Sandbox,
    Secret,
    SubscriptionResponse,
    UploadArtifactOptions,
    UsageHistoryResponse,
    UsageSummary,
    Webhook,
    WebhookDelivery,
)


class StateSetSandbox:
    """Client for the StateSet Sandbox API.

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
        print(f"Created sandbox: {sandbox.sandbox_id}")

        # Execute a command
        result = client.execute(sandbox.sandbox_id, command=["echo", "Hello!"])
        print(result.stdout)

        # Clean up
        client.stop(sandbox.sandbox_id)
        ```
    """

    def __init__(
        self,
        base_url: str,
        auth_token: str,
        org_id: Optional[str] = None,
        timeout: int = 30000,
        api_version: str = "v1",
    ) -> None:
        """Initialize the sandbox client.

        Args:
            base_url: The base URL of the sandbox API.
            auth_token: API key or JWT token for authentication.
            org_id: Organization ID (required for API key auth).
            timeout: Request timeout in milliseconds.
            api_version: API version to use.
        """
        if not base_url:
            raise SandboxValidationError("base_url is required")

        if not auth_token or not auth_token.strip():
            raise SandboxValidationError(
                "auth_token is required. Provide a valid JWT token or API key."
            )

        # Validate that org_id is provided for API key auth
        is_jwt = "." in auth_token
        if not is_jwt and not org_id:
            raise SandboxValidationError(
                "org_id is required when using API key authentication."
            )

        self.base_url = base_url.rstrip("/")
        self.auth_token = auth_token
        self.org_id = org_id
        self.timeout = timeout / 1000  # Convert to seconds for httpx
        self.api_version = api_version

        self._client = httpx.Client(timeout=self.timeout)

    def __enter__(self) -> "StateSetSandbox":
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()

    def close(self) -> None:
        """Close the HTTP client."""
        self._client.close()

    def _get_headers(self) -> Dict[str, str]:
        """Get request headers with authentication."""
        headers = {"Content-Type": "application/json"}

        if "." in self.auth_token:
            # JWT token
            headers["Authorization"] = f"Bearer {self.auth_token}"
        else:
            # API key
            headers["Authorization"] = f"ApiKey {self.auth_token}"
            if self.org_id:
                headers["X-Org-Id"] = self.org_id

        return headers

    def _request(
        self,
        method: str,
        path: str,
        body: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
    ) -> Any:
        """Make an API request."""
        request_id = str(uuid.uuid4())
        url = f"{self.base_url}/api/{self.api_version}{path}"

        headers = self._get_headers()
        headers["X-Request-Id"] = request_id

        try:
            response = self._client.request(
                method=method,
                url=url,
                headers=headers,
                json=body,
                params=params,
            )

            server_request_id = response.headers.get("x-request-id", request_id)

            if not response.is_success:
                try:
                    error_body = response.json()
                except Exception:
                    error_body = {"error": response.text or "Unknown error"}
                raise SandboxApiError.from_response(
                    error_body, response.status_code, server_request_id
                )

            return response.json()

        except httpx.TimeoutException as e:
            raise SandboxTimeoutError(
                f"Request timed out after {self.timeout * 1000}ms",
                int(self.timeout * 1000),
                request_id,
            ) from e

        except httpx.RequestError as e:
            raise SandboxNetworkError(
                f"Network error: {str(e)}",
                e,
                request_id,
            ) from e

    # ===========================================
    # Sandbox Operations
    # ===========================================

    def create(self, options: Optional[CreateSandboxOptions] = None) -> Sandbox:
        """Create a new sandbox.

        Args:
            options: Optional configuration for the sandbox.

        Returns:
            The created sandbox details.
        """
        body = options.model_dump(exclude_none=True) if options else {}
        if self.org_id:
            body["org_id"] = self.org_id
        response = self._request("POST", "/sandbox/create", body)
        return Sandbox(**response)

    def get(self, sandbox_id: str) -> Sandbox:
        """Get sandbox details.

        Args:
            sandbox_id: The sandbox ID.

        Returns:
            The sandbox details.
        """
        response = self._request("GET", f"/sandbox/{sandbox_id}")
        return Sandbox(**response)

    def list(self) -> List[Sandbox]:
        """List all sandboxes for the organization.

        Returns:
            List of sandboxes.
        """
        params = {"org_id": self.org_id} if self.org_id else None
        response = self._request("GET", "/sandboxes", params=params)
        return [Sandbox(**s) for s in response.get("sandboxes", [])]

    def execute(
        self,
        sandbox_id: str,
        command: Union[str, List[str]],
        timeout: Optional[int] = None,
        env: Optional[Dict[str, str]] = None,
        cwd: Optional[str] = None,
        working_dir: Optional[str] = None,
    ) -> ExecuteResult:
        """Execute a command in the sandbox.

        Args:
            sandbox_id: The sandbox ID.
            command: Command to execute (string or list of args).
            timeout: Command timeout in milliseconds.
            env: Environment variables.
            cwd: Working directory (alias for working_dir).
            working_dir: Working directory (preferred).

        Returns:
            The execution result.
        """
        body: Dict[str, Any] = {"command": command, "stream": False}
        if timeout:
            body["timeout"] = timeout
        if env:
            body["env"] = env
        resolved_dir = working_dir or cwd
        if resolved_dir:
            body["working_dir"] = resolved_dir

        response = self._request("POST", f"/sandbox/{sandbox_id}/execute", body)
        return ExecuteResult(**response)

    def execute_stream(
        self,
        sandbox_id: str,
        command: Union[str, List[str]],
        on_stdout: Optional[Callable[[str], None]] = None,
        on_stderr: Optional[Callable[[str], None]] = None,
        on_exit: Optional[Callable[[int], None]] = None,
        on_error: Optional[Callable[[Exception], None]] = None,
        cwd: Optional[str] = None,
        working_dir: Optional[str] = None,
        timeout: Optional[int] = None,
        env: Optional[Dict[str, str]] = None,
    ) -> None:
        """Execute a command with streaming output.

        Args:
            sandbox_id: The sandbox ID.
            command: Command to execute.
            on_stdout: Callback for stdout data.
            on_stderr: Callback for stderr data.
            on_exit: Callback for exit code.
            on_error: Callback for errors.
            cwd: Working directory (alias for working_dir).
            working_dir: Working directory (preferred).
            timeout: Command timeout in milliseconds.
            env: Environment variables.
        """
        request_id = str(uuid.uuid4())
        url = f"{self.base_url}/api/{self.api_version}/sandbox/{sandbox_id}/execute"

        headers = self._get_headers()
        headers["X-Request-Id"] = request_id

        body: Dict[str, Any] = {"command": command, "stream": True}
        if timeout:
            body["timeout"] = timeout
        resolved_dir = working_dir or cwd
        if resolved_dir:
            body["working_dir"] = resolved_dir
        if env:
            body["env"] = env

        with self._client.stream("POST", url, headers=headers, json=body) as response:
            if not response.is_success:
                error_body = {"error": "Stream request failed"}
                raise SandboxApiError.from_response(
                    error_body, response.status_code, request_id
                )

            for line in response.iter_lines():
                if line.startswith("data: "):
                    import json

                    try:
                        event = json.loads(line[6:])
                        event_type = event.get("type")

                        if event_type == "stdout" and on_stdout:
                            on_stdout(event.get("data", ""))
                        elif event_type == "stderr" and on_stderr:
                            on_stderr(event.get("data", ""))
                        elif event_type == "exit" and on_exit:
                            on_exit(event.get("code", 0))
                        elif event_type == "error" and on_error:
                            on_error(Exception(event.get("error", "Unknown error")))
                        elif event_type == "done":
                            return
                    except json.JSONDecodeError:
                        pass

    def write_file(self, sandbox_id: str, path: str, content: str) -> None:
        """Write a file to the sandbox.

        Args:
            sandbox_id: The sandbox ID.
            path: File path in the sandbox.
            content: File content (will be base64 encoded).
        """
        encoded = base64.b64encode(content.encode()).decode()
        self._request(
            "POST",
            f"/sandbox/{sandbox_id}/files",
            {"files": [{"path": path, "content": encoded}]},
        )

    def write_files(self, sandbox_id: str, files: List[Dict[str, str]]) -> None:
        """Write multiple files to the sandbox.

        Args:
            sandbox_id: The sandbox ID.
            files: List of {"path": str, "content": str} dicts.
        """
        encoded_files = [
            {"path": f["path"], "content": base64.b64encode(f["content"].encode()).decode()}
            for f in files
        ]
        self._request("POST", f"/sandbox/{sandbox_id}/files", {"files": encoded_files})

    def read_file(self, sandbox_id: str, path: str) -> str:
        """Read a file from the sandbox.

        Args:
            sandbox_id: The sandbox ID.
            path: File path in the sandbox.

        Returns:
            The file content (decoded from base64).
        """
        response = self._request("GET", f"/sandbox/{sandbox_id}/files", params={"path": path})
        content = response.get("content", "")
        return base64.b64decode(content).decode()

    def read_file_raw(self, sandbox_id: str, path: str) -> FileRead:
        """Read a file with metadata.

        Args:
            sandbox_id: The sandbox ID.
            path: File path in the sandbox.

        Returns:
            File read response with content and metadata.
        """
        response = self._request("GET", f"/sandbox/{sandbox_id}/files", params={"path": path})
        return FileRead(**response)

    def stop(self, sandbox_id: str) -> bool:
        """Stop and delete a sandbox.

        Args:
            sandbox_id: The sandbox ID.

        Returns:
            True if successful.
        """
        response = self._request("POST", f"/sandbox/{sandbox_id}/stop")
        return response.get("success", False)

    def delete(self, sandbox_id: str) -> bool:
        """Delete a sandbox (alias for stop).

        Args:
            sandbox_id: The sandbox ID.

        Returns:
            True if successful.
        """
        response = self._request("DELETE", f"/sandbox/{sandbox_id}")
        return response.get("success", False)

    # ===========================================
    # API Key Management
    # ===========================================

    def list_api_keys(self) -> List[ApiKey]:
        """List all API keys for the organization."""
        response = self._request("GET", "/api-keys")
        return [ApiKey(**k) for k in response.get("api_keys", [])]

    def create_api_key(self, options: CreateApiKeyOptions) -> CreateApiKeyResponse:
        """Create a new API key."""
        response = self._request("POST", "/api-keys", options.model_dump(exclude_none=True))
        return CreateApiKeyResponse(**response)

    def revoke_api_key(self, key_id: str) -> bool:
        """Revoke an API key."""
        response = self._request("DELETE", f"/api-keys/{key_id}")
        return response.get("success", False)

    # ===========================================
    # Usage
    # ===========================================

    def get_current_usage(self) -> UsageSummary:
        """Get current billing period usage."""
        response = self._request("GET", "/usage/current")
        return UsageSummary(**response)

    def get_usage_history(
        self,
        granularity: str = "daily",
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> UsageHistoryResponse:
        """Get usage history."""
        params: Dict[str, str] = {"granularity": granularity}
        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date
        response = self._request("GET", "/usage/history", params=params)
        return UsageHistoryResponse(**response)

    # ===========================================
    # Billing
    # ===========================================

    def get_subscription(self) -> SubscriptionResponse:
        """Get current subscription details."""
        response = self._request("GET", "/billing/subscription")
        return SubscriptionResponse(**response)

    def upgrade_plan(self, plan: str, success_url: str, cancel_url: str) -> str:
        """Upgrade to a different plan. Returns Stripe checkout URL."""
        response = self._request(
            "POST",
            "/billing/upgrade",
            {"plan": plan, "success_url": success_url, "cancel_url": cancel_url},
        )
        return response.get("url", "")

    def get_billing_portal(self, return_url: str) -> str:
        """Get Stripe billing portal URL."""
        response = self._request("POST", "/billing/portal", {"return_url": return_url})
        return response.get("url", "")

    def list_invoices(self, limit: int = 10) -> List[Invoice]:
        """List invoices."""
        response = self._request("GET", "/billing/invoices", params={"limit": limit})
        return [Invoice(**i) for i in response.get("invoices", [])]

    # ===========================================
    # Secrets
    # ===========================================

    def list_secrets(self) -> List[Secret]:
        """List all secrets for the organization."""
        response = self._request("GET", "/secrets")
        return [Secret(**s) for s in response.get("secrets", [])]

    def create_secret(self, options: CreateSecretOptions) -> Secret:
        """Create a new secret."""
        response = self._request("POST", "/secrets", options.model_dump())
        return Secret(**response.get("secret", response))

    def update_secret(self, name: str, value: str) -> Secret:
        """Update an existing secret."""
        response = self._request("PUT", f"/secrets/{name}", {"value": value})
        return Secret(**response.get("secret", response))

    def delete_secret(self, name: str) -> bool:
        """Delete a secret."""
        response = self._request("DELETE", f"/secrets/{name}")
        return response.get("success", False)

    def inject_secrets(
        self,
        sandbox_id: str,
        secrets: Optional[List[str]] = None,
        all_secrets: bool = False,
    ) -> List[str]:
        """Inject secrets into a sandbox."""
        body: Dict[str, Any] = {}
        if secrets:
            body["secrets"] = secrets
        if all_secrets:
            body["all"] = True
        response = self._request("POST", f"/sandbox/{sandbox_id}/secrets/inject", body)
        return response.get("injected", [])

    # ===========================================
    # Checkpoints
    # ===========================================

    def list_checkpoints(self, sandbox_id: Optional[str] = None) -> List[Checkpoint]:
        """List checkpoints."""
        params = {"sandbox_id": sandbox_id} if sandbox_id else None
        response = self._request("GET", "/checkpoints", params=params)
        return [Checkpoint(**c) for c in response.get("checkpoints", [])]

    def get_checkpoint(self, checkpoint_id: str) -> Checkpoint:
        """Get checkpoint details."""
        response = self._request("GET", f"/checkpoints/{checkpoint_id}")
        return Checkpoint(**response)

    def create_checkpoint(
        self, sandbox_id: str, options: CreateCheckpointOptions
    ) -> Checkpoint:
        """Create a checkpoint."""
        response = self._request(
            "POST",
            f"/sandbox/{sandbox_id}/checkpoints",
            options.model_dump(exclude_none=True),
        )
        return Checkpoint(**response)

    def restore_checkpoint(
        self,
        sandbox_id: str,
        checkpoint_id: str,
        restore_files: bool = True,
        restore_env: bool = False,
        overwrite: bool = True,
    ) -> bool:
        """Restore a checkpoint to a sandbox."""
        response = self._request(
            "POST",
            f"/sandbox/{sandbox_id}/checkpoints/restore",
            {
                "checkpoint_id": checkpoint_id,
                "restore_files": restore_files,
                "restore_env": restore_env,
                "overwrite": overwrite,
            },
        )
        return response.get("success", False)

    def clone_checkpoint(self, checkpoint_id: str, name: str) -> Checkpoint:
        """Clone a checkpoint."""
        response = self._request(
            "POST", f"/checkpoints/{checkpoint_id}/clone", {"name": name}
        )
        return Checkpoint(**response)

    def delete_checkpoint(self, checkpoint_id: str) -> bool:
        """Delete a checkpoint."""
        response = self._request("DELETE", f"/checkpoints/{checkpoint_id}")
        return response.get("success", False)

    # ===========================================
    # Artifacts
    # ===========================================

    def list_artifacts(self, sandbox_id: Optional[str] = None) -> List[Artifact]:
        """List artifacts."""
        params = {"sandbox_id": sandbox_id} if sandbox_id else None
        response = self._request("GET", "/artifacts", params=params)
        return [Artifact(**a) for a in response.get("artifacts", [])]

    def get_artifact(self, artifact_id: str) -> Artifact:
        """Get artifact details."""
        response = self._request("GET", f"/artifacts/{artifact_id}")
        return Artifact(**response)

    def get_artifact_url(self, artifact_id: str, expires_in: int = 3600) -> str:
        """Get a download URL for an artifact."""
        response = self._request(
            "GET", f"/artifacts/{artifact_id}/url", params={"expires_in": expires_in}
        )
        return response.get("url", "")

    def upload_artifact(
        self, sandbox_id: str, options: UploadArtifactOptions
    ) -> Artifact:
        """Upload an artifact from a sandbox."""
        response = self._request(
            "POST",
            f"/sandbox/{sandbox_id}/artifacts/upload",
            options.model_dump(exclude_none=True),
        )
        return Artifact(**response)

    def delete_artifact(self, artifact_id: str) -> bool:
        """Delete an artifact."""
        response = self._request("DELETE", f"/artifacts/{artifact_id}")
        return response.get("success", False)

    # ===========================================
    # Webhooks
    # ===========================================

    def list_webhooks(self) -> List[Webhook]:
        """List webhooks."""
        response = self._request("GET", "/webhooks")
        return [Webhook(**w) for w in response.get("webhooks", [])]

    def create_webhook(self, options: CreateWebhookOptions) -> Webhook:
        """Create a webhook."""
        response = self._request("POST", "/webhooks", options.model_dump(exclude_none=True))
        return Webhook(**response)

    def delete_webhook(self, webhook_id: str) -> bool:
        """Delete a webhook."""
        response = self._request("DELETE", f"/webhooks/{webhook_id}")
        return response.get("success", False)

    def test_webhook(self, webhook_id: str) -> Dict[str, Any]:
        """Test a webhook."""
        return self._request("POST", f"/webhooks/{webhook_id}/test")

    def get_webhook_deliveries(
        self, webhook_id: str, limit: int = 50
    ) -> List[WebhookDelivery]:
        """Get webhook delivery history."""
        response = self._request(
            "GET", f"/webhooks/{webhook_id}/deliveries", params={"limit": limit}
        )
        return [WebhookDelivery(**d) for d in response.get("deliveries", [])]

    # ===========================================
    # Audit Logs
    # ===========================================

    def list_audit_events(
        self,
        sandbox_id: Optional[str] = None,
        action: Optional[str] = None,
        outcome: Optional[str] = None,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> Dict[str, Any]:
        """List audit events."""
        params: Dict[str, Any] = {"limit": limit, "offset": offset}
        if sandbox_id:
            params["sandbox_id"] = sandbox_id
        if action:
            params["action"] = action
        if outcome:
            params["outcome"] = outcome
        if start_time:
            params["start_time"] = start_time
        if end_time:
            params["end_time"] = end_time

        response = self._request("GET", "/audit", params=params)
        return {
            "events": [AuditEvent(**e) for e in response.get("events", [])],
            "total": response.get("total", 0),
        }

    def get_sandbox_audit_summary(self, sandbox_id: str) -> AuditSummary:
        """Get audit summary for a sandbox."""
        response = self._request("GET", f"/sandbox/{sandbox_id}/audit/summary")
        return AuditSummary(**response)


# ===========================================
# Static Registration Function
# ===========================================


def register(
    base_url: str,
    request: RegistrationRequest,
    timeout: int = 30000,
) -> RegistrationResponse:
    """Register a new organization and user.

    This function doesn't require authentication.

    Args:
        base_url: The base URL of the sandbox API.
        request: Registration request details.
        timeout: Request timeout in milliseconds.

    Returns:
        Registration response with organization, user, and API key.
    """
    url = f"{base_url.rstrip('/')}/api/v1/register"
    request_id = str(uuid.uuid4())

    try:
        with httpx.Client(timeout=timeout / 1000) as client:
            response = client.post(
                url,
                headers={
                    "Content-Type": "application/json",
                    "X-Request-Id": request_id,
                },
                json=request.model_dump(exclude_none=True),
            )

            server_request_id = response.headers.get("x-request-id", request_id)

            if not response.is_success:
                try:
                    error_body = response.json()
                except Exception:
                    error_body = {"error": response.text or "Unknown error"}
                raise SandboxApiError.from_response(
                    error_body, response.status_code, server_request_id
                )

            return RegistrationResponse(**response.json())

    except httpx.TimeoutException as e:
        raise SandboxTimeoutError(
            f"Registration request timed out after {timeout}ms",
            timeout,
            request_id,
        ) from e

    except httpx.RequestError as e:
        raise SandboxNetworkError(
            f"Network error during registration: {str(e)}",
            e,
            request_id,
        ) from e
