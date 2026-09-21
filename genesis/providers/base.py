from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True, slots=True)
class ModelResponse:
    text: str
    provider: str
    model: str
    input_tokens: int = 0
    output_tokens: int = 0


class ModelProvider(Protocol):
    provider_name: str
    model_name: str

    def generate(self, prompt: str) -> ModelResponse:
        ...
