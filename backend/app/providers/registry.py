from dataclasses import dataclass

@dataclass
class ProviderCapabilities:
    supports_json_mode: bool
    supports_tools: bool
    supports_vision: bool
    max_context_window: int
    max_request_size_mb: int

PROVIDER_REGISTRY = {
    "groq": ProviderCapabilities(
        supports_json_mode=True,
        supports_tools=True,
        supports_vision=False,
        max_context_window=8192,
        max_request_size_mb=25
    ),
    "openrouter": ProviderCapabilities(
        supports_json_mode=False, # Explicitly false to avoid disparate model 400s
        supports_tools=False,
        supports_vision=False,
        max_context_window=8192,
        max_request_size_mb=10
    ),
    "gemini": ProviderCapabilities(
        supports_json_mode=True,
        supports_tools=True,
        supports_vision=True,
        max_context_window=2000000,
        max_request_size_mb=50
    ),
    "ollama": ProviderCapabilities(
        supports_json_mode=True,
        supports_tools=False,
        supports_vision=False,
        max_context_window=8192,
        max_request_size_mb=10
    ),
    "mock": ProviderCapabilities(
        supports_json_mode=True,
        supports_tools=True,
        supports_vision=True,
        max_context_window=100000,
        max_request_size_mb=10
    )
}
