"""
Main text profiler API - combines all analysis components
"""
import time
import logging
from typing import Dict, Optional
from .language_detector import LanguageDetector
from .meaningfulness_checker import MeaningfulnessChecker
from .structure_analyzer import StructureAnalyzer
from .utils import validate_text_input, count_words

logger = logging.getLogger(__name__)


class TextProfiler:
    """
    Main API for comprehensive text analysis.

    Combines language detection, meaningfulness checking, and structure analysis
    into a single unified interface.

    Examples:
        >>> profiler = TextProfiler()
        >>> result = profiler.analyze_text("## Hello World\\n\\nThis is a test.")
        >>> result["language"]
        'en'
        >>> result["is_meaningful"]
        True
        >>> result["is_structured"]
        True
    """

    def __init__(
        self,
        min_confidence: float = 0.7,
        min_meaningfulness: float = 0.6,
        min_structure: float = 0.5,
        max_text_length: int = 1_000_000,
    ):
        """
        Initialize text profiler with all components.

        Args:
            min_confidence: Minimum confidence for language detection
            min_meaningfulness: Minimum score for meaningfulness check
            min_structure: Minimum score for structure check
            max_text_length: Maximum allowed text length in characters
        """
        self.max_text_length = max_text_length

        # Initialize components
        self.language_detector = LanguageDetector(min_confidence=min_confidence)
        self.structure_analyzer = StructureAnalyzer(min_structure_score=min_structure)

        # Meaningfulness checker will be created after language detection
        self.meaningfulness_checker = None
        self.min_meaningfulness = min_meaningfulness

        logger.info("TextProfiler initialized")

    def analyze_text(self, text: str, detect_language: bool = True) -> Dict[str, any]:
        """
        Perform complete text analysis.

        Args:
            text: Text to analyze (string, up to max_text_length)
            detect_language: Whether to perform language detection (default: True)

        Returns:
            Dictionary with complete analysis results:
            {
                "language": "en",
                "language_confidence": 0.98,
                "is_meaningful": True,
                "meaningfulness_score": 0.87,
                "is_structured": True,
                "structure_score": 0.76,
                "text_length": 1024,
                "word_count": 145,
                "paragraph_count": 7,
                "readability_index": 58.4,
                "processing_time_ms": 125
            }

        Examples:
            >>> profiler = TextProfiler()
            >>> result = profiler.analyze_text("Hello world! This is a test.")
            >>> result["language"]
            'en'
            >>> result["is_meaningful"]
            True
        """
        start_time = time.time()

        # Validate input
        is_valid, error_msg = validate_text_input(text, self.max_text_length)
        if not is_valid:
            return {
                "success": False,
                "error": error_msg,
                "processing_time_ms": int((time.time() - start_time) * 1000),
            }

        result = {"success": True}

        # 1. Language Detection
        if detect_language:
            lang_result = self.language_detector.detect(text)
            result["language"] = lang_result["language"]
            result["language_confidence"] = lang_result["confidence"]
            result["language_method"] = lang_result["method"]

            if "warning" in lang_result:
                result["language_warning"] = lang_result["warning"]
            if "error" in lang_result:
                result["language_error"] = lang_result["error"]

            detected_language = lang_result["language"]
        else:
            detected_language = "en"  # Default
            result["language"] = "en"
            result["language_confidence"] = None

        # 2. Meaningfulness Check
        # Create checker with detected language
        self.meaningfulness_checker = MeaningfulnessChecker(
            language=detected_language, min_score=self.min_meaningfulness
        )
        meaning_result = self.meaningfulness_checker.check(text)

        result["is_meaningful"] = meaning_result.get("is_meaningful", False)
        result["meaningfulness_score"] = meaning_result.get("score", 0.0)
        result["meaningfulness_metrics"] = meaning_result.get("metrics", {})

        if "error" in meaning_result:
            result["meaningfulness_error"] = meaning_result["error"]

        # 3. Structure Analysis
        struct_result = self.structure_analyzer.analyze(text)

        result["is_structured"] = struct_result.get("is_structured", False)
        result["structure_score"] = struct_result.get("score", 0.0)
        result["structure_elements"] = struct_result.get("elements", {})

        if "error" in struct_result:
            result["structure_error"] = struct_result["error"]

        # 4. Basic Statistics
        result["text_length"] = len(text)
        result["word_count"] = count_words(text)
        result["paragraph_count"] = struct_result.get("elements", {}).get("paragraphs", 0)

        # Include readability if available
        readability = struct_result.get("elements", {}).get("readability_index")
        if readability is not None:
            result["readability_index"] = readability

        # Processing time
        result["processing_time_ms"] = int((time.time() - start_time) * 1000)

        return result

    def quick_check(self, text: str) -> Dict[str, bool]:
        """
        Quick boolean checks without detailed metrics.

        Args:
            text: Text to check

        Returns:
            Dictionary with boolean results:
            {
                "is_valid": True,
                "is_meaningful": True,
                "is_structured": True,
                "is_english": True
            }

        Examples:
            >>> profiler = TextProfiler()
            >>> checks = profiler.quick_check("Hello world")
            >>> checks["is_valid"]
            True
        """
        # Validate
        is_valid, _ = validate_text_input(text, self.max_text_length)
        if not is_valid:
            return {"is_valid": False}

        result = {"is_valid": True}

        # Language
        lang_result = self.language_detector.detect(text)
        result["is_english"] = lang_result["language"] == "en"
        result["is_russian"] = lang_result["language"] == "ru"
        result["is_chinese"] = lang_result["language"] == "zh"

        # Meaningfulness
        checker = MeaningfulnessChecker(
            language=lang_result["language"], min_score=self.min_meaningfulness
        )
        meaning_result = checker.check(text)
        result["is_meaningful"] = meaning_result.get("is_meaningful", False)

        # Structure
        struct_result = self.structure_analyzer.analyze(text)
        result["is_structured"] = struct_result.get("is_structured", False)

        return result

    def get_text_summary(self, text: str) -> str:
        """
        Get human-readable summary of text analysis.

        Args:
            text: Text to analyze

        Returns:
            Summary string

        Examples:
            >>> profiler = TextProfiler()
            >>> summary = profiler.get_text_summary("## Hello\\n\\nTest")
            >>> "English" in summary
            True
        """
        result = self.analyze_text(text)

        if not result.get("success"):
            return f"Error: {result.get('error', 'Unknown error')}"

        parts = []

        # Language
        lang = result.get("language", "unknown")
        lang_name = self.language_detector.get_language_name(lang)
        confidence = result.get("language_confidence", 0)
        parts.append(f"Language: {lang_name} ({confidence:.0%} confidence)")

        # Meaningfulness
        if result.get("is_meaningful"):
            score = result.get("meaningfulness_score", 0)
            parts.append(f"Meaningful text (score: {score:.2f})")
        else:
            parts.append("Random or low-quality text")

        # Structure
        if result.get("is_structured"):
            score = result.get("structure_score", 0)
            parts.append(f"Well-structured (score: {score:.2f})")
        else:
            parts.append("Plain text without structure")

        # Stats
        words = result.get("word_count", 0)
        paras = result.get("paragraph_count", 0)
        parts.append(f"{words} words, {paras} paragraphs")

        # Readability
        readability = result.get("readability_index")
        if readability is not None:
            if readability >= 70:
                level = "easy"
            elif readability >= 50:
                level = "moderate"
            else:
                level = "difficult"
            parts.append(f"Readability: {level} ({readability:.1f})")

        return " | ".join(parts)

    def should_process_text(
        self,
        text: str,
        require_meaningful: bool = True,
        require_structured: bool = False,
        allowed_languages: Optional[list] = None,
    ) -> tuple:
        """
        Decision helper: should this text be processed?

        Useful for filtering content in pipelines.

        Args:
            text: Text to check
            require_meaningful: Must be meaningful text (not random)
            require_structured: Must have structure (headers, lists, etc.)
            allowed_languages: List of allowed language codes (None = all)

        Returns:
            Tuple of (should_process: bool, reason: str)

        Examples:
            >>> profiler = TextProfiler()
            >>> should, reason = profiler.should_process_text(
            ...     "Hello world", require_meaningful=True
            ... )
            >>> should
            True
        """
        result = self.analyze_text(text)

        if not result.get("success"):
            return False, f"Invalid text: {result.get('error')}"

        # Check language
        if allowed_languages:
            if result.get("language") not in allowed_languages:
                return False, f"Language {result.get('language')} not in allowed list"

        # Check meaningfulness
        if require_meaningful and not result.get("is_meaningful"):
            score = result.get("meaningfulness_score", 0)
            return False, f"Text not meaningful (score: {score:.2f})"

        # Check structure
        if require_structured and not result.get("is_structured"):
            score = result.get("structure_score", 0)
            return False, f"Text not structured (score: {score:.2f})"

        return True, "Text passes all checks"


# Convenience function for quick analysis
def analyze_text(text: str) -> Dict[str, any]:
    """
    Convenience function for quick text analysis.

    Args:
        text: Text to analyze

    Returns:
        Analysis result dictionary

    Examples:
        >>> from text_quality_analyzer import analyze_text
        >>> result = analyze_text("Hello world")
        >>> result["language"]
        'en'
    """
    profiler = TextProfiler()
    return profiler.analyze_text(text)
