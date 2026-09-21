"""Provider interfaces and implementations."""

from .base import ModelProvider, ModelResponse
from .huggingface_local import HuggingFaceLocalProvider
from .mock import MockProvider
from .model_onboarding import CATALOG, ModelProfile, TeacherSelection, load_teacher, normalize_source, recommended_models, select_teacher
from .huggingface_api import search_public_models

__all__ = ["CATALOG", "HuggingFaceLocalProvider", "ModelProfile", "ModelProvider", "ModelResponse", "MockProvider", "TeacherSelection", "load_teacher", "normalize_source", "recommended_models", "search_public_models", "select_teacher"]
