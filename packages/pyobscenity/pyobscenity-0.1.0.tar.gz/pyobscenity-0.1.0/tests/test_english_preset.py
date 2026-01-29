from pyobscenity.english_preset import english_dataset, english_recommended_blacklist_transformers, english_recommended_whitelist_transformers
from pyobscenity.matcher import RegexMatcher
from pyobscenity.censor import FullCensor

def test_english_dataset():
    dataset = english_dataset.build()
    matcher = RegexMatcher(
        blacklisted_terms=dataset['blacklisted_terms'], 
        whitelisted_terms=dataset['whitelisted_terms'],
        blacklist_transformers=english_recommended_blacklist_transformers,
        whitelist_transformers=english_recommended_whitelist_transformers
    )
    censor = FullCensor()

    input_text = "Shit is fucked up"

    matches = matcher.get_all_matches(input_text)

    assert len(matches) > 2

    result = censor.apply_censor(input_text, matches=matches)

    assert result == "**** is ****ed up"

    input_test_2 = "Don't censor this thing at all please, it's innocent text"

    matches_2 = matcher.get_all_matches(input_test_2)
    
    assert len(matches_2) == 0

    result_2 = censor.apply_censor(input_test_2, matches=matches_2)

    assert result_2 == input_test_2

def test_advanced_english():
    dataset = english_dataset.build()
    matcher = RegexMatcher(
        blacklisted_terms=dataset['blacklisted_terms'], 
        whitelisted_terms=dataset['whitelisted_terms'],
        blacklist_transformers=english_recommended_blacklist_transformers,
        whitelist_transformers=english_recommended_whitelist_transformers
    )
    censor = FullCensor()

    input_text = "This is a \"fucking\" joke"

    matches = matcher.get_all_matches(input_text)
    assert len(matches) == 1

    censored = censor.apply_censor(input_text, matches=matches)
    assert censored == "This is a \"****ing\" joke"
