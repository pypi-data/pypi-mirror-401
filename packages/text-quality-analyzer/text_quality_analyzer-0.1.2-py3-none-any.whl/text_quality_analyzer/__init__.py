"""
Text Quality Analyzer - Universal text analysis module

Detect language, meaningfulness, and structure of text documents.
Perfect for filtering, classifying, and preprocessing text in NLP pipelines.

Usage:
    >>> from text_quality_analyzer import TextProfiler
    >>> profiler = TextProfiler()
    >>> result = profiler.analyze_text("Your text here")
    >>> print(result["language"], result["is_meaningful"], result["is_structured"])

Quick usage:
    >>> from text_quality_analyzer import analyze_text
    >>> result = analyze_text("Your text here")
"""

__version__ = "0.1.1"
__author__ = "Text Quality Analyzer Team"
__license__ = "MIT"

# Import main classes
from .text_profile import TextProfiler, analyze_text
from .language_detector import LanguageDetector
from .meaningfulness_checker import MeaningfulnessChecker
from .structure_analyzer import StructureAnalyzer

# Public API
__all__ = [
    # Main API
    "TextProfiler",
    "analyze_text",
    # Individual components
    "LanguageDetector",
    "MeaningfulnessChecker",
    "StructureAnalyzer",
    # Metadata
    "__version__",
]


# Configure logging
import logging

logging.getLogger(__name__).addHandler(logging.NullHandler())
