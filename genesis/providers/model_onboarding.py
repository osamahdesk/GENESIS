from __future__ import annotations

import json
import os
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from urllib.parse import urlparse


@dataclass(frozen=True, slots=True)
class ModelProfile:
    repo_id: str
    label: str
    task: str
    min_ram_gb: float
    approximate_parameters: str
    source_url: str


CATALOG = (
    ModelProfile("sshleifer/tiny-gpt2", "Tiny GPT-2", "text-generation", 1.0, "2.1M", "https://huggingface.co/sshleifer/tiny-gpt2"),
    ModelProfile("HuggingFaceTB/SmolLM-135M", "SmolLM 135M", "text-generation", 4.0, "134.5M", "https://huggingface.co/HuggingFaceTB/SmolLM-135M"),
    ModelProfile("distilbert/distilgpt2", "DistilGPT2", "text-generation", 4.0, "88.2M", "https://huggingface.co/distilbert/distilgpt2"),
)


@dataclass(frozen=True, slots=True)
class TeacherSelection:
    source: str
    source_type: str
    resolved_id: str
    label: str
    status: str = "selected"

    def as_dict(self) -> dict[str, str]:
        return asdict(self)


def available_memory_gb() -> float:
    pages = os.sysconf("SC_PHYS_PAGES")
    page_size = os.sysconf("SC_PAGE_SIZE")
    return round((pages * page_size) / (1024**3), 1)


def recommended_models(memory_gb: float | None = None) -> list[ModelProfile]:
    available = memory_gb if memory_gb is not None else available_memory_gb()
    return [profile for profile in CATALOG if profile.min_ram_gb <= available]


def normalize_source(source: str) -> tuple[str, str]:
    value = source.strip()
    if not value:
        raise ValueError("Enter a Hugging Face model name, URL, or local model directory")
    path = Path(value).expanduser()
    if path.exists() and path.is_dir():
        return "local", str(path.resolve())
    if value.startswith("hf://models/"):
        return "huggingface", value.removeprefix("hf://models/").strip("/")
    parsed = urlparse(value)
    if parsed.scheme in {"http", "https"} and parsed.netloc.endswith("huggingface.co"):
        parts = [part for part in parsed.path.split("/") if part]
        if len(parts) >= 2:
            return "huggingface", "/".join(parts[:2])
        raise ValueError("The Hugging Face URL must include an owner and model name")
    if re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", value):
        return "huggingface", value
    raise ValueError("Use owner/model, a huggingface.co URL, or an existing local directory")


def select_teacher(source: str, root: str | Path) -> TeacherSelection:
    source_type, resolved = normalize_source(source)
    profile = next((item for item in CATALOG if item.repo_id == resolved), None)
    label = profile.label if profile else resolved
    selection = TeacherSelection(source, source_type, resolved, label)
    path = Path(root) / "teacher.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(selection.as_dict(), indent=2) + "\n", encoding="utf-8")
    return selection


def load_teacher(root: str | Path) -> TeacherSelection | None:
    path = Path(root) / "teacher.json"
    if not path.exists():
        return None
    return TeacherSelection(**json.loads(path.read_text(encoding="utf-8")))
