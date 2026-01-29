from pyobscenity.censor import CensorContext, TextCensor, KeepStartCensor, KeepEndCensor, FullCensor, RandomCharCensor, FixedCensor
from pyobscenity.matcher import MatchPayload

def test_text_censor_no_matches():
    '''
    Test the TextCensor with no matches.
    '''
    def strategy(_: CensorContext) -> str:
        return 'CENSORED'

    text_censor = TextCensor(strategy)
    input_text = "This is a test."
    output_text = text_censor(input_text, [])
    assert output_text == input_text, "TextCensor with no matches should return the original text."

def test_keep_start_censor():
    '''
    Test the KeepStartCensor.
    '''
    keep_start_censor = KeepStartCensor(keep_length=2, censor_char='#')
    input_text = "SensitiveData"
    output_text = keep_start_censor(input_text, [MatchPayload(0, len(input_text), len(input_text), 1)])
    assert output_text == "Se###########", "KeepStartCensor failed."

    input_text2 = "DataSensitive"
    output_text2 = keep_start_censor(input_text2, [MatchPayload(4, len(input_text2), len(input_text2)-4, 1)])
    assert output_text2 == "DataSe#######", "KeepStartCensor failed."

def test_keep_end_censor():
    '''
    Test the KeepEndCensor.
    '''
    keep_end_censor = KeepEndCensor(keep_length=4, censor_char='#')
    input_text = "SensitiveData"
    output_text = keep_end_censor(input_text, [MatchPayload(0, len(input_text), len(input_text), 1)])
    assert output_text == "#########Data", "KeepEndCensor failed."

    input_text2 = "DataSensitive"
    output_text2 = keep_end_censor(input_text2, [MatchPayload(4, len(input_text2), len(input_text2)-4, 1)])
    assert output_text2 == "Data#####tive", "KeepEndCensor failed."

def test_full_censor():
    '''
    Test the FullCensor.
    '''
    full_censor = FullCensor(censor_char='#')
    input_text = "SensitiveData"
    output_text = full_censor(input_text, [MatchPayload(0, len(input_text), len(input_text), 1)])
    assert output_text == '#' * len(input_text), "FullCensor failed."

    input_text2 = "DataSensitive"
    output_text2 = full_censor(input_text2, [MatchPayload(4, len(input_text2), len(input_text2)-4, 1)])
    assert output_text2 == "Data#########", "FullCensor failed."

def test_random_char_censor():
    '''
    Test the RandomCharCensor.
    '''
    random_char_censor = RandomCharCensor('123456789')
    input_text = "SensitiveData"
    output_text = random_char_censor(input_text, [MatchPayload(0, len(input_text), len(input_text), 1)])
    assert len(output_text) == len(input_text), "RandomCharCensor failed."
    assert output_text != input_text, "RandomCharCensor failed."
    assert all(c in '123456789' for c in output_text), "RandomCharCensor failed."

    input_text2 = "DataSensitive"
    output_text2 = random_char_censor(input_text2, [MatchPayload(4, len(input_text2), len(input_text2)-4, 1)])
    assert len(output_text2) == len(input_text2), "RandomCharCensor failed."
    assert output_text2[:4] == "Data", "RandomCharCensor failed."
    assert all(c in '123456789' for c in output_text2[4:]), "RandomCharCensor failed."

def test_fixed_censor():
    '''
    Test the FixedCensor.
    '''
    fixed_censor = FixedCensor("CENSORED")
    input_text = "SensitiveData"
    output_text = fixed_censor(input_text, [MatchPayload(0, len(input_text), len(input_text), 1)])
    assert output_text == "CENSORED", "FixedCensor failed."

    input_text2 = "DataSensitive"
    output_text2 = fixed_censor(input_text2, [MatchPayload(4, len(input_text2), len(input_text2)-4, 1)])
    assert output_text2 == "DataCENSORED", "FixedCensor failed."