from __future__ import annotations

from .base import ModelResponse


class MockProvider:
    provider_name = "mock"
    model_name = "deterministic-placeholder"

    def generate(self, prompt: str) -> ModelResponse:
        return ModelResponse(
            text="Mock provider response. No external model was called.",
            provider=self.provider_name,
            model=self.model_name,
            input_tokens=len(prompt.split()),
            output_tokens=8,
        )
