# Advanced Usage Guide

This guide covers advanced features, customization, and low-level API usage for power users.

## Table of Contents

- [Censor Types](#censor-types)
- [Text Transformers](#text-transformers)
- [Custom Datasets](#custom-datasets)
- [Low-Level API](#low-level-api)
- [Architecture](#architecture)
- [Performance Tuning](#performance-tuning)

## Censor Types

The library supports multiple censoring strategies. Choose based on your use case:

| Type | Example | Description | Use Case |
|------|---------|-------------|----------|
| `"full"` | `****` | Replace entire match (default) | General purpose |
| `"keep_start"` | `s***` | Keep N characters from start | Hint at original word |
| `"keep_end"` | `***t` | Keep N characters from end | Hint at original word |
| `"fixed"` | `[REDACTED]` | Replace with fixed string | Consistent replacement |
| `"random"` | `@#$%` | Replace with random characters | Varied appearance |
| `"grawlix"` | `@#$%` | Comic book-style symbols | Playful tone |

### Examples

```python
from pyobscenity import censor

# Keep first character as a hint
result = censor("shit", censor_type="keep_start", keep_length=1)
# Output: "s***"

# Keep last character
result = censor("shit", censor_type="keep_end", keep_length=2)
# Output: "**it"

# Use descriptive replacement
result = censor("shit", censor_type="fixed", replacement="[REDACTED]")
# Output: "[REDACTED]"

# Use grawlix for fun
result = censor("shit", censor_type="grawlix")
# Output: "@#$%"
```

## Text Transformers

Text transformers normalize variations in text before pattern matching. This allows detection of:

- **Case variations**: `shit`, `SHIT`, `Shit`
- **Leet speak**: `sh1t`, `5h1t`, `sh@t`
- **Unicode confusables**: `shiт` (Cyrillic т)

### Available Transformers

- **LowercaseTransformer** - Normalize to lowercase
- **ResolveConfusablesTransformer** - Convert Unicode lookalikes (е→e, А→a, etc.)
- **ResolveLeetTransformer** - Convert leet speak (4→a, 3→e, @→a, etc.)
- **CollapseDuplicateTransformer** - Reduce repeated characters with configurable thresholds
- **SkipNonAlphaTransformer** - Remove non-alphabetic characters
- **RemapCharacterTransformer** - Custom character mapping

### Using Custom Transformers

```python
from pyobscenity import ProfanityFilter, LowercaseTransformer, SkipNonAlphaTransformer

# Create filter with custom transformers
filter = (
    ProfanityFilter.english()
    .with_transformers(
        blacklist=[LowercaseTransformer(), SkipNonAlphaTransformer()],
        whitelist=[LowercaseTransformer()]
    )
)

# Now matches text with removed spaces/punctuation
result = filter.censor("shit!")  # Won't match because ! is removed by transformer
```

**Note**: The default English preset's `CollapseDuplicateTransformer` has limits configured for specific characters. Excessive duplicates like "shhhhhit" may not be detected depending on threshold settings.

## Custom Datasets

Beyond the built-in English preset, you can create custom datasets for:

- Domain-specific profanity
- Multiple languages
- Custom patterns

### Creating a Custom Dataset

```python
from pyobscenity import Dataset, ProfanityFilter

# Define your phrases with patterns
dataset = (
    Dataset()
    .add_phrase(lambda p: p
        .set_metadata({"originalWord": "badword", "severity": "high"})
        .add_pattern("|badword|")  # Word boundary pattern
        .add_whitelisted_term("badwords")  # Don't censor "badwords" (plural)
        .add_whitelisted_term("badwording")  # Don't censor gerund
    )
    .add_phrase(lambda p: p
        .set_metadata({"originalWord": "naughty", "severity": "medium"})
        .add_pattern("|naughty|")
    )
    .add_phrase(lambda p: p
        .set_metadata({"originalWord": "offensive", "severity": "high"})
        .add_pattern("offensive")  # No word boundaries
        .add_pattern("|offended|")  # Alternative pattern
    )
)

filter = ProfanityFilter.custom(dataset)
result = filter.censor("This is a badword")  # Censored
result = filter.censor("These are badwords")  # Not censored (whitelisted)
```

### Pattern Syntax

Patterns support a custom DSL:

- `|word|` - Word boundary (space or punctuation on both sides)
- `[optional]` - Optional character
- `*` - Wildcard (any characters)
- Plain text - Literal match

Examples:
```python
# Word boundary on both sides
.add_pattern("|anal|")

# Optional 's' at end (for singular/plural)
.add_pattern("|ass[s]|")

# Wildcard for any characters between
.add_pattern("ab*cd")

# No word boundary (matches within words)
.add_pattern("shit")
```

### Using Custom Transformers with Custom Datasets

```python
from pyobscenity import Dataset, ProfanityFilter, LowercaseTransformer, ResolveLeetTransformer

dataset = Dataset().add_phrase(lambda p: p
    .set_metadata({"originalWord": "customword"})
    .add_pattern("|customword|")
)

filter = (
    ProfanityFilter.custom(dataset)
    .with_transformers(
        blacklist=[LowercaseTransformer(), ResolveLeetTransformer()],
        whitelist=[LowercaseTransformer()]
    )
)
```

## Low-Level API

For maximum control, use the low-level components directly:

```python
from pyobscenity import (
    RegexMatcher,
    FullCensor,
    LowercaseTransformer,
    english_dataset,
    english_recommended_blacklist_transformers,
)

# 1. Build dataset
dataset = english_dataset.build()

# 2. Create matcher with custom configuration
matcher = RegexMatcher(
    blacklisted_terms=dataset["blacklisted_terms"],
    whitelisted_terms=dataset["whitelisted_terms"],
    blacklist_transformers=english_recommended_blacklist_transformers,
    whitelist_transformers=[LowercaseTransformer()],
)

# 3. Get matches
text = "hello shit world"
matches = matcher.get_all_matches(text)

# 4. Create censor with specific strategy
censor = FullCensor("*")

# 5. Apply censoring
result = censor.apply_censor(text, matches)
```

### Available Components

**Matchers:**
- `RegexMatcher` - Regex-based pattern matching with transformer pipeline

**Censors:**
- `FullCensor(char)` - Replace with character
- `KeepStartCensor(length, char)` - Keep N chars from start
- `KeepEndCensor(length, char)` - Keep N chars from end
- `FixedCensor(replacement)` - Fixed string replacement
- `RandomCharCensor(chars)` - Random character replacement
- `GrawlixCensor()` - Comic book symbols

**Transformers:**
- `LowercaseTransformer()`
- `SkipNonAlphaTransformer()`
- `CollapseDuplicateTransformer(default_limit, char_limits)`
- `RemapCharacterTransformer(char_map)`
- `ResolveConfusablesTransformer()`
- `ResolveLeetTransformer()`

## Architecture

```
Input Text
    ↓
[Text Transformers] - Normalize variations (leet, Unicode, duplicates)
    ↓
[Pattern Matcher] - Check against blacklist/whitelist with transformations
    ↓
[Match Results] - List of MatchPayload objects with positions
    ↓
[Censor Strategy] - Apply censoring strategy to matched regions
    ↓
Output Text
```

### Match Resolution

When overlapping matches are found:

1. Matches are sorted by position and duration
2. For overlaps, shorter matches are resolved based on term ID ordering
3. Censoring is applied sequentially to avoid double-censoring

## Performance Tuning

### Caching Strategy

The convenience API (`censor()`, `check()`, `find_matches()`) caches the default matcher globally:

```python
# First call creates and caches matcher
censor("hello shit")  # Creates matcher

# Subsequent calls reuse cached matcher
censor("hello fuck")  # Reuses cached matcher
```

**Use simple API when:**
- Processing one or two texts
- Different configurations each time
- Want lowest memory footprint

### Reusable Filters Strategy

For batch processing, create a filter instance once:

```python
from pyobscenity import ProfanityFilter

# Create once
filter = ProfanityFilter.english().with_censor("fixed", replacement="***")

# Reuse many times
results = [filter.censor(text) for text in 1000_texts]
```

**Benchmark comparison:**
```python
import timeit

texts = ["shit", "fuck", "damn"] * 100

# Simple API (creates matcher each time)
time1 = timeit.timeit(
    lambda: [censor(t) for t in texts],
    number=10
)

# Reusable filter (reuses matcher)
filter = ProfanityFilter.english()
time2 = timeit.timeit(
    lambda: [filter.censor(t) for t in texts],
    number=10
)

print(f"Simple API: {time1:.3f}s")  # Slower
print(f"Reusable Filter: {time2:.3f}s")  # Faster
```

### Memory Optimization

- **Small inputs**: Use simple API (`censor()`)
- **Batch processing**: Use reusable `ProfanityFilter`
- **Multiple filters**: Consider sharing dataset between filters
- **Large datasets**: Use custom datasets with only needed phrases

### Threading

Filter instances are thread-safe for reading but not for configuration changes:

```python
from concurrent.futures import ThreadPoolExecutor
from pyobscenity import ProfanityFilter

filter = ProfanityFilter.english()

def process_text(text):
    return filter.censor(text)  # Safe - reading only

# Safe to use in threads
with ThreadPoolExecutor(max_workers=4) as executor:
    results = list(executor.map(process_text, texts))
```

## Troubleshooting

### Pattern not matching

Check:
1. **Case**: Patterns are lowercased by transformer. Use `LowercaseTransformer` in blacklist transformers.
2. **Word boundaries**: `|word|` requires space/punctuation around. Use plain `word` for substring matching.
3. **Transformers**: Verify transformers are stripping/converting expected variations.

### Performance issues

1. **Check caching**: Use reusable `ProfanityFilter` for batch operations
2. **Reduce transformers**: Only use transformers you need
3. **Profile**: Use Python's `cProfile` to identify bottlenecks
4. **Dataset size**: Custom dataset with fewer phrases will be faster

### Unexpected matches

1. **Whitelisting**: Add `add_whitelisted_term()` to phrase builder
2. **Pattern specificity**: Use `|word|` for word boundaries
3. **Transformer effects**: Test transformers individually to see effects
