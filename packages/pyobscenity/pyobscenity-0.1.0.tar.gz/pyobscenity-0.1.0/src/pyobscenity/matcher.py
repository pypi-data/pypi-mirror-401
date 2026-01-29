import abc
from dataclasses import dataclass
from typing import Optional
import regex

from pyobscenity.transformers import Transformer
from pyobscenity.util import compare_intervals, is_high_surrogate, is_low_surrogate

@dataclass
class MatchPayload:
    startIndex: int
    endIndex: int
    matchLength: int
    termId: int

@dataclass
class BlacklistedTerm:
    id: int
    term: str

def compare_matches(a: MatchPayload, b: MatchPayload) -> int:
    '''
    Compares two MatchPayload objects for sorting.
    :param a: The first MatchPayload object.
    :param b: The second MatchPayload object.
    :return: Negative if a < b, positive if a > b, zero if equal.
    '''
    result = compare_intervals(a.startIndex, a.endIndex, b.startIndex, b.endIndex)
    if result != 0:
        return result
    return 0 if a.termId == b.termId else -1 if a.termId < b.termId else 1

class Matcher(abc.ABC):
    '''
    Base class for matchers.
    '''
    @abc.abstractmethod
    def get_all_matches(self, input: str, sorted: Optional[bool] = False) -> list[MatchPayload]:
        '''
        Gets all matches in the input text.
        :param input: The input text to be matched against.
        :return: A list of MatchPayload objects representing the matches.
        '''
        pass

    @abc.abstractmethod
    def has_match(self, input: str) -> bool:
        '''
        Checks if there is at least one match in the input text.
        :param input: The input text to be checked.
        :return: True if there is at least one match, False otherwise.
        '''
        pass

class RegexMatcher(Matcher):
    '''
    Matcher that uses regular expressions.
    '''
    def __init__(self, 
                 blacklisted_terms: list, 
                 whitelisted_terms: list | None = None,
                 blacklist_transformers: list | None = None,
                 whitelist_transformers: list | None = None):
        '''
        Initializes the RegexMatcher with blacklisted and whitelisted terms.
        :param blacklisted_terms: A list representing blacklisted terms.
        :param whitelisted_terms: A list representing whitelisted terms.
        '''
        self.blacklisted_terms = blacklisted_terms
        self.whitelisted_terms = whitelisted_terms or []
        self.blacklist_transformers = blacklist_transformers or []
        self.whitelist_transformers = whitelist_transformers or []
        self.compile_terms()

    def get_all_matches(self, input: str, sorted: Optional[bool] = False) -> list[MatchPayload]:
        whitelisted_intervals = self.get_whitelisted_intervals(input)
        transformedToOrigIndex, transformed = self.apply_transformers(input, self.blacklist_transformers)

        matches = []
        for term in self.compiled_blacklisted_terms:
            for match in term['regex'].finditer(transformed):
                start, end = match.start(), match.end()
                orig_start = transformedToOrigIndex[start]
                orig_end = transformedToOrigIndex[end - 1] + 1

                if orig_end < len(input) and is_high_surrogate(input[orig_end - 1]) and is_low_surrogate(input[orig_end]):
                    orig_end += 1

                if not self.is_interval_whitelisted(orig_start, orig_end, whitelisted_intervals):
                    matches.append(MatchPayload(
                        startIndex=orig_start,
                        endIndex=orig_end,
                        matchLength=orig_end - orig_start,
                        termId=term['id']
                    ))

        if sorted:
            matches.sort(key=lambda m: (m.startIndex, m.endIndex, m.termId))

        return matches
    
    def has_match(self, input: str) -> bool:
        whitelisted_intervals = self.get_whitelisted_intervals(input)
        transformedToOrigIndex, transformed = self.apply_transformers(input, self.blacklist_transformers)

        for term in self.compiled_blacklisted_terms:
            for match in term['regex'].finditer(transformed):
                start, end = match.start(), match.end()
                orig_start = transformedToOrigIndex[start]
                orig_end = transformedToOrigIndex[end - 1] + 1

                if orig_end < len(input) and is_high_surrogate(input[orig_end - 1]) and is_low_surrogate(input[orig_end]):
                    orig_end += 1

                if not self.is_interval_whitelisted(orig_start, orig_end, whitelisted_intervals):
                    return True

        return False
    
    def get_whitelisted_intervals(self, input: str) -> list[tuple[int, int]]:
        intervals = []
        transformedToOrigIndex, transformed = self.apply_transformers(input, self.whitelist_transformers)

        for term in self.compiled_whitelisted_terms:
            for match in term['regex'].finditer(transformed):
                start, end = match.start(), match.end()
                orig_start = transformedToOrigIndex[start]
                orig_end = transformedToOrigIndex[end - 1] + 1

                if orig_end < len(input) and is_high_surrogate(input[orig_end - 1]) and is_low_surrogate(input[orig_end]):
                    orig_end += 1

                intervals.append((orig_start, orig_end))

        intervals.sort(key=lambda interval: (interval[0], interval[1]))
        return intervals

    def is_interval_whitelisted(self, start: int, end: int, intervals: list[tuple[int, int]]) -> bool:
        '''
        Determines whether the interval [start, end) overlaps any whitelisted interval.
        Assumes intervals are sorted and non-overlapping (as produced by get_whitelisted_intervals).
        '''
        if not intervals:
            return False

        for w_start, w_end in intervals:
            if w_end <= start:
                continue
            if w_start >= end:
                break
            return True

        return False
    
    def apply_transformers(self, input: str, transformers: list[Transformer]) -> tuple[list[int], str]:
        transformed = input
        transformed_to_orig = list(range(len(input)))

        if not transformers:
            return transformed_to_orig, transformed

        for transformer in transformers:
            new_chars: list[str] = []
            new_mapping: list[int] = []

            for idx, char in enumerate(transformed):
                orig_index = transformed_to_orig[idx]
                transformed_chunk = transformer.transform_text(char)

                for out_char in transformed_chunk:
                    new_chars.append(out_char)
                    new_mapping.append(orig_index)

            transformed = ''.join(new_chars)
            transformed_to_orig = new_mapping

        for transformer in transformers:
            transformer.reset()

        return transformed_to_orig, transformed
    
    def compile_terms(self):
        self.compiled_blacklisted_terms = []
        self.compiled_whitelisted_terms = []

        for term in self.blacklisted_terms:
            self.compiled_blacklisted_terms.append({
                'id': term['id'],
                'regex': regex.compile(term['pattern'].as_regex()) if hasattr(term['pattern'], 'as_regex') else regex.compile(term['pattern'])
            })

        for term in self.whitelisted_terms:
            self.compiled_whitelisted_terms.append({
                'id': term['id'],
                'regex': regex.compile(term['pattern'].as_regex()) if hasattr(term['pattern'], 'as_regex') else regex.compile(term['pattern'])
            })
