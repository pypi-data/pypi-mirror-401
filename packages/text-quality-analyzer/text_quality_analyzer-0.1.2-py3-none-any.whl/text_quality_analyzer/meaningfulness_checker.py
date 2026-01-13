"""
Meaningfulness checker - determines if text is meaningful or random
"""
from typing import Dict, List
import logging
from .utils import normalize, safe_divide, get_character_distribution

logger = logging.getLogger(__name__)


class MeaningfulnessChecker:
    """
    Check if text is meaningful (coherent writing) or random characters.

    Uses multiple metrics:
    - Letter ratio (proportion of alphabetic characters)
    - Space ratio (appropriate spacing between words)
    - Stopword presence (common words for the language)
    - Average word length (reasonable word sizes)
    - Dictionary match (words found in frequency lists)
    """

    # Common stopwords for supported languages
    STOPWORDS = {
        "en": [
            "the",
            "is",
            "at",
            "which",
            "on",
            "a",
            "an",
            "and",
            "or",
            "but",
            "in",
            "with",
            "to",
            "for",
            "of",
            "as",
            "by",
            "that",
            "this",
            "from",
            "be",
            "are",
            "was",
            "were",
            "been",
            "have",
            "has",
            "had",
            "do",
            "does",
            "did",
        ],
        "ru": [
            "и",
            "в",
            "не",
            "на",
            "я",
            "что",
            "он",
            "с",
            "это",
            "как",
            "а",
            "по",
            "но",
            "они",
            "к",
            "у",
            "его",
            "из",
            "за",
            "для",
            "от",
            "о",
            "мы",
            "же",
            "все",
            "так",
            "вы",
            "при",
            "еще",
            "уже",
        ],
        "zh": ["的", "是", "在", "了", "和", "有", "人", "我", "中", "大", "为", "上", "个", "国", "来", "要"],
        "es": [
            "el",
            "la",
            "de",
            "que",
            "y",
            "a",
            "en",
            "un",
            "ser",
            "se",
            "no",
            "haber",
            "por",
            "con",
            "para",
        ],
        "fr": [
            "le",
            "de",
            "un",
            "être",
            "et",
            "à",
            "il",
            "avoir",
            "ne",
            "je",
            "son",
            "que",
            "se",
            "qui",
            "ce",
        ],
        "de": [
            "der",
            "die",
            "und",
            "in",
            "den",
            "von",
            "zu",
            "das",
            "mit",
            "sich",
            "des",
            "auf",
            "für",
            "ist",
            "im",
        ],
    }

    def __init__(self, language: str = "en", min_score: float = 0.6):
        """
        Initialize meaningfulness checker.

        Args:
            language: Language code for stopword checking (default: "en")
            min_score: Minimum score to consider text meaningful (0.0-1.0)
        """
        self.language = language
        self.min_score = min_score
        self.stopwords = set(self.STOPWORDS.get(language, self.STOPWORDS["en"]))

        # Try to load wordfreq for dictionary matching
        try:
            from wordfreq import word_frequency

            self.word_frequency = word_frequency
            self.has_wordfreq = True
            logger.debug(f"MeaningfulnessChecker initialized with wordfreq for {language}")
        except ImportError:
            self.word_frequency = None
            self.has_wordfreq = False
            logger.warning("wordfreq not available, dictionary matching disabled")

    def check(self, text: str) -> Dict[str, any]:
        """
        Check if text is meaningful.

        Args:
            text: Text to analyze

        Returns:
            Dictionary with:
                - is_meaningful: Boolean result
                - score: Overall meaningfulness score (0.0-1.0)
                - metrics: Individual metric scores

        Examples:
            >>> checker = MeaningfulnessChecker(language="en")
            >>> result = checker.check("This is a normal sentence.")
            >>> result["is_meaningful"]
            True
            >>> result = checker.check("xkcd1234!@#$")
            >>> result["is_meaningful"]
            False
        """
        if not text or not text.strip():
            return {
                "is_meaningful": False,
                "score": 0.0,
                "metrics": {},
                "error": "Empty text",
            }

        # Calculate all metrics
        metrics = {}

        # 1. Character distribution
        char_dist = get_character_distribution(text)
        metrics["letter_ratio"] = char_dist["letter_ratio"]
        metrics["space_ratio"] = char_dist["space_ratio"]
        metrics["digit_ratio"] = char_dist["digit_ratio"]

        # 2. Stopword presence
        stopword_score = self._check_stopwords(text)
        metrics["stopword_presence"] = stopword_score

        # 3. Average word length
        avg_word_len, word_len_score = self._check_word_lengths(text)
        metrics["avg_word_length"] = avg_word_len
        metrics["word_length_score"] = word_len_score

        # 4. Dictionary match (if available)
        dict_match = self._check_dictionary_match(text)
        metrics["dictionary_match"] = dict_match

        # Calculate overall meaningfulness score
        score = self._calculate_meaningfulness_score(metrics)

        return {
            "is_meaningful": score >= self.min_score,
            "score": score,
            "metrics": metrics,
        }

    def _check_stopwords(self, text: str) -> float:
        """
        Check presence of stopwords in text.

        Args:
            text: Text to check

        Returns:
            Score 0.0-1.0 based on stopword presence
        """
        words = text.lower().split()
        if not words:
            return 0.0

        stopword_count = sum(1 for word in words if word.strip(".,!?;:\"'-()[]{}") in self.stopwords)

        # Expect at least 10-30% stopwords in natural text
        stopword_ratio = safe_divide(stopword_count, len(words))
        return normalize(stopword_ratio, 0.05, 0.35)

    def _check_word_lengths(self, text: str) -> tuple:
        """
        Check average word length.

        Args:
            text: Text to check

        Returns:
            Tuple of (average_length, normalized_score)
        """
        words = text.split()
        if not words:
            return 0.0, 0.0

        # Filter out very short and very long "words" (likely garbage)
        meaningful_words = [w for w in words if 1 < len(w) < 25]
        if not meaningful_words:
            return 0.0, 0.0

        avg_len = sum(len(w) for w in meaningful_words) / len(meaningful_words)

        # Normal word length: 3-12 characters
        # Score is highest around 5-7 characters
        if avg_len < 3:
            score = avg_len / 3
        elif avg_len <= 7:
            score = 1.0
        elif avg_len <= 12:
            score = 1.0 - (avg_len - 7) / 10
        else:
            score = max(0.0, 1.0 - (avg_len - 12) / 10)

        return avg_len, score

    def _check_dictionary_match(self, text: str) -> float:
        """
        Check how many words exist in language frequency dictionary.

        Args:
            text: Text to check

        Returns:
            Score 0.0-1.0 based on dictionary match ratio
        """
        if not self.has_wordfreq:
            # If wordfreq not available, return neutral score
            return 0.5

        words = text.lower().split()
        if not words:
            return 0.0

        # Check each word against frequency dictionary
        # Words with frequency > 0 are considered "real words"
        matched_words = 0
        for word in words:
            word_clean = word.strip(".,!?;:\"'-()[]{}").lower()
            if len(word_clean) > 1:  # Skip single characters
                try:
                    freq = self.word_frequency(word_clean, self.language)
                    if freq > 0:
                        matched_words += 1
                except:
                    pass

        match_ratio = safe_divide(matched_words, len(words))
        return match_ratio

    def _calculate_meaningfulness_score(self, metrics: Dict) -> float:
        """
        Calculate overall meaningfulness score from individual metrics.

        Weighted formula:
        - 30% letter ratio (text should be mostly letters)
        - 20% space ratio (proper spacing)
        - 20% stopword presence
        - 15% word length normality
        - 15% dictionary match (if available)

        Args:
            metrics: Dictionary of individual metric scores

        Returns:
            Overall score 0.0-1.0
        """
        # Normalize letter ratio (expect 0.5-0.9)
        letter_score = normalize(metrics.get("letter_ratio", 0), 0.5, 0.9)

        # Normalize space ratio (expect 0.05-0.25)
        space_score = normalize(metrics.get("space_ratio", 0), 0.05, 0.25)

        # Stopword presence score (already normalized)
        stopword_score = metrics.get("stopword_presence", 0)

        # Word length score (already normalized)
        word_len_score = metrics.get("word_length_score", 0)

        # Dictionary match score (already normalized)
        dict_score = metrics.get("dictionary_match", 0.5)

        # Weighted average
        score = (
            0.30 * letter_score
            + 0.20 * space_score
            + 0.20 * stopword_score
            + 0.15 * word_len_score
            + 0.15 * dict_score
        )

        return min(1.0, max(0.0, score))

    def set_language(self, language: str) -> None:
        """
        Change the language for stopword checking.

        Args:
            language: New language code (e.g., "en", "ru", "zh")
        """
        self.language = language
        self.stopwords = set(self.STOPWORDS.get(language, self.STOPWORDS["en"]))
        logger.debug(f"Language set to {language}")
