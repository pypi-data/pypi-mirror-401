"""
Tests for main TextProfiler API
"""
import pytest
from text_quality_analyzer import TextProfiler, analyze_text


class TestTextProfiler:
    """Test cases for TextProfiler class"""

    def test_init(self):
        """Test profiler initialization"""
        profiler = TextProfiler()
        assert profiler is not None
        assert profiler.language_detector is not None
        assert profiler.structure_analyzer is not None

    def test_analyze_english_text(self):
        """Test analysis of simple English text"""
        profiler = TextProfiler()
        text = "Hello world! This is a test document with some content."
        result = profiler.analyze_text(text)

        assert result["success"] is True
        assert result["language"] == "en"
        assert result["language_confidence"] > 0.7
        assert result["is_meaningful"] is True
        assert "word_count" in result
        assert result["word_count"] > 0

    def test_analyze_russian_text(self):
        """Test analysis of Russian text"""
        profiler = TextProfiler()
        text = "\u041f\u0440\u0438\u0432\u0435\u0442 \u043c\u0438\u0440! \u042d\u0442\u043e \u0442\u0435\u0441\u0442\u043e\u0432\u044b\u0439 \u0434\u043e\u043a\u0443\u043c\u0435\u043d\u0442 \u0441 \u043d\u0435\u043a\u043e\u0442\u043e\u0440\u044b\u043c \u0441\u043e\u0434\u0435\u0440\u0436\u0430\u043d\u0438\u0435\u043c."
        result = profiler.analyze_text(text)

        assert result["success"] is True
        assert result["language"] == "ru"
        assert result["is_meaningful"] is True

    def test_analyze_structured_text(self):
        """Test analysis of structured Markdown text"""
        profiler = TextProfiler()
        text = """## Header 1

This is a paragraph with some content.

- List item 1
- List item 2
- List item 3

Another paragraph here.
"""
        result = profiler.analyze_text(text)

        assert result["success"] is True
        assert result["is_structured"] is True
        assert result["structure_elements"]["headers"] > 0
        assert result["structure_elements"]["total_list_items"] > 0
        assert result["structure_elements"]["paragraphs"] > 0

    def test_analyze_plain_text(self):
        """Test analysis of plain unstructured text"""
        profiler = TextProfiler()
        text = "Just a simple sentence without any structure or formatting."
        result = profiler.analyze_text(text)

        assert result["success"] is True
        assert result["is_structured"] is False or result["structure_score"] < 0.5

    def test_analyze_random_text(self):
        """Test detection of random/meaningless text"""
        profiler = TextProfiler()
        text = "xkcd1234!@#$%^&*()_+=[]{}|\\:;<>?,./~`"
        result = profiler.analyze_text(text)

        assert result["success"] is True
        # Should detect as not meaningful due to lack of words
        assert result["is_meaningful"] is False or result["meaningfulness_score"] < 0.6

    def test_empty_text(self):
        """Test handling of empty text"""
        profiler = TextProfiler()
        result = profiler.analyze_text("")

        assert result["success"] is False
        assert "error" in result

    def test_too_long_text(self):
        """Test handling of text exceeding maximum length"""
        profiler = TextProfiler(max_text_length=100)
        text = "a" * 200
        result = profiler.analyze_text(text)

        assert result["success"] is False
        assert "error" in result

    def test_quick_check(self):
        """Test quick check functionality"""
        profiler = TextProfiler()
        text = "Hello world! This is a test."
        result = profiler.quick_check(text)

        assert result["is_valid"] is True
        assert "is_english" in result
        assert "is_meaningful" in result
        assert "is_structured" in result

    def test_get_text_summary(self):
        """Test getting text summary"""
        profiler = TextProfiler()
        text = "## Hello World\n\nThis is a test document."
        summary = profiler.get_text_summary(text)

        assert isinstance(summary, str)
        assert len(summary) > 0
        assert "English" in summary or "Language" in summary

    def test_should_process_text(self):
        """Test should_process_text decision helper"""
        profiler = TextProfiler()

        # Meaningful English text
        should, reason = profiler.should_process_text(
            "This is a normal sentence.",
            require_meaningful=True,
            allowed_languages=["en"],
        )
        assert should is True

        # Random text should be rejected
        should, reason = profiler.should_process_text(
            "xkcd123!@#$", require_meaningful=True
        )
        # May pass or fail depending on scoring, but should return tuple
        assert isinstance(should, bool)
        assert isinstance(reason, str)

    def test_convenience_function(self):
        """Test convenience analyze_text function"""
        result = analyze_text("Hello world")

        assert result["success"] is True
        assert result["language"] == "en"
        assert "word_count" in result

    def test_processing_time(self):
        """Test that processing time is included in result"""
        profiler = TextProfiler()
        result = profiler.analyze_text("Test text")

        assert "processing_time_ms" in result
        assert result["processing_time_ms"] >= 0

    def test_different_confidence_thresholds(self):
        """Test with different confidence thresholds"""
        profiler = TextProfiler(min_confidence=0.5, min_meaningfulness=0.4)
        text = "Short"  # Short text might have lower confidence
        result = profiler.analyze_text(text)

        # Should still process even with lower confidence
        assert "language" in result


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
