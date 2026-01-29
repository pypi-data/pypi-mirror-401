from pyobscenity.dataset import Dataset, PhraseBuilder, PhraseContainer
from pyobscenity.pattern import ParsedPattern

def test_phrase_builder_and_container():
    builder = PhraseBuilder()
    builder.set_metadata({'category': 'test'})
    builder.add_pattern(ParsedPattern(nodes=[], require_word_boundary_at_start=False, require_word_boundary_at_end=False))
    builder.add_whitelisted_term("safeTerm")
    container = builder.build()

    assert container.metadata == {'category': 'test'}
    assert len(container.patterns) == 1
    assert container.whitelistedTerms == ["safeTerm"]