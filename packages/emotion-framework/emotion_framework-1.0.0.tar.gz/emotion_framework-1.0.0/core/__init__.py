"""Core framework components."""

from .pipeline import EmotionAnalysisPipeline
from .config_loader import load_framework_config

__all__ = [
    "EmotionAnalysisPipeline",
    "load_framework_config",
]

