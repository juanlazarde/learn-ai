#!/usr/bin/env python3
"""
clean-output.py — Post-processing for Skiller output files.
Strips invisible characters and normalizes common AI text aberrations
before files are delivered to inbox/.

Usage:
    python clean-output.py <file> [file2 ...]

Exit codes:
    0 — success (changes made or file already clean)
    1 — file not found or read error
"""

import sys
import re
import unicodedata

# (bad_char, replacement) — order matters: run invisible removals before space normalization
REPLACEMENTS = [
    # Invisible / zero-width characters — remove entirely
    ('\u200b', ''),   # zero-width space
    ('\u200c', ''),   # zero-width non-joiner
    ('\u200d', ''),   # zero-width joiner
    ('\u200e', ''),   # left-to-right mark
    ('\u200f', ''),   # right-to-left mark
    ('\u2060', ''),   # word joiner
    ('\ufeff', ''),   # BOM / zero-width no-break space
    ('\u00ad', ''),   # soft hyphen
    # Non-standard spaces — normalize to regular space
    ('\u00a0', ' '),  # non-breaking space
    ('\u202f', ' '),  # narrow no-break space
    ('\u2009', ' '),  # thin space
    ('\u2007', ' '),  # figure space
    ('\u2008', ' '),  # punctuation space
    # Em dash and relatives — normalize to spaced hyphen
    ('\u2014', ' - '),  # em dash
    ('\u2013', '-'),    # en dash
    ('\u2012', '-'),    # figure dash
    ('\u2015', '-'),    # horizontal bar
    # Smart / curly quotes — normalize to straight quotes
    ('\u201c', '"'),  # left double quotation mark
    ('\u201d', '"'),  # right double quotation mark
    ('\u2018', "'"),  # left single quotation mark
    ('\u2019', "'"),  # right single quotation mark
    ('\u201a', "'"),  # single low-9 quotation mark
    ('\u201e', '"'),  # double low-9 quotation mark
    # Ellipsis
    ('\u2026', '...'),  # horizontal ellipsis
    # Other common aberrations
    ('\u2022', '-'),    # bullet (outside markdown lists it appears as raw unicode)
    ('\u00b7', '-'),    # middle dot
    ('\u2032', "'"),    # prime (often misused as apostrophe)
    ('\u2033', '"'),    # double prime (often misused as quotation mark)
]


def clean_text(text: str) -> tuple[str, list[str]]:
    """Apply all replacements and return (cleaned_text, list_of_change_descriptions)."""
    changes = []
    for bad, good in REPLACEMENTS:
        count = text.count(bad)
        if count:
            try:
                char_name = unicodedata.name(bad)
            except ValueError:
                char_name = f'U+{ord(bad):04X}'
            replacement_repr = repr(good) if good else 'removed'
            changes.append(
                f'  {count}x {char_name} ({repr(bad)}) -> {replacement_repr}'
            )
            text = text.replace(bad, good)

    # Collapse runs of 3+ blank lines down to 2
    cleaned, subs = re.subn(r'\n{3,}', '\n\n', text)
    if subs:
        changes.append(f'  Collapsed {subs} run(s) of excessive blank lines')
    text = cleaned

    return text, changes


def process_file(path: str) -> bool:
    """Clean a single file in place. Returns True on success."""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            original = f.read()
    except FileNotFoundError:
        print(f'ERROR: File not found: {path}', file=sys.stderr)
        return False
    except OSError as e:
        print(f'ERROR: Could not read {path}: {e}', file=sys.stderr)
        return False

    cleaned, changes = clean_text(original)

    if changes:
        try:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(cleaned)
        except OSError as e:
            print(f'ERROR: Could not write {path}: {e}', file=sys.stderr)
            return False
        print(f'Cleaned: {path}')
        for c in changes:
            print(c)
    else:
        print(f'Clean:   {path} (no changes needed)')

    return True


def main():
    if len(sys.argv) < 2:
        print('Usage: clean-output.py <file> [file2 ...]', file=sys.stderr)
        sys.exit(1)

    all_ok = all(process_file(path) for path in sys.argv[1:])
    sys.exit(0 if all_ok else 1)


if __name__ == '__main__':
    main()
