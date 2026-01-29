from collections.abc import Callable
from dataclasses import dataclass
from functools import cmp_to_key

from pyobscenity.matcher import MatchPayload
from pyobscenity.matcher import compare_matches

@dataclass
class CensorContext:
    """Context for censoring operations."""
    input: str
    """The entire input text, without any censoring applied to it."""
    overlapsAtEnd: bool
    """Whether the current region overlaps at the end with some other region."""
    overlapsAtStart: bool
    """Whether the current region overlaps at the start with some other region."""

class TextCensor:
    '''
    Base class for text censors.
    '''

    def __init__(self, strategy: Callable[[CensorContext], str]):
        '''
        Initializes the TextCensor with a censoring strategy.
        :param strategy: A function that takes a CensorContext and returns a censored string.
        '''
        self.strategy = strategy

    def set_strategy(self, strategy: Callable[[CensorContext], str]):
        '''
        Sets a new censoring strategy.
        :param strategy: A function that takes a CensorContext and returns a censored string.
        '''
        self.strategy = strategy

    def apply_censor(self, input: str, matches: list[MatchPayload]) -> str:
        '''
        Applies the censoring strategy to the input text based on the provided matches.
        :param input: The input text to be censored.
        :param matches: A list of MatchPayload objects representing the regions to be censored.
        :return: The censored text.
        '''

        if not matches:
            return input
        
        # Sort matches using compare_matches
        sorted_matches = sorted(matches, key=cmp_to_key(compare_matches))

        censored = ''
        last_index = 0

        for i, match in enumerate(sorted_matches):
            if last_index > match.endIndex:
                # completely contained in the previous span
                continue

            overlaps_at_start = match.startIndex < last_index

            if not overlaps_at_start:
                censored += input[last_index:match.startIndex]

            actual_start_index = max(last_index, match.startIndex)
            overlaps_at_end = i < len(sorted_matches) - 1 \
                and match.endIndex > sorted_matches[i + 1].startIndex \
                and match.endIndex > sorted_matches[i + 1].endIndex
            
            censored += self.strategy(CensorContext(
                input=input[actual_start_index:match.endIndex],
                overlapsAtEnd=overlaps_at_end,
                overlapsAtStart=overlaps_at_start
            ))

            last_index = max(last_index, match.endIndex)

        censored += input[last_index:]
        return censored
    
    def __call__(self, *args, **kwds):
        return self.apply_censor(*args, **kwds)

class KeepStartCensor(TextCensor):
    '''
    Censor that keeps the start of the matched region and censors the rest.
    '''

    def __init__(self, keep_length: int = 1, censor_char: str = '*'):
        '''
        Initializes the KeepStartCensor.
        :param keep_length: Number of characters to keep at the start of the matched region.
        :param censor_char: Character to use for censoring.
        '''
        def strategy(context: CensorContext) -> str:
            if context.overlapsAtStart:
                return ''
            keep_part = context.input[:keep_length]
            censor_part = censor_char * (len(context.input) - len(keep_part))
            return keep_part + censor_part

        super().__init__(strategy)

class KeepEndCensor(TextCensor):
    '''
    Censor that keeps the end of the matched region and censors the rest.
    '''

    def __init__(self, keep_length: int = 1, censor_char: str = '*'):
        '''
        Initializes the KeepEndCensor.
        :param keep_length: Number of characters to keep at the end of the matched region.
        :param censor_char: Character to use for censoring.
        '''
        def strategy(context: CensorContext) -> str:
            if context.overlapsAtEnd:
                return ''
            keep_part = context.input[-keep_length:]
            censor_part = censor_char * (len(context.input) - len(keep_part))
            return censor_part + keep_part

        super().__init__(strategy)

class FullCensor(TextCensor):
    '''
    Censor that censors the entire matched region.
    '''

    def __init__(self, censor_char: str = '*'):
        '''
        Initializes the FullCensor.
        :param censor_char: Character to use for censoring.
        '''
        def strategy(context: CensorContext) -> str:
            return '' if context.overlapsAtStart or context.overlapsAtEnd else censor_char * len(context.input)

        super().__init__(strategy)

class RandomCharCensor(TextCensor):
    '''
    Censor that replaces the matched region with random characters.
    '''

    def __init__(self, random_chars: str):
        '''
        Initializes the RandomCharCensor.
        :param random_chars: String of characters to use for random replacement.
        '''
        def strategy(context: CensorContext) -> str:
            if context.overlapsAtStart or context.overlapsAtEnd:
                return ''
            random_string = ''
            for i in range(len(context.input)):
                random_string += random_chars[i % len(random_chars)]
            return random_string

        super().__init__(strategy)

class GrawlixCensor(RandomCharCensor):
    '''
    Censor that replaces the matched region with [grawlix](https://www.merriam-webster.com/words-at-play/grawlix-symbols-swearing-comic-strips) characters.
    '''

    def __init__(self):
        '''
        Initializes the GrawlixCensor.
        '''
        super().__init__('@#$%&*')
        

class FixedCensor(TextCensor):
    '''
    Censor that replaces the matched region with a fixed string.
    '''

    def __init__(self, replacement: str = '[CENSORED]'):
        '''
        Initializes the FixedCensor.
        :param replacement: The fixed string to replace the matched region.
        '''
        def strategy(context: CensorContext) -> str:
            return '' if context.overlapsAtStart or context.overlapsAtEnd else replacement

        super().__init__(strategy)