# misaki-ja-lightning ⚡

Lightweight Japanese text-to-IPA phoneme converter extracted from the [misaki](https://github.com/hexgrad/misaki) library. This package contains only the Japanese G2P (grapheme-to-phoneme) functionality with minimal dependencies.

## Features

- 🇯🇵 Convert Japanese text (hiragana, katakana, kanji) to IPA phonemes
- 🔢 Convert numbers to Japanese kana
- ⚡ Lightning-fast with minimal dependencies
- 🎯 Focused on Japanese language only
- 🔧 Uses `pyopenjtalk` for accurate phoneme conversion

## Installation

```bash
pip install misaki-ja-lightning
```

## Usage

### Basic G2P Conversion

```python
from misaki_ja_lightning import JAG2P

# Initialize the converter
g2p = JAG2P()

# Convert Japanese text to IPA phonemes
text = "こんにちは、世界"
phonemes, tokens = g2p(text)

print(phonemes)  # IPA phoneme string with pitch information
```

### Number to Kana Conversion

```python
from misaki_ja_lightning import Convert, ConvertKanji

# Convert Arabic numbers to Japanese
result = Convert(12345, 'hiragana')
print(result)  # いちまんにせんさんびゃくよんじゅうご

# Convert to kanji
result = Convert(12345, 'kanji')
print(result)  # 一万二千三百四十五

# Convert to romaji
result = Convert(12345, 'romaji')
print(result)  # ichi man ni sen san byaku yon juu go

# Supported formats: 'hiragana', 'kanji', 'romaji'
# Note: 'katakana' is not supported in num2kana module

# Convert kanji numbers back to Arabic
number = ConvertKanji("一万二千三百四十五")
print(number)  # 12345
```

### Token-level Processing

```python
from misaki_ja_lightning import JAG2P

g2p = JAG2P()
phonemes, tokens = g2p("今日は良い天気ですね")

for token in tokens:
    print(f"Text: {token.text}")
    print(f"Phonemes: {token.phonemes}")
    print(f"Tag: {token.tag}")
    print(f"Pitch: {token._.pitch}")
    print("---")
```

## What's Included

This lightweight package includes only:

- `ja.py` - Japanese G2P converter using pyopenjtalk
- `num2kana.py` - Number to Japanese kana converter
- `token.py` - Token data structure

## Differences from Original Misaki

- ✅ Japanese-only (removed other languages)
- ✅ Removed `cutlet` dependency
- ✅ Removed `addict` dependency
- ✅ Simplified token structure
- ✅ Only `pyopenjtalk` version (no cutlet option)
- ✅ Minimal dependencies

## Requirements

- Python >= 3.8
- pyopenjtalk (forked version with /tmp support for serverless environments)

**Note**: This package uses a forked version of pyopenjtalk that downloads the dictionary to `/tmp` instead of the package directory. This allows it to work in serverless environments like Vercel where the filesystem is read-only.

## License

MIT License (inherited from original misaki library)

## Credits

This package is extracted from [misaki](https://github.com/hexgrad/misaki) by hexgrad. All credit for the original implementation goes to the misaki authors.

The num2kana module is based on [Convert-Numbers-to-Japanese](https://github.com/Greatdane/Convert-Numbers-to-Japanese) by Greatdane (MIT License).

## Related Projects

- [misaki](https://github.com/hexgrad/misaki) - Full multilingual G2P library
- [Kokoro-82M](https://huggingface.co/hexgrad/Kokoro-82M) - Text-to-speech model
- [pyopenjtalk](https://github.com/r9y9/pyopenjtalk) - Japanese text processing

## Use Cases

Perfect for:
- Text-to-speech applications
- Japanese language learning tools
- Phoneme-based synthesis
- Lightweight Japanese text processing

## Support

For issues and questions, please visit the [GitHub Issues](https://github.com/yourusername/misaki-ja-lightning/issues) page.
