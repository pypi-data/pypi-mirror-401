from .client import (
    BatchInferenceClient,
    Message,
    ActivationsRequest,
    ChatCompletionRequest,
    ActivationsResponse,
    ChatCompletionResponse,
)


def hello() -> str:
    return "Hello from jsinfer!"


__all__ = [
    "BatchInferenceClient",
    "Message",
    "ActivationsRequest",
    "ChatCompletionRequest",
    "ActivationsResponse",
    "ChatCompletionResponse",
    "hello",
]
