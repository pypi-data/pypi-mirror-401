"""
Language detection module using langid
"""
from typing import Dict, Optional
import logging

logger = logging.getLogger(__name__)


class LanguageDetector:
    """
    Detect language of text using langid library.

    Supports 97+ languages with ISO 639-1 codes.
    Falls back to 'unknown' if detection fails or confidence is too low.
    """

    def __init__(self, min_confidence: float = 0.7, min_text_length: int = 10):
        """
        Initialize language detector.

        Args:
            min_confidence: Minimum confidence threshold (0.0-1.0)
            min_text_length: Minimum text length required for detection
        """
        self.min_confidence = min_confidence
        self.min_text_length = min_text_length

        # Try to import langid
        try:
            import langid

            self.langid = langid
            self.langid.set_languages(
                ["en", "ru", "zh", "es", "fr", "de", "ar", "ja", "pt", "it", "ko", "hi"]
            )
            self.method = "langid"
            logger.debug("LanguageDetector initialized with langid")
        except ImportError:
            logger.warning("langid not available, language detection will be limited")
            self.langid = None
            self.method = "fallback"

    def detect(self, text: str) -> Dict[str, any]:
        """
        Detect language of text.

        Args:
            text: Text to analyze (string)

        Returns:
            Dictionary with:
                - language: ISO 639-1 language code (e.g., "en", "ru", "zh")
                - confidence: Confidence score 0.0-1.0
                - method: Detection method used ("langid" or "fallback")

        Examples:
            >>> detector = LanguageDetector()
            >>> result = detector.detect("Hello world")
            >>> result["language"]
            'en'
            >>> result["confidence"] > 0.9
            True
        """
        # Validate input
        if not text or not text.strip():
            return {
                "language": "unknown",
                "confidence": 0.0,
                "method": self.method,
                "error": "Empty text",
            }

        if len(text) < self.min_text_length:
            return {
                "language": "unknown",
                "confidence": 0.0,
                "method": self.method,
                "error": f"Text too short (min {self.min_text_length} chars)",
            }

        # Try langid detection
        if self.langid:
            try:
                lang, raw_confidence = self.langid.classify(text)

                # langid returns negative log-likelihood, convert to probability
                # More negative = less confident, closer to 0 = more confident
                # We'll normalize to 0-1 range where 1 = most confident
                # Typical range is -200 (uncertain) to 0 (very confident)
                import math
                confidence = 1.0 / (1.0 + math.exp(raw_confidence / 10.0))

                # Check confidence threshold
                if confidence < self.min_confidence:
                    logger.debug(
                        f"Low confidence detection: {lang} ({confidence:.2f})"
                    )
                    return {
                        "language": lang,
                        "confidence": confidence,
                        "method": self.method,
                        "warning": "Low confidence",
                    }

                return {
                    "language": lang,
                    "confidence": confidence,
                    "method": self.method,
                }

            except Exception as e:
                logger.error(f"Error in langid detection: {e}")
                return {
                    "language": "unknown",
                    "confidence": 0.0,
                    "method": self.method,
                    "error": str(e),
                }

        # Fallback: simple heuristic-based detection
        return self._fallback_detect(text)

    def _fallback_detect(self, text: str) -> Dict[str, any]:
        """
        Simple fallback language detection based on character sets.

        Args:
            text: Text to analyze

        Returns:
            Detection result dictionary
        """
        # Count characters from different scripts
        cyrillic = sum(1 for c in text if "\u0400" <= c <= "\u04FF")
        chinese = sum(1 for c in text if "\u4E00" <= c <= "\u9FFF")
        arabic = sum(1 for c in text if "\u0600" <= c <= "\u06FF")
        latin = sum(1 for c in text if c.isalpha() and c.isascii())

        total_chars = len([c for c in text if c.isalpha()])
        if total_chars == 0:
            return {
                "language": "unknown",
                "confidence": 0.0,
                "method": "fallback",
                "error": "No alphabetic characters",
            }

        # Determine dominant script
        ratios = {
            "ru": cyrillic / total_chars if total_chars > 0 else 0,
            "zh": chinese / total_chars if total_chars > 0 else 0,
            "ar": arabic / total_chars if total_chars > 0 else 0,
            "en": latin / total_chars if total_chars > 0 else 0,
        }

        dominant_lang = max(ratios, key=ratios.get)
        confidence = ratios[dominant_lang]

        if confidence < 0.5:
            return {
                "language": "unknown",
                "confidence": confidence,
                "method": "fallback",
                "warning": "No dominant script detected",
            }

        return {
            "language": dominant_lang,
            "confidence": confidence,
            "method": "fallback",
            "warning": "Fallback detection (install langid for better accuracy)",
        }

    def get_language_name(self, lang_code: str) -> str:
        """
        Get full language name from ISO code.

        Args:
            lang_code: ISO 639-1 code (e.g., "en")

        Returns:
            Full language name (e.g., "English")

        Examples:
            >>> detector = LanguageDetector()
            >>> detector.get_language_name("en")
            'English'
            >>> detector.get_language_name("ru")
            'Russian'
        """
        language_names = {
            "en": "English",
            "ru": "Russian",
            "zh": "Chinese",
            "es": "Spanish",
            "fr": "French",
            "de": "German",
            "ar": "Arabic",
            "ja": "Japanese",
            "pt": "Portuguese",
            "it": "Italian",
            "ko": "Korean",
            "hi": "Hindi",
            "unknown": "Unknown",
        }
        return language_names.get(lang_code, f"Language({lang_code})")
