"""
Tests that verify all README examples work correctly.

This ensures the documentation is accurate and examples don't become stale.
"""

import pytest
from pyobscenity import (
    censor,
    check,
    find_matches,
    ProfanityFilter,
    Dataset,
    RegexMatcher,
    FullCensor,
    LowercaseTransformer,
    english_dataset,
    english_recommended_blacklist_transformers,
)


class TestReadmeQuickStart:
    """Test Quick Start section examples."""

    def test_simple_one_liner_censoring(self):
        """Test: Simple One-Liner Censoring"""
        result = censor("This is fucking great!")
        # Output should be: "This is ****ing great!"
        assert "fucking" not in result
        assert "*" in result
        assert "This is" in result
        assert "great!" in result

    def test_check_for_profanity(self):
        """Test: Check for Profanity"""
        user_input = "hello shit"
        if check(user_input):
            found_profanity = True
        else:
            found_profanity = False
        assert found_profanity is True

    def test_find_profanity_matches(self):
        """Test: Find Profanity Matches"""
        matches = find_matches("fuck this shit")
        assert len(matches) >= 2  # Should find at least 2 matches
        # Verify we can iterate and access properties
        for match in matches:
            assert hasattr(match, "matched_text")
            assert hasattr(match, "start_index")
            assert len(match.matched_text) > 0
            assert match.start_index >= 0


class TestReadmeConvenienceAPI:
    """Test Convenience API section examples."""

    def test_censor_default(self):
        """Test: censor() - Default (full censoring with *)"""
        result = censor("This is shit")
        assert result == "This is ****"

    def test_censor_custom_char(self):
        """Test: censor() - Custom censor character"""
        result = censor("This is shit", censor_char="#")
        assert result == "This is ####"

    def test_censor_keep_start(self):
        """Test: censor() - Keep start characters"""
        result = censor("shit", censor_type="keep_start", keep_length=1)
        assert result == "s***"

    def test_censor_keep_end(self):
        """Test: censor() - Keep end characters"""
        result = censor("shit", censor_type="keep_end", keep_length=2)
        assert result == "**it"

    def test_censor_fixed(self):
        """Test: censor() - Fixed replacement"""
        result = censor("This is shit", censor_type="fixed", replacement="[REDACTED]")
        assert result == "This is [REDACTED]"

    def test_censor_grawlix(self):
        """Test: censor() - Grawlix (comic book style)"""
        result = censor("shit", censor_type="grawlix")
        # Should contain grawlix characters
        assert any(c in result for c in "@#$%&*")

    def test_check_without_profanity(self):
        """Test: check() - without profanity"""
        assert check("hello world") is False

    def test_check_with_profanity(self):
        """Test: check() - with profanity"""
        assert check("hello shit") is True

    def test_check_empty(self):
        """Test: check() - empty string"""
        assert check("") is False

    def test_find_matches_with_profanity(self):
        """Test: find_matches() - Get match details"""
        matches = find_matches("fuck this shit")
        assert len(matches) >= 2  # Should find at least 2 matches
        for m in matches:
            # Verify structure
            assert hasattr(m, "matched_text")
            assert hasattr(m, "start_index")
            assert hasattr(m, "end_index")
            # Verify values
            assert len(m.matched_text) > 0
            assert m.start_index >= 0
            assert m.end_index > m.start_index


class TestReadmeReusableFilters:
    """Test Reusable Filters section examples."""

    def test_filter_english_preset(self):
        """Test: Create a filter with English preset"""
        filter = ProfanityFilter.english()
        assert filter is not None
        # Verify it can censor
        result = filter.censor("This is shit")
        assert "*" in result

    def test_filter_apply_to_multiple_texts(self):
        """Test: Apply filter to multiple texts"""
        filter = ProfanityFilter.english()
        texts = ["hello shit", "fucking great", "clean text"]
        censored = [filter.censor(text) for text in texts]
        assert len(censored) == 3
        # First two should have censoring
        assert "*" in censored[0]
        assert "*" in censored[1]
        # Third should be unchanged
        assert censored[2] == "clean text"

    def test_filter_customize_with_chaining(self):
        """Test: Customize with method chaining"""
        filter = (
            ProfanityFilter.english()
            .with_censor("grawlix")
        )
        result = filter.censor("shit")
        # Should contain grawlix characters
        assert any(c in result for c in "@#$%&*")

    def test_filter_change_strategy_on_fly(self):
        """Test: Change censoring strategy on the fly"""
        filter = ProfanityFilter.english().with_censor("grawlix")
        # Change strategy
        filter.with_censor("fixed", replacement="[BAD]")
        result = filter.censor("shit")
        assert result == "[BAD]"

    def test_filter_check_and_find(self):
        """Test: Check and find matches with the same filter"""
        filter = ProfanityFilter.english()
        if filter.has_match("shit"):
            matches = filter.find_matches("shit")
            assert len(matches) >= 1
        else:
            pytest.fail("Filter should detect 'shit'")


class TestReadmeCustomDatasets:
    """Test Custom Datasets section examples."""

    def test_custom_dataset_basic(self):
        """Test: Build custom dataset with your own profanity list"""
        dataset = (
            Dataset()
            .add_phrase(lambda p: p
                .set_metadata({"originalWord": "badword"})
                .add_pattern("|badword|")
                .add_whitelisted_term("badwords")  # Don't censor "badwords"
            )
            .add_phrase(lambda p: p
                .set_metadata({"originalWord": "naughty"})
                .add_pattern("|naughty|")
            )
        )

        filter = ProfanityFilter.custom(dataset)
        
        # Test censoring badword
        result1 = filter.censor("This is a badword")
        assert "*" in result1  # badword should be censored
        assert "badword" not in result1
        
        # Test that badwords (plural) is not censored due to whitelist
        result2 = filter.censor("These are badwords")
        assert result2 == "These are badwords"

    def test_custom_dataset_structure(self):
        """Test: Custom dataset can be built and used"""
        dataset = (
            Dataset()
            .add_phrase(lambda p: p
                .set_metadata({"originalWord": "test"})
                .add_pattern("|test|")
            )
        )
        
        filter = ProfanityFilter.custom(dataset)
        assert filter.has_match("test")
        assert not filter.has_match("clean")


class TestReadmeAdvancedUsage:
    """Test Advanced Usage section examples."""

    def test_low_level_api_power_users(self):
        """Test: Low-Level API (Power Users)"""
        # Build matcher with custom transformers
        dataset = english_dataset.build()
        matcher = RegexMatcher(
            blacklisted_terms=dataset["blacklisted_terms"],
            whitelisted_terms=dataset["whitelisted_terms"],
            blacklist_transformers=english_recommended_blacklist_transformers,
            whitelist_transformers=[LowercaseTransformer()],
        )

        # Get matches
        matches = matcher.get_all_matches("hello shit")
        assert len(matches) >= 1

        # Apply custom censoring
        censor_instance = FullCensor("*")
        result = censor_instance.apply_censor("hello shit", matches)
        assert "shit" not in result
        assert "hello" in result


class TestReadmeCensorTypes:
    """Test various censor type examples from the table."""

    def test_censor_type_full(self):
        """Test: full - Replace entire match (default)"""
        result = censor("shit", censor_type="full", censor_char="*")
        assert result == "****"

    def test_censor_type_keep_start(self):
        """Test: keep_start - Keep N characters from start"""
        result = censor("shit", censor_type="keep_start", keep_length=1, censor_char="*")
        assert result == "s***"

    def test_censor_type_keep_end(self):
        """Test: keep_end - Keep N characters from end"""
        result = censor("shit", censor_type="keep_end", keep_length=1, censor_char="*")
        assert result == "***t"

    def test_censor_type_fixed(self):
        """Test: fixed - Replace with fixed string"""
        result = censor("shit", censor_type="fixed", replacement="[REDACTED]")
        assert result == "[REDACTED]"

    def test_censor_type_random(self):
        """Test: random - Replace with random characters"""
        result = censor("shit", censor_type="random", censor_char="@")
        # Should have same length as "shit" but with @ characters
        assert len(result) == 4
        assert "@" in result

    def test_censor_type_grawlix(self):
        """Test: grawlix - Comic book-style symbols"""
        result = censor("shit", censor_type="grawlix")
        # Should contain grawlix characters
        assert any(c in result for c in "@#$%&*")


class TestReadmeTextTransformers:
    """Test text transformer detection capabilities."""

    def test_detect_case_variations(self):
        """Test: Detect case variations (shit, SHIT, Shit)"""
        assert check("shit")
        assert check("SHIT")
        assert check("Shit")

    def test_detect_leet_speak(self):
        """Test: Detect leet speak (sh1t, 5h1t)"""
        assert check("sh1t")
        assert check("5h1t")

    def test_censoring_works_with_variations(self):
        """Test: Censoring works with variations"""
        # Case variations
        assert censor("SHIT") != "SHIT"
        assert censor("Shit") != "Shit"
        # Leet speak variations
        assert censor("sh1t") != "sh1t"
        assert censor("5h1t") != "5h1t"


class TestReadmeIntegration:
    """Integration tests combining multiple README examples."""

    def test_workflow_check_then_censor(self):
        """Test: Common workflow - check then censor"""
        text = "This is shit"
        if check(text):
            censored = censor(text)
            assert censored != text
            assert "shit" not in censored
        else:
            pytest.fail("Should detect profanity in text")

    def test_workflow_find_and_analyze(self):
        """Test: Find matches and analyze them"""
        text = "fuck this shit"
        matches = find_matches(text)
        assert len(matches) >= 2
        
        # Verify each match can be analyzed
        for match in matches:
            assert match.matched_text in text
            assert text[match.start_index:match.end_index] == match.matched_text

    def test_workflow_filter_batch_processing(self):
        """Test: Using filter for batch processing"""
        filter = ProfanityFilter.english().with_censor("fixed", replacement="***")
        
        texts = [
            "hello shit",
            "fucking great",
            "clean text",
            "damn it",
        ]
        
        results = [filter.censor(text) for text in texts]
        
        # Verify batch processing works
        assert len(results) == len(texts)
        # All texts should be processed without error
        for result in results:
            assert isinstance(result, str)

    def test_workflow_custom_dataset_batch(self):
        """Test: Using custom dataset for batch processing"""
        dataset = (
            Dataset()
            .add_phrase(lambda p: p.set_metadata({"originalWord": "badword"}).add_pattern("|badword|"))
            .add_phrase(lambda p: p.set_metadata({"originalWord": "naughty"}).add_pattern("|naughty|"))
        )
        
        filter = ProfanityFilter.custom(dataset)
        
        texts = [
            "This is badword",
            "That is naughty",
            "This is clean",
        ]
        
        results = [filter.censor(text) for text in texts]
        
        # Verify results
        assert "*" in results[0]  # badword censored
        assert "*" in results[1]  # naughty censored
        assert results[2] == "This is clean"  # clean text unchanged
