from pyobscenity.transformers import Transformer, LowercaseTransformer, SkipNonAlphaTransformer, CollapseDuplicateTransformer, RemapCharacterTransformer, ResolveConfusablesTransformer, ResolveLeetTransformer

def test_identity_transformer():
    '''
    Test the Transformer base class with an identity transformation.
    '''
    identity_transformer = Transformer(
        transform_func=lambda text: text
    )
    input_text = "Hello, World!"
    output_text = identity_transformer.transform_text(input_text)
    assert output_text == input_text, "Identity transformer should return the same text."

def test_lowercase_transformer():
    '''
    Test the LowercaseTransformer.
    '''
    lowercase_transformer = LowercaseTransformer()
    input_text = "Hello, World!"
    output_text = lowercase_transformer.transform_text(input_text)
    assert output_text == "hello, world!", "Lowercase transformer failed."

def test_skip_non_alpha_transformer():
    '''
    Test the SkipNonAlphaTransformer.
    '''
    skip_non_alpha_transformer = SkipNonAlphaTransformer()
    input_text = "Hello, World! 123"
    output_text = skip_non_alpha_transformer.transform_text(input_text)
    assert output_text == "HelloWorld", "SkipNonAlpha transformer failed."

def test_collapse_duplicate_transformer():
    '''
    Test the CollapseDuplicateTransformer.
    '''
    collapse_duplicate_transformer = CollapseDuplicateTransformer()
    input_text = "Heeellooo,, Wooorrrld!!!"
    output_text = collapse_duplicate_transformer.transform_text(input_text)
    assert output_text == "Helo, World!", "CollapseDuplicate transformer failed."

    # Reset and test again
    collapse_duplicate_transformer.reset()
    input_text2 = "Hhhhhhiiiiiii"
    output_text2 = collapse_duplicate_transformer.transform_text(input_text2)
    assert output_text2 == "Hhi", "CollapseDuplicate transformer failed."

    # Test thresholds
    custom_collapse_transformer = CollapseDuplicateTransformer(2)
    input_text3 = "hello"
    output_text3 = custom_collapse_transformer.transform_text(input_text3)
    assert output_text3 == "hello", "CollapseDuplicate transformer with threshold failed."

    # Test custom character thresholds
    custom_char_transformer = CollapseDuplicateTransformer(3, {
        'o': 2,
        'l': 1,
    })
    input_text4 = "hellooo!!!!!"
    output_text4 = custom_char_transformer.transform_text(input_text4)
    assert output_text4 == "heloo!!!", "CollapseDuplicate transformer with custom char thresholds failed."

    # Test with None threshold
    none_threshold_transformer = CollapseDuplicateTransformer(None, {
        ' ': 1,
    })
    input_text5 = "This    is  a    test."
    output_text5 = none_threshold_transformer.transform_text(input_text5)
    assert output_text5 == "This is a test.", "CollapseDuplicate transformer with None threshold failed."

def test_remap_character_transformer():
    '''
    Test the RemapCharacterTransformer.
    '''
    mapping = {'H': 'e', 'e': 'l', 'l': 'o', 'o': 'H'}
    remap_character_transformer = RemapCharacterTransformer(mapping)
    input_text = "Hello"
    output_text = remap_character_transformer.transform_text(input_text)
    assert output_text == "elooH", "RemapCharacter transformer failed."

def test_resolve_confusables_transformer():
    '''
    Test the ResolveConfusablesTransformer.
    '''
    resolve_confusables_transformer = ResolveConfusablesTransformer()
    input_text = "ⓗⓔⓛⓛⓞ 𝟘𝟙, hello"
    output_text = resolve_confusables_transformer.transform_text(input_text)
    assert output_text == "hello 01, hello", "ResolveConfusables transformer failed."