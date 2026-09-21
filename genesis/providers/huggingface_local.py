from __future__ import annotations

from pathlib import Path

from .base import ModelResponse


class HuggingFaceLocalProvider:
    """Local Hugging Face text-generation provider.

    Dependencies are imported lazily so the offline core remains lightweight.
    The model directory can be a checked-in model or a downloaded Hub snapshot.
    """

    provider_name = "huggingface-local"

    def __init__(self, model_path: str | Path):
        self.model_path = str(model_path)
        self.model_name = Path(model_path).name
        self._tokenizer = None
        self._model = None

    def _load(self) -> None:
        try:
            from transformers import AutoModelForCausalLM, AutoTokenizer
        except ImportError as error:  # pragma: no cover - depends on optional extra
            raise RuntimeError(
                "Install the optional Hugging Face provider: pip install -e '.[hf]'"
            ) from error
        self._tokenizer = AutoTokenizer.from_pretrained(self.model_path, local_files_only=True)
        self._model = AutoModelForCausalLM.from_pretrained(self.model_path, local_files_only=True)

    def generate(self, prompt: str, max_new_tokens: int = 32) -> ModelResponse:
        if self._model is None or self._tokenizer is None:
            self._load()
        inputs = self._tokenizer(prompt, return_tensors="pt")
        outputs = self._model.generate(**inputs, max_new_tokens=max_new_tokens, do_sample=False)
        text = self._tokenizer.decode(outputs[0], skip_special_tokens=True)
        return ModelResponse(
            text=text,
            provider=self.provider_name,
            model=self.model_name,
            input_tokens=int(inputs["input_ids"].shape[-1]),
            output_tokens=int(outputs.shape[-1] - inputs["input_ids"].shape[-1]),
        )
