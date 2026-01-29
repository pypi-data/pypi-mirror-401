# pyobscenity

A Python port of the JavaScript library [obscenity](https://github.com/jo3-l/obscenity) for detecting and censoring obscene words in text.

**Note:** Due to the nature of this library, repository contents may be considered NSFW or offensive.

## Features

- **Simple API** - Censor profanity with a single function call
- **Multiple censoring strategies** - Full replacement, keep start/end, grawlix, fixed, random
- **Smart detection** - Handles case variations, leet speak, Unicode lookalikes
- **Language support** - Built-in English preset with 100+ phrases
- **Whitelist support** - Exclude specific terms from censoring
- **Reusable filters** - Build efficient, reusable filters for batch processing

## Quick Start

### Installation

```bash
pip install pyobscenity
```

### Basic Usage

```python
from pyobscenity import censor, check, find_matches

# Censor profanity
result = censor("This is fucking great!")
# "This is ****ing great!"

# Check if text contains profanity
if check(user_input):
    print("Please keep it clean!")

# Find all profanity matches
matches = find_matches("fuck this shit")
for match in matches:
    print(f"'{match.matched_text}' at position {match.start_index}")
```

**Note:** the default English filters are too aggressive for some use cases. Consider customizing the dataset or transformers for your needs. It is based on the original filter from the JavaScript library, with some minor adjustments.

## Common Use Cases

### Censor with Different Styles

```python
from pyobscenity import censor

# Default (full replacement with *)
censor("This is shit")  
# "This is ****"

# Custom character
censor("shit", censor_char="#")  
# "####"

# Keep first character as hint
censor("shit", censor_type="keep_start", keep_length=1)  
# "s***"

# Fixed replacement
censor("shit", censor_type="fixed", replacement="[REDACTED]")  
# "[REDACTED]"

# Grawlix (comic book style)
censor("shit", censor_type="grawlix")  
# "@#$%"
```

### Check and Find Matches

```python
from pyobscenity import check, find_matches

# Simple check
has_profanity = check("hello world")  # False
has_profanity = check("hello shit")   # True

# Get match details
matches = find_matches("fuck this shit")
for m in matches:
    print(f"'{m.matched_text}' at [{m.start_index}:{m.end_index}]")
```

### Custom Datasets

```python
from pyobscenity import Dataset, ProfanityFilter

# Define custom profanity
dataset = (
    Dataset()
    .add_phrase(lambda p: p
        .add_pattern("|badword|")
        .add_whitelisted_term("badwords")  # Don't censor this
    )
    .add_phrase(lambda p: p.add_pattern("|naughty|"))
)

filter = ProfanityFilter.custom(dataset)
result = filter.censor("This is a badword")  # Censored
result = filter.censor("These are badwords") # Not censored
```

## What Gets Detected?

The library detects:

- **Case variations**: `shit`, `SHIT`, `Shit`
- **Leet speak**: `sh1t`, `5h1t`
- **Unicode lookalikes**: `shiт` (with Cyrillic т)

These work automatically with the default English preset through intelligent text transformers.

# Advanced features: 

See [ADVANCED_USAGE.md](ADVANCED_USAGE.md) for:

  - Custom censoring strategies and transformers
  - Building domain-specific datasets
  - Low-level API access
  - Performance tuning
  - Architecture details