"""CLI and API Client error classes."""

from konic.common.errors.base import KonicError

__all__ = [
    "KonicCLIError",
    "KonicConfigurationError",
    "KonicAPIClientError",
    "KonicHTTPError",
    "KonicValidationError",
    "KonicEnvironmentError",
    "KonicAgentNotFoundError",
    "KonicAgentConflictError",
    "KonicAgentResolutionError",
    "KonicTrainingJobNotFoundError",
    "KonicTrainingJobError",
    "KonicDataNotFoundError",
    "KonicDataConflictError",
    "KonicDataValidationError",
    "KonicArtifactNotFoundError",
    "KonicInferenceServerNotFoundError",
    "KonicModelNotFoundError",
    "KonicModelConflictError",
    "KonicModelGatedError",
]


class KonicCLIError(KonicError):
    """Base exception for CLI-related errors."""

    def __init__(self, message: str, exit_code: int = 1):
        super().__init__(message)
        self.exit_code = exit_code


class KonicConfigurationError(KonicCLIError):
    """Configuration error (missing env vars, invalid config)."""

    def __init__(self, message: str, config_key: str | None = None):
        super().__init__(message, exit_code=1)
        self.config_key = config_key


class KonicEnvironmentError(KonicConfigurationError):
    """Missing or invalid environment variable."""

    def __init__(self, env_var: str, suggestion: str | None = None):
        message = f"Missing or invalid environment variable: {env_var}"
        if suggestion:
            message += f"\n💡 Suggestion: {suggestion}"
        super().__init__(message, config_key=env_var)
        self.env_var = env_var


class KonicAPIClientError(KonicCLIError):
    """Base exception for API client errors."""

    def __init__(self, message: str, endpoint: str | None = None):
        super().__init__(message, exit_code=1)
        self.endpoint = endpoint


class KonicHTTPError(KonicAPIClientError):
    """HTTP request failure."""

    def __init__(
        self,
        message: str,
        status_code: int,
        endpoint: str | None = None,
        response_body: str | None = None,
    ):
        super().__init__(message, endpoint=endpoint)
        self.status_code = status_code
        self.response_body = response_body

    def __str__(self) -> str:
        base = f"HTTP {self.status_code}"
        if self.endpoint:
            base += f" at {self.endpoint}"
        base += f": {self.message}"
        return base


class KonicValidationError(KonicCLIError):
    """Input validation failure."""

    def __init__(self, message: str, field: str | None = None):
        super().__init__(message, exit_code=1)
        self.field = field


class KonicAgentNotFoundError(KonicAPIClientError):
    """Agent not found (404)."""

    def __init__(self, agent_identifier: str):
        message = f"Agent not found: {agent_identifier}"
        super().__init__(message, endpoint="/agents")
        self.agent_identifier = agent_identifier


class KonicAgentConflictError(KonicAPIClientError):
    """Agent name already exists (409)."""

    def __init__(self, agent_name: str):
        message = f"Agent with name '{agent_name}' already exists. Use 'konic agent update' to add a new version."
        super().__init__(message, endpoint="/agents/upload")
        self.agent_name = agent_name


class KonicAgentResolutionError(KonicAPIClientError):
    """Multiple agents match name."""

    def __init__(self, agent_name: str, count: int):
        message = f"Multiple agents ({count}) found with name '{agent_name}'. Please use the agent ID instead."
        super().__init__(message, endpoint="/agents")
        self.agent_name = agent_name
        self.count = count


class KonicTrainingJobNotFoundError(KonicAPIClientError):
    """Training job not found (404)."""

    def __init__(self, job_id: str):
        message = f"Training job not found: {job_id}"
        super().__init__(message, endpoint="/training/jobs")
        self.job_id = job_id


class KonicTrainingJobError(KonicAPIClientError):
    """Training job operation error."""

    def __init__(self, message: str, job_id: str | None = None):
        super().__init__(message, endpoint="/training/jobs")
        self.job_id = job_id


class KonicDataNotFoundError(KonicAPIClientError):
    """Dataset not found (404)."""

    def __init__(self, data_identifier: str):
        message = f"Dataset not found: {data_identifier}"
        super().__init__(message, endpoint="/data")
        self.data_identifier = data_identifier


class KonicDataConflictError(KonicAPIClientError):
    """Dataset version already exists (409)."""

    def __init__(self, data_name: str, version: str):
        message = f"Version '{version}' already exists for dataset '{data_name}'."
        super().__init__(message, endpoint="/data/upload")
        self.data_name = data_name
        self.version = version


class KonicDataValidationError(KonicAPIClientError):
    """Data validation failure."""

    def __init__(self, message: str, field: str | None = None):
        super().__init__(message, endpoint="/data")
        self.field = field


class KonicArtifactNotFoundError(KonicAPIClientError):
    """Artifact not found (404)."""

    def __init__(self, artifact_id: str):
        message = f"Artifact not found: {artifact_id}"
        super().__init__(message, endpoint="/artifacts")
        self.artifact_id = artifact_id


class KonicInferenceServerNotFoundError(KonicAPIClientError):
    """Inference server not found (404)."""

    def __init__(self, server_id: str):
        message = f"Inference server not found: {server_id}"
        super().__init__(message, endpoint="/inference")
        self.server_id = server_id


class KonicModelNotFoundError(KonicAPIClientError):
    """Model not found (404)."""

    def __init__(self, hf_model_id: str, context: str = "registry"):
        if context == "huggingface":
            message = f"Model not found on HuggingFace Hub: {hf_model_id}"
        else:
            message = f"Model not found in registry: {hf_model_id}"
        super().__init__(message, endpoint="/models")
        self.hf_model_id = hf_model_id
        self.context = context


class KonicModelConflictError(KonicAPIClientError):
    """Model already exists (409)."""

    def __init__(self, hf_model_id: str):
        message = f"Model '{hf_model_id}' is already downloaded."
        super().__init__(message, endpoint="/models/download")
        self.hf_model_id = hf_model_id


class KonicModelGatedError(KonicAPIClientError):
    """Gated model access denied (403)."""

    def __init__(self, hf_model_id: str):
        message = f"Model '{hf_model_id}' is gated. Only public models are supported."
        super().__init__(message, endpoint="/models/download")
        self.hf_model_id = hf_model_id
