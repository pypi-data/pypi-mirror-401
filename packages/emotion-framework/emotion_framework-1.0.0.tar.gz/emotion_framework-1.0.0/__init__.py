"""
Emotion Analysis Framework

A reusable framework for multimodal emotion recognition from video files.
This framework can be used by both API services and UI applications.
"""

__version__ = "1.0.0"
__author__ = "Emotion Analysis Team"

from .core.pipeline import EmotionAnalysisPipeline
from .models.result_models import EmotionAnalysisResult

__all__ = [
    "EmotionAnalysisPipeline",
    "EmotionAnalysisResult",
]

