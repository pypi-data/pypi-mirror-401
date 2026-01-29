"""
pyobscenity - A Python library for detecting and censoring profane/obscene text.

High-level convenience API for common use cases, with full access to lower-level
components for advanced customization.
"""

from typing import Optional, List
from dataclasses import dataclass

# Low-level imports (for backward compatibility and power users)
from pyobscenity.dataset import Dataset, PhraseBuilder
from pyobscenity.matcher import Matcher, RegexMatcher, MatchPayload
from pyobscenity.censor import TextCensor, FullCensor, KeepStartCensor, KeepEndCensor, FixedCensor, RandomCharCensor, GrawlixCensor
from pyobscenity.transformers import (
    Transformer,
    LowercaseTransformer,
    CollapseDuplicateTransformer,
    SkipNonAlphaTransformer,
    ResolveConfusablesTransformer,
    ResolveLeetTransformer,
    RemapCharacterTransformer,
)
from pyobscenity.english_preset import (
    english_dataset,
    english_recommended_blacklist_transformers,
    english_recommended_whitelist_transformers,
)
from pyobscenity.pattern import PatternParser

__version__ = "0.1.0"

__all__ = [
    # Convenience API
    "censor",
    "check",
    "find_matches",
    "ProfanityFilter",
    # Low-level components (backward compatibility)
    "Dataset",
    "PhraseBuilder",
    "Matcher",
    "RegexMatcher",
    "MatchPayload",
    "TextCensor",
    "FullCensor",
    "KeepStartCensor",
    "KeepEndCensor",
    "FixedCensor",
    "RandomCharCensor",
    "GrawlixCensor",
    "Transformer",
    "LowercaseTransformer",
    "CollapseDuplicateTransformer",
    "SkipNonAlphaTransformer",
    "ResolveConfusablesTransformer",
    "ResolveLeetTransformer",
    "RemapCharacterTransformer",
    "PatternParser",
]

# ============================================================================
# GLOBAL DEFAULTS & PRESETS
# ============================================================================

_DEFAULT_MATCHER: Optional[RegexMatcher] = None
_DEFAULT_CENSOR: Optional[TextCensor] = None


def _get_default_matcher() -> RegexMatcher:
    """Get or create the default matcher instance with English preset."""
    global _DEFAULT_MATCHER
    if _DEFAULT_MATCHER is None:
        dataset = english_dataset.build()
        _DEFAULT_MATCHER = RegexMatcher(
            blacklisted_terms=dataset["blacklisted_terms"],
            whitelisted_terms=dataset["whitelisted_terms"],
            blacklist_transformers=english_recommended_blacklist_transformers,
            whitelist_transformers=english_recommended_whitelist_transformers,
        )
    return _DEFAULT_MATCHER


def _get_default_censor() -> TextCensor:
    """Get or create the default censor instance."""
    global _DEFAULT_CENSOR
    if _DEFAULT_CENSOR is None:
        _DEFAULT_CENSOR = FullCensor("*")
    return _DEFAULT_CENSOR


# ============================================================================
# SIMPLE FUNCTION-BASED API
# ============================================================================


def censor(
    text: str,
    *,
    censor_char: str = "*",
    censor_type: str = "full",
    keep_length: int = 0,
    replacement: str = "[REDACTED]",
    language: str = "en",
) -> str:
    """
    Censor profanity in text using default settings.

    This is the simplest way to censor profanity. For more control or reusable
    filtering, use ProfanityFilter instead.

    Args:
        text: Input text to censor.
        censor_char: Character to use for censoring (default: "*").
        censor_type: Type of censoring strategy. Options:
            - "full": Replace entire match with censor_char (default)
            - "keep_start": Keep start characters, censor the rest
            - "keep_end": Censor start, keep end characters
            - "fixed": Replace with fixed replacement string
            - "random": Replace with random characters
            - "grawlix": Use grawlix symbols (@#$%&*)
        keep_length: For keep_start/keep_end, number of chars to keep (default: 0).
        replacement: For "fixed" type, the replacement string (default: "[REDACTED]").
        language: Language preset to use (default: "en"). Only "en" supported currently.

    Returns:
        Censored text. Uncensored if no profanity found.

    Examples:
        >>> censor("This is fucking great!")
        'This is ****ing great!'
        >>> censor("shit", censor_type="grawlix")
        '@#$%'
        >>> censor("badass", censor_type="keep_start", keep_length=2)
        'ba****'
    """
    if not text:
        return text

    if language != "en":
        raise ValueError(f"Language '{language}' not supported. Only 'en' is currently available.")

    matcher = _get_default_matcher()
    matches = matcher.get_all_matches(text)

    if not matches:
        return text

    # Create appropriate censor based on type
    if censor_type == "full":
        censor_instance = FullCensor(censor_char)
    elif censor_type == "keep_start":
        censor_instance = KeepStartCensor(keep_length, censor_char)
    elif censor_type == "keep_end":
        censor_instance = KeepEndCensor(keep_length, censor_char)
    elif censor_type == "fixed":
        censor_instance = FixedCensor(replacement)
    elif censor_type == "random":
        censor_instance = RandomCharCensor(censor_char)
    elif censor_type == "grawlix":
        censor_instance = GrawlixCensor()
    else:
        raise ValueError(
            f"Unknown censor_type: {censor_type}. "
            "Valid options: full, keep_start, keep_end, fixed, random, grawlix"
        )

    return censor_instance.apply_censor(text, matches)


def check(text: str, *, language: str = "en") -> bool:
    """
    Check if text contains profanity without censoring it.

    Args:
        text: Input text to check.
        language: Language preset to use (default: "en").

    Returns:
        True if profanity is found, False otherwise.

    Examples:
        >>> check("hello world")
        False
        >>> check("hello shit")
        True
    """
    if not text:
        return False

    if language != "en":
        raise ValueError(f"Language '{language}' not supported. Only 'en' is currently available.")

    matcher = _get_default_matcher()
    return matcher.has_match(text)


@dataclass
class Match:
    """Represents a profanity match in text."""

    start_index: int
    """Start position of the match (0-based)."""

    end_index: int
    """End position of the match (exclusive)."""

    match_length: int
    """Length of the matched text."""

    matched_text: str
    """The actual matched text from the input."""

    term_id: int
    """Internal term ID."""

    metadata: Optional[dict] = None
    """Optional metadata about the matched phrase."""

    @property
    def matched_word(self) -> str:
        """Alias for matched_text for convenience."""
        return self.matched_text


def find_matches(
    text: str, *, language: str = "en", include_metadata: bool = True
) -> List[Match]:
    """
    Find all profanity matches in text.

    Args:
        text: Input text to analyze.
        language: Language preset to use (default: "en").
        include_metadata: Include phrase metadata in results (default: True).

    Returns:
        List of Match objects with position and content information.

    Examples:
        >>> matches = find_matches("this is fucking shit")
        >>> for m in matches:
        ...     print(f"Found '{m.matched_text}' at position {m.start_index}")
        Found 'fucking' at position 8
        Found 'shit' at position 16
    """
    if not text:
        return []

    if language != "en":
        raise ValueError(f"Language '{language}' not supported. Only 'en' is currently available.")

    matcher = _get_default_matcher()
    raw_matches = matcher.get_all_matches(text)

    if not raw_matches:
        return []

    results = []
    for match in raw_matches:
        matched_text = text[match.startIndex : match.endIndex]
        metadata = getattr(match, "phraseMetadata", None) if include_metadata else None

        results.append(
            Match(
                start_index=match.startIndex,
                end_index=match.endIndex,
                match_length=match.matchLength,
                matched_text=matched_text,
                term_id=match.termId,
                metadata=metadata,
            )
        )

    return results


# ============================================================================
# REUSABLE FILTER CLASS WITH FLUENT BUILDER INTERFACE
# ============================================================================


class ProfanityFilter:
    """
    Configurable profanity filter with fluent builder interface.

    This class is ideal for reusable filtering scenarios where you want to
    apply the same configuration multiple times. It caches the compiled
    matcher/censor internally for better performance.

    Examples:
        >>> filter = ProfanityFilter.english()
        >>> filter.censor("bad language")
        'bad language'

        >>> filter = (
        ...     ProfanityFilter.english()
        ...     .with_censor("grawlix")
        ... )
        >>> filter.censor("shit")
        '@#$%'

        >>> filter = (
        ...     ProfanityFilter.english()
        ...     .with_censor("keep_start", keep_length=2, censor_char="#")
        ... )
        >>> filter.censor("badass")
        'ba####'
    """

    def __init__(
        self,
        matcher: RegexMatcher,
        censor_instance: TextCensor,
    ):
        """
        Initialize a profanity filter with custom matcher and censor.

        Users should typically use the class methods (english(), custom())
        instead of calling this directly.

        Args:
            matcher: RegexMatcher instance for detecting profanity.
            censor_instance: TextCensor instance for applying censoring.
        """
        self._matcher = matcher
        self._censor = censor_instance
        self._censor_type = "full"
        self._censor_char = "*"
        self._keep_length = 0
        self._replacement = "[REDACTED]"

    @classmethod
    def english(cls) -> "ProfanityFilter":
        """
        Create a profanity filter with English language preset.

        Uses the built-in English profanity dataset with recommended
        transformers for detecting common variations (leet speak, confusables, etc.).

        Returns:
            ProfanityFilter instance configured for English.
        """
        dataset = english_dataset.build()
        matcher = RegexMatcher(
            blacklisted_terms=dataset["blacklisted_terms"],
            whitelisted_terms=dataset["whitelisted_terms"],
            blacklist_transformers=english_recommended_blacklist_transformers,
            whitelist_transformers=english_recommended_whitelist_transformers,
        )
        censor_instance = FullCensor("*")
        return cls(matcher, censor_instance)

    @classmethod
    def custom(cls, dataset: Dataset) -> "ProfanityFilter":
        """
        Create a profanity filter with a custom dataset.

        Args:
            dataset: Dataset instance containing phrases to detect.

        Returns:
            ProfanityFilter instance configured with the custom dataset.
        """
        built = dataset.build()
        matcher = RegexMatcher(
            blacklisted_terms=built["blacklisted_terms"],
            whitelisted_terms=built["whitelisted_terms"],
            blacklist_transformers=[LowercaseTransformer()],
            whitelist_transformers=[LowercaseTransformer()],
        )
        censor_instance = FullCensor("*")
        return cls(matcher, censor_instance)

    def with_censor(
        self,
        censor_type: str = "full",
        *,
        censor_char: str = "*",
        keep_length: int = 0,
        replacement: str = "[REDACTED]",
    ) -> "ProfanityFilter":
        """
        Configure the censoring strategy.

        Args:
            censor_type: Type of censoring. Options:
                - "full": Replace entire match (default)
                - "keep_start": Keep N chars from start
                - "keep_end": Keep N chars from end
                - "fixed": Replace with fixed string
                - "random": Replace with random chars
                - "grawlix": Use grawlix symbols
            censor_char: Character for censoring (default: "*").
            keep_length: For keep_start/keep_end modes (default: 0).
            replacement: For "fixed" mode (default: "[REDACTED]").

        Returns:
            Self for method chaining.
        """
        self._censor_type = censor_type
        self._censor_char = censor_char
        self._keep_length = keep_length
        self._replacement = replacement

        if censor_type == "full":
            self._censor = FullCensor(censor_char)
        elif censor_type == "keep_start":
            self._censor = KeepStartCensor(keep_length, censor_char)
        elif censor_type == "keep_end":
            self._censor = KeepEndCensor(keep_length, censor_char)
        elif censor_type == "fixed":
            self._censor = FixedCensor(replacement)
        elif censor_type == "random":
            self._censor = RandomCharCensor(censor_char)
        elif censor_type == "grawlix":
            self._censor = GrawlixCensor()
        else:
            raise ValueError(
                f"Unknown censor_type: {censor_type}. "
                "Valid options: full, keep_start, keep_end, fixed, random, grawlix"
            )

        return self

    def with_transformers(
        self,
        blacklist: Optional[List[Transformer]] = None,
        whitelist: Optional[List[Transformer]] = None,
    ) -> "ProfanityFilter":
        """
        Override the text transformers used for matching.

        Transformers are applied to text before pattern matching to normalize
        variations like leet speak, confusables, and duplicate characters.

        Args:
            blacklist: List of transformers for blacklisted term matching.
            whitelist: List of transformers for whitelisted term matching.

        Returns:
            Self for method chaining.
        """
        if blacklist is not None:
            self._matcher.blacklist_transformers = blacklist
        if whitelist is not None:
            self._matcher.whitelist_transformers = whitelist

        return self

    def censor(self, text: str) -> str:
        """
        Apply censoring to text.

        Args:
            text: Input text to censor.

        Returns:
            Censored text. Unchanged if no profanity found.
        """
        if not text:
            return text

        matches = self._matcher.get_all_matches(text)
        if not matches:
            return text

        return self._censor.apply_censor(text, matches)

    def has_match(self, text: str) -> bool:
        """
        Check if text contains profanity.

        Args:
            text: Input text to check.

        Returns:
            True if profanity found, False otherwise.
        """
        if not text:
            return False

        return self._matcher.has_match(text)

    def find_matches(self, text: str, include_metadata: bool = True) -> List[Match]:
        """
        Find all profanity matches in text.

        Args:
            text: Input text to analyze.
            include_metadata: Include phrase metadata (default: True).

        Returns:
            List of Match objects with details about each found profanity.
        """
        if not text:
            return []

        raw_matches = self._matcher.get_all_matches(text)
        if not raw_matches:
            return []

        results = []
        for match in raw_matches:
            matched_text = text[match.startIndex : match.endIndex]
            metadata = getattr(match, "phraseMetadata", None) if include_metadata else None

            results.append(
                Match(
                    start_index=match.startIndex,
                    end_index=match.endIndex,
                    match_length=match.matchLength,
                    matched_text=matched_text,
                    term_id=match.termId,
                    metadata=metadata,
                )
            )

        return results
