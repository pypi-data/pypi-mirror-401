"""
Structure analyzer - detects document structure and formatting
"""
import re
from typing import Dict
import logging
from .utils import normalize, safe_divide, count_words, count_sentences

logger = logging.getLogger(__name__)


class StructureAnalyzer:
    """
    Analyze text structure and formatting.

    Detects:
    - Markdown headers (# ##, etc.)
    - Lists (ordered and unordered)
    - Paragraphs (separated by blank lines)
    - Links and URLs
    - Code blocks (inline and multiline)
    - Readability metrics
    """

    def __init__(self, min_structure_score: float = 0.5):
        """
        Initialize structure analyzer.

        Args:
            min_structure_score: Minimum score to consider text structured
        """
        self.min_structure_score = min_structure_score

        # Try to load textstat for readability
        try:
            import textstat

            self.textstat = textstat
            self.has_textstat = True
            logger.debug("StructureAnalyzer initialized with textstat")
        except ImportError:
            self.textstat = None
            self.has_textstat = False
            logger.warning("textstat not available, readability analysis disabled")

        # Compile regex patterns
        self.header_pattern = re.compile(r"^#{1,6}\s+.+$", re.MULTILINE)
        self.unordered_list_pattern = re.compile(r"^\s*[-*+]\s+.+$", re.MULTILINE)
        self.ordered_list_pattern = re.compile(r"^\s*\d+\.\s+.+$", re.MULTILINE)
        self.link_pattern = re.compile(r"\[.+?\]\(.+?\)")
        self.url_pattern = re.compile(r"https?://\S+")
        self.code_block_pattern = re.compile(r"```[\s\S]*?```")
        self.inline_code_pattern = re.compile(r"`[^`]+`")

    def analyze(self, text: str) -> Dict[str, any]:
        """
        Analyze text structure.

        Args:
            text: Text to analyze

        Returns:
            Dictionary with:
                - is_structured: Boolean result
                - score: Overall structure score (0.0-1.0)
                - elements: Count of structural elements
                - readability_index: Flesch reading ease (if available)

        Examples:
            >>> analyzer = StructureAnalyzer()
            >>> text = "## Header\\n\\nParagraph 1\\n\\n- List item\\n- Another item"
            >>> result = analyzer.analyze(text)
            >>> result["is_structured"]
            True
            >>> result["elements"]["headers"] > 0
            True
        """
        if not text or not text.strip():
            return {
                "is_structured": False,
                "score": 0.0,
                "elements": {},
                "error": "Empty text",
            }

        # Count structural elements
        elements = {}

        # 1. Headers
        headers = self.header_pattern.findall(text)
        elements["headers"] = len(headers)

        # 2. Lists
        unordered_items = self.unordered_list_pattern.findall(text)
        ordered_items = self.ordered_list_pattern.findall(text)
        elements["unordered_lists"] = len(unordered_items)
        elements["ordered_lists"] = len(ordered_items)
        elements["total_list_items"] = len(unordered_items) + len(ordered_items)

        # 3. Paragraphs (separated by blank lines)
        paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
        elements["paragraphs"] = len(paragraphs)

        # 4. Links
        markdown_links = self.link_pattern.findall(text)
        urls = self.url_pattern.findall(text)
        elements["markdown_links"] = len(markdown_links)
        elements["urls"] = len(urls)
        elements["total_links"] = len(markdown_links) + len(urls)

        # 5. Code blocks
        code_blocks = self.code_block_pattern.findall(text)
        inline_code = self.inline_code_pattern.findall(text)
        elements["code_blocks"] = len(code_blocks)
        elements["inline_code"] = len(inline_code)

        # 6. Basic text stats
        elements["word_count"] = count_words(text)
        elements["sentence_count"] = count_sentences(text)

        # 7. Readability (if textstat available)
        readability = self._calculate_readability(text)
        if readability is not None:
            elements["readability_index"] = readability

        # Calculate structure score
        score = self._calculate_structure_score(elements, text)

        return {
            "is_structured": score >= self.min_structure_score,
            "score": score,
            "elements": elements,
        }

    def _calculate_readability(self, text: str) -> float:
        """
        Calculate Flesch reading ease score.

        Args:
            text: Text to analyze

        Returns:
            Readability index (0-100) or None if not available
        """
        if not self.has_textstat:
            return None

        try:
            # Flesch Reading Ease: higher = easier to read
            # 90-100: Very easy
            # 60-70: Standard
            # 0-30: Very difficult
            score = self.textstat.flesch_reading_ease(text)
            return round(score, 2)
        except Exception as e:
            logger.warning(f"Error calculating readability: {e}")
            return None

    def _calculate_structure_score(self, elements: Dict, text: str) -> float:
        """
        Calculate overall structure score.

        Strategy:
        1. Check for explicit structural elements (headers, lists, code)
        2. If present, boost score significantly
        3. Otherwise, evaluate paragraphs and readability

        Args:
            elements: Dictionary of structural elements
            text: Original text

        Returns:
            Structure score 0.0-1.0
        """
        # Count explicit structural elements
        headers = elements.get("headers", 0)
        lists = elements.get("total_list_items", 0)
        code_blocks = elements.get("code_blocks", 0)
        links = elements.get("total_links", 0)
        paragraphs = elements.get("paragraphs", 0)

        # Strong indicators of structure
        has_headers = headers >= 1
        has_lists = lists >= 2
        has_code = code_blocks >= 1
        has_links = links >= 1
        has_multiple_paragraphs = paragraphs >= 3

        # Count strong structure indicators
        structure_indicators = sum([
            has_headers,
            has_lists,
            has_code,
            has_links and has_multiple_paragraphs,  # Links + paragraphs together
        ])

        # If we have 2+ strong indicators, it's definitely structured
        if structure_indicators >= 2:
            base_score = 0.7
        elif structure_indicators == 1:
            base_score = 0.5
        else:
            base_score = 0.0

        # Add bonuses for quantity
        # Normalize header count (more headers = better)
        header_bonus = min(0.15, headers * 0.05)  # +0.05 per header, max 0.15

        # Normalize list items
        list_bonus = min(0.15, lists * 0.02)  # +0.02 per item, max 0.15

        # Code blocks bonus
        code_bonus = 0.1 if code_blocks > 0 else 0.0

        # Calculate final score
        final_score = base_score + header_bonus + list_bonus + code_bonus

        # Cap at 1.0
        return min(1.0, max(0.0, final_score))

    def get_structure_summary(self, text: str) -> str:
        """
        Get human-readable structure summary.

        Args:
            text: Text to analyze

        Returns:
            Summary string describing the structure

        Examples:
            >>> analyzer = StructureAnalyzer()
            >>> text = "## Header\\n\\nText\\n\\n- Item"
            >>> summary = analyzer.get_structure_summary(text)
            >>> "1 header" in summary
            True
        """
        result = self.analyze(text)
        if "error" in result:
            return "Empty or invalid text"

        elements = result["elements"]
        parts = []

        if elements.get("headers", 0) > 0:
            parts.append(f"{elements['headers']} header(s)")

        if elements.get("total_list_items", 0) > 0:
            parts.append(f"{elements['total_list_items']} list item(s)")

        if elements.get("paragraphs", 0) > 0:
            parts.append(f"{elements['paragraphs']} paragraph(s)")

        if elements.get("total_links", 0) > 0:
            parts.append(f"{elements['total_links']} link(s)")

        if elements.get("code_blocks", 0) > 0:
            parts.append(f"{elements['code_blocks']} code block(s)")

        if not parts:
            return "Plain text without structure"

        summary = "Structure: " + ", ".join(parts)

        if result.get("is_structured"):
            summary += " (well-structured)"
        else:
            summary += " (minimal structure)"

        return summary
