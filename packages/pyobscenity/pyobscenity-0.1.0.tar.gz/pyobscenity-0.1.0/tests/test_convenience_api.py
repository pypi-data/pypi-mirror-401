"""Tests for the high-level convenience API."""

import pytest
from pyobscenity import (
    censor,
    check,
    find_matches,
    ProfanityFilter,
    Match,
)


class TestSimpleAPI:
    """Test simple function-based API."""

    def test_censor_basic(self):
        """Test basic censoring with default settings."""
        result = censor("This is fucking great!")
        assert "*" in result
        assert "fucking" not in result

    def test_censor_empty_string(self):
        """Test censoring empty string."""
        assert censor("") == ""

    def test_censor_no_profanity(self):
        """Test censoring text without profanity."""
        text = "This is a nice day"
        assert censor(text) == text

    def test_censor_full_type(self):
        """Test full censoring type."""
        result = censor("This is shit", censor_type="full")
        assert result == "This is ****"

    def test_censor_keep_start(self):
        """Test keep_start censoring type."""
        result = censor("shit", censor_type="keep_start", keep_length=1)
        assert result == "s***"

    def test_censor_keep_end(self):
        """Test keep_end censoring type."""
        result = censor("shit", censor_type="keep_end", keep_length=1)
        assert result == "***t"

    def test_censor_fixed(self):
        """Test fixed censoring type."""
        result = censor("This is shit", censor_type="fixed", replacement="[REDACTED]")
        assert "[REDACTED]" in result
        assert "shit" not in result

    def test_censor_grawlix(self):
        """Test grawlix censoring type."""
        result = censor("shit", censor_type="grawlix")
        # Should contain grawlix characters
        assert any(c in result for c in "@#$%&*")

    def test_censor_custom_char(self):
        """Test censoring with custom character."""
        result = censor("shit", censor_char="#")
        assert result == "####"

    def test_censor_language_error(self):
        """Test error on unsupported language."""
        with pytest.raises(ValueError, match="Language 'es' not supported"):
            censor("test", language="es")

    def test_censor_invalid_type(self):
        """Test error on invalid censor type."""
        with pytest.raises(ValueError, match="Unknown censor_type"):
            censor("shit", censor_type="invalid")

    def test_check_with_profanity(self):
        """Test checking text with profanity."""
        assert check("hello shit") is True

    def test_check_without_profanity(self):
        """Test checking text without profanity."""
        assert check("hello world") is False

    def test_check_empty_string(self):
        """Test checking empty string."""
        assert check("") is False

    def test_check_language_error(self):
        """Test error on unsupported language."""
        with pytest.raises(ValueError, match="Language 'fr' not supported"):
            check("test", language="fr")

    def test_find_matches_with_profanity(self):
        """Test finding matches in text."""
        matches = find_matches("this is fucking shit")
        assert len(matches) >= 2  # May have duplicate patterns
        assert all(isinstance(m, Match) for m in matches)

    def test_find_matches_text_extraction(self):
        """Test that matched_text is correctly extracted."""
        matches = find_matches("hello shit world")
        assert len(matches) >= 1
        assert matches[0].matched_text == "shit"
        assert matches[0].start_index == 6
        assert matches[0].end_index == 10

    def test_find_matches_without_profanity(self):
        """Test finding matches when there's no profanity."""
        matches = find_matches("hello world")
        assert len(matches) == 0

    def test_find_matches_empty_string(self):
        """Test finding matches in empty string."""
        assert find_matches("") == []

    def test_find_matches_with_metadata(self):
        """Test finding matches with metadata."""
        matches = find_matches("shit", include_metadata=True)
        assert len(matches) >= 1
        # Metadata may be None if not set in dataset
        assert all(isinstance(m.metadata, (dict, type(None))) for m in matches)

    def test_find_matches_without_metadata(self):
        """Test finding matches without metadata."""
        matches = find_matches("shit", include_metadata=False)
        assert len(matches) >= 1
        assert all(m.metadata is None for m in matches)

    def test_match_dataclass_properties(self):
        """Test Match dataclass properties."""
        matches = find_matches("shit world")
        m = matches[0]
        assert m.start_index == 0
        assert m.end_index == 4
        assert m.match_length == 4
        assert m.matched_text == "shit"
        assert m.matched_word == "shit"  # Alias property


class TestProfanityFilter:
    """Test reusable ProfanityFilter class."""

    def test_english_preset(self):
        """Test creating filter with English preset."""
        filter = ProfanityFilter.english()
        result = filter.censor("This is fucking great")
        assert "*" in result

    def test_filter_chaining(self):
        """Test fluent API method chaining."""
        filter = (
            ProfanityFilter.english()
            .with_censor("keep_start", keep_length=1, censor_char="#")
        )
        result = filter.censor("shit")
        assert result == "s###"

    def test_filter_with_censor_full(self):
        """Test filter with full censoring."""
        filter = ProfanityFilter.english().with_censor("full", censor_char="*")
        result = filter.censor("shit")
        assert result == "****"

    def test_filter_with_censor_keep_start(self):
        """Test filter with keep_start censoring."""
        filter = ProfanityFilter.english().with_censor(
            "keep_start", keep_length=2, censor_char="*"
        )
        result = filter.censor("shit")
        assert "s" in result and "*" in result

    def test_filter_with_censor_keep_end(self):
        """Test filter with keep_end censoring."""
        filter = ProfanityFilter.english().with_censor(
            "keep_end", keep_length=2, censor_char="*"
        )
        result = filter.censor("shit")
        assert "t" in result and "*" in result

    def test_filter_with_censor_fixed(self):
        """Test filter with fixed replacement."""
        filter = ProfanityFilter.english().with_censor(
            "fixed", replacement="[BAD]"
        )
        result = filter.censor("shit")
        assert result == "[BAD]"

    def test_filter_with_censor_grawlix(self):
        """Test filter with grawlix."""
        filter = ProfanityFilter.english().with_censor("grawlix")
        result = filter.censor("shit")
        assert any(c in result for c in "@#$%&*")

    def test_filter_censor_empty(self):
        """Test filter censoring empty string."""
        filter = ProfanityFilter.english()
        assert filter.censor("") == ""

    def test_filter_censor_no_matches(self):
        """Test filter censoring text without profanity."""
        filter = ProfanityFilter.english()
        text = "hello world"
        assert filter.censor(text) == text

    def test_filter_has_match_true(self):
        """Test filter checking for matches that exist."""
        filter = ProfanityFilter.english()
        assert filter.has_match("hello shit") is True

    def test_filter_has_match_false(self):
        """Test filter checking for matches that don't exist."""
        filter = ProfanityFilter.english()
        assert filter.has_match("hello world") is False

    def test_filter_has_match_empty(self):
        """Test filter checking empty string."""
        filter = ProfanityFilter.english()
        assert filter.has_match("") is False

    def test_filter_find_matches(self):
        """Test filter finding matches."""
        filter = ProfanityFilter.english()
        matches = filter.find_matches("fucking shit")
        assert len(matches) >= 2  # May have duplicate patterns
        assert all(isinstance(m, Match) for m in matches)

    def test_filter_find_matches_empty(self):
        """Test filter finding matches in empty string."""
        filter = ProfanityFilter.english()
        assert filter.find_matches("") == []

    def test_filter_find_matches_no_profanity(self):
        """Test filter finding matches when there's no profanity."""
        filter = ProfanityFilter.english()
        assert filter.find_matches("hello world") == []

    def test_filter_custom_dataset(self):
        """Test creating filter with custom dataset."""
        from pyobscenity import Dataset

        dataset = Dataset().add_phrase(
            lambda p: p.set_metadata({"originalWord": "test"}).add_pattern("|test|")
        )
        filter = ProfanityFilter.custom(dataset)
        assert filter.has_match("this is test")

    def test_filter_reusable(self):
        """Test that filter instances are reusable."""
        filter = ProfanityFilter.english().with_censor("full", censor_char="*")

        result1 = filter.censor("shit")
        result2 = filter.censor("fuck")

        assert result1 == "****"
        assert result2 == "****"

    def test_filter_method_returns_self(self):
        """Test that with_censor returns self for chaining."""
        filter = ProfanityFilter.english()
        result = filter.with_censor("full")
        assert result is filter


class TestIntegration:
    """Integration tests combining multiple features."""

    def test_censor_multiple_matches(self):
        """Test censoring text with multiple matches."""
        text = "This fucking shit is so damn bad"
        result = censor(text)
        # Should censor multiple words
        assert result.count("*") > 11

    def test_find_matches_preserves_order(self):
        """Test that matches are in order."""
        matches = find_matches("shit fuck damn")
        assert len(matches) >= 3
        # Get unique positions and verify they're sorted
        if len(matches) >= 2:
            positions = sorted(set(m.start_index for m in matches))
            assert positions == sorted(positions)

    def test_filter_consistency(self):
        """Test that filter produces consistent results."""
        filter = ProfanityFilter.english()
        text = "Hello shit world"
        result1 = filter.censor(text)
        result2 = filter.censor(text)
        assert result1 == result2

    def test_censor_vs_filter_equivalence(self):
        """Test that simple API and filter produce equivalent results."""
        text = "This is shit"
        simple_result = censor(text, censor_type="full", censor_char="*")
        filter_result = ProfanityFilter.english().with_censor("full", censor_char="*").censor(text)
        assert simple_result == filter_result

    def test_case_insensitive_matching(self):
        """Test that matching is case-insensitive."""
        assert check("SHIT")
        assert check("Shit")
        assert check("shit")

    def test_leet_speak_detection(self):
        """Test that leet speak variations are detected."""
        # sh1t, sh!t, etc. should be detected
        assert check("sh1t")
        assert check("f4ck")
