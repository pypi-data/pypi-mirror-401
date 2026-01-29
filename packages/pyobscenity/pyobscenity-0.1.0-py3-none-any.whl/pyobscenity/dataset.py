from dataclasses import dataclass
from typing import Callable

from pyobscenity.matcher import MatchPayload
from pyobscenity.pattern import ParsedPattern, PatternParser

def assign_incrementing_ids(terms: list[ParsedPattern]) -> list[dict]:
	'''
	Assigns incrementing IDs to a list of terms.
	:param terms: List of terms to assign IDs to.
	:return: List of dictionaries with 'id' and 'pattern' keys.
	'''
	return [{'id': i, 'pattern': term} for i, term in enumerate(terms)]

@dataclass
class PhraseContainer:
    metadata: any
    '''Metadata associated with the phrase.'''
    patterns: list[ParsedPattern]
    '''Patterns associated with the phrase.'''
    whitelistedTerms: list[str]
    '''Terms to not censor even if they match patterns.'''

class PhraseBuilder:
    def __init__(self):
        self.metadata = None
        self.patterns = []
        self.whitelistedTerms = []
        self._parser = PatternParser()

    def add_pattern(self, pattern: str | ParsedPattern) -> 'PhraseBuilder':
        if isinstance(pattern, str):
            pattern = self._parser.parse_pattern(pattern)
        self.patterns.append(pattern)
        return self
    
    def set_metadata(self, metadata: any) -> 'PhraseBuilder':
        self.metadata = metadata
        return self
    
    def add_whitelisted_term(self, term: str) -> 'PhraseBuilder':
        self.whitelistedTerms.append(term)
        return self
    
    def build(self) -> PhraseContainer:
        return PhraseContainer(
            metadata=self.metadata,
            patterns=self.patterns,
            whitelistedTerms=self.whitelistedTerms
        )


class Dataset:
    def __init__(self):
        self.containers = []
        self.patternCount = 0
        self.patternIdToContainerIndex = {}

    def add_all(self, other: 'Dataset') -> 'Dataset':
        for container in other.containers:
            self.register_container(container)
        return self
    
    def remove_phrases_if(self, predicate: Callable[[PhraseContainer], bool]) -> 'Dataset':
        self.patternCount = 0
        self.patternIdToContainerIndex.clear()
        containers = self.containers.copy()
        self.containers.clear()
        for container in containers:
            if not predicate(container):
                self.register_container(container)

        return self
    
    def add_phrase(self, fn: Callable[[PhraseBuilder], PhraseBuilder]) -> 'Dataset':
        container = fn(PhraseBuilder()).build()
        self.register_container(container)
        return self
    
    def get_payload_with_phrase_metadata(self, payload: MatchPayload) -> any:
        offset = self.patternIdToContainerIndex.get(payload.termId)
        if offset is None:
            raise ValueError(f"Pattern ID {payload.termId} not found in dataset.")
        return {
            **payload.__dict__,
            "phraseMetadata": self.containers[offset].metadata
        }
    
    def build(self) -> dict:
        return {
			"blacklisted_terms": assign_incrementing_ids([pattern for container in self.containers for pattern in container.patterns]),
			"whitelisted_terms": assign_incrementing_ids([term for container in self.containers for term in container.whitelistedTerms]),
		}

    def register_container(self, container: PhraseContainer):
        offset = len(self.containers)
        self.containers.append(container)
        for pattern in container.patterns:
            self.patternIdToContainerIndex[self.patternCount] = offset
            self.patternCount += 1
