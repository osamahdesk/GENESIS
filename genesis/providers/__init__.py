"""Provider interfaces and implementations."""

from .base import ModelProvider, ModelResponse
from .huggingface_api import search_public_models
from .huggingface_local import HuggingFaceLocalProvider
from .mock import MockProvider
from .model_onboarding import (
    CATALOG,
    ModelProfile,
    TeacherSelection,
    load_teacher,
    normalize_source,
    recommended_models,
    select_teacher,
)

__all__ = ["CATALOG", "HuggingFaceLocalProvider", "MockProvider", "ModelProfile", "ModelProvider", "ModelResponse", "TeacherSelection", "load_teacher", "normalize_source", "recommended_models", "search_public_models", "select_teacher"]
