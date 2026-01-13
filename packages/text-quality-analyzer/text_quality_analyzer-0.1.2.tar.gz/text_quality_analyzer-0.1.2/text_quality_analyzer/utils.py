"""
Utility functions for text-quality-analyzer
"""
from typing import Union


def normalize(
    value: float, min_val: float, max_val: float, clamp: bool = True
) -> float:
    """
    Normalize a value to 0-1 range based on min/max boundaries.

    Args:
        value: The value to normalize
        min_val: Minimum boundary (maps to 0.0)
        max_val: Maximum boundary (maps to 1.0)
        clamp: If True, clamp result to [0, 1]

    Returns:
        Normalized value in 0-1 range

    Examples:
        >>> normalize(5, 0, 10)
        0.5
        >>> normalize(15, 0, 10, clamp=True)
        1.0
        >>> normalize(-5, 0, 10, clamp=True)
        0.0
    """
    if max_val == min_val:
        return 1.0 if value >= max_val else 0.0

    normalized = (value - min_val) / (max_val - min_val)

    if clamp:
        return max(0.0, min(1.0, normalized))

    return normalized


def safe_divide(numerator: Union[int, float], denominator: Union[int, float]) -> float:
    """
    Safely divide two numbers, returning 0.0 if denominator is 0.

    Args:
        numerator: The numerator
        denominator: The denominator

    Returns:
        Result of division or 0.0 if denominator is 0

    Examples:
        >>> safe_divide(10, 2)
        5.0
        >>> safe_divide(10, 0)
        0.0
    """
    if denominator == 0:
        return 0.0
    return float(numerator) / float(denominator)


def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """
    Truncate text to maximum length, adding suffix if truncated.

    Args:
        text: Text to truncate
        max_length: Maximum length (including suffix)
        suffix: Suffix to add if truncated

    Returns:
        Truncated text

    Examples:
        >>> truncate_text("Hello world this is a long text", 20)
        'Hello world this ...'
    """
    if len(text) <= max_length:
        return text

    return text[: max_length - len(suffix)] + suffix


def count_words(text: str) -> int:
    """
    Count words in text (simple whitespace-based splitting).

    Args:
        text: Text to count words in

    Returns:
        Number of words

    Examples:
        >>> count_words("Hello world")
        2
        >>> count_words("Hello,  world!  ")
        2
    """
    return len(text.split())


def count_sentences(text: str) -> int:
    """
    Count sentences in text (simple punctuation-based).

    Args:
        text: Text to count sentences in

    Returns:
        Number of sentences (minimum 1 if text is non-empty)

    Examples:
        >>> count_sentences("Hello. World!")
        2
        >>> count_sentences("Hello world")
        1
    """
    if not text.strip():
        return 0

    # Count by sentence-ending punctuation
    count = text.count(".") + text.count("!") + text.count("?")
    return max(1, count)


def get_character_distribution(text: str) -> dict:
    """
    Get distribution of character types in text.

    Args:
        text: Text to analyze

    Returns:
        Dictionary with character type counts and ratios

    Examples:
        >>> dist = get_character_distribution("Hello123!")
        >>> dist["letters"]
        5
        >>> dist["digits"]
        3
    """
    if not text:
        return {
            "letters": 0,
            "digits": 0,
            "spaces": 0,
            "punctuation": 0,
            "other": 0,
            "letter_ratio": 0.0,
            "digit_ratio": 0.0,
            "space_ratio": 0.0,
        }

    letters = sum(c.isalpha() for c in text)
    digits = sum(c.isdigit() for c in text)
    spaces = sum(c.isspace() for c in text)
    punctuation = sum(c in ".,!?;:\"'-()[]{}..." for c in text)
    other = len(text) - letters - digits - spaces - punctuation

    total = len(text)

    return {
        "letters": letters,
        "digits": digits,
        "spaces": spaces,
        "punctuation": punctuation,
        "other": other,
        "letter_ratio": safe_divide(letters, total),
        "digit_ratio": safe_divide(digits, total),
        "space_ratio": safe_divide(spaces, total),
        "punctuation_ratio": safe_divide(punctuation, total),
    }


def validate_text_input(text: str, max_length: int = 1_000_000) -> tuple:
    """
    Validate text input for processing.

    Args:
        text: Text to validate
        max_length: Maximum allowed text length in characters

    Returns:
        Tuple of (is_valid: bool, error_message: str or None)

    Examples:
        >>> validate_text_input("Hello world")
        (True, None)
        >>> validate_text_input("")
        (False, 'Text is empty')
        >>> validate_text_input("a" * 2000000)
        (False, 'Text exceeds maximum length of 1000000 characters')
    """
    if not isinstance(text, str):
        return False, f"Text must be a string, got {type(text).__name__}"

    if not text or not text.strip():
        return False, "Text is empty"

    if len(text) > max_length:
        return False, f"Text exceeds maximum length of {max_length} characters"

    return True, None
