#!/usr/bin/env python3
"""
Example usage of misaki-ja-lightning
"""

from misaki_ja_lightning import JAG2P, Convert, ConvertKanji

def main():
    print("=" * 60)
    print("misaki-ja-lightning Example")
    print("=" * 60)

    # Initialize G2P converter
    g2p = JAG2P()

    # Example 1: Basic text conversion
    print("\n1. Basic Japanese Text to IPA:")
    print("-" * 60)
    text = "こんにちは、世界"
    phonemes, tokens = g2p(text)
    print(f"Input: {text}")
    print(f"Phonemes: {phonemes[:len(phonemes)//2]}")  # First half is phonemes
    print(f"Pitch: {phonemes[len(phonemes)//2:]}")     # Second half is pitch

    # Example 2: Token-level processing
    print("\n2. Token-level Processing:")
    print("-" * 60)
    text = "今日は良い天気です"
    phonemes, tokens = g2p(text)
    for token in tokens:
        if token.phonemes:
            print(f"  {token.text:8s} -> {token.phonemes:20s} (pitch: {token._.pitch if token._ else 'N/A'})")

    # Example 3: Number to Kana
    print("\n3. Number to Kana Conversion:")
    print("-" * 60)
    number = 12345
    print(f"  {number} -> {Convert(number, 'hiragana')} (hiragana)")
    print(f"  {number} -> {Convert(number, 'kanji')} (kanji)")
    print(f"  {number} -> {Convert(number, 'romaji')} (romaji)")

    # Try different numbers
    print(f"  {2024} -> {Convert(2024, 'hiragana')} (hiragana)")
    print(f"  {100} -> {Convert(100, 'kanji')} (kanji)")

    # Example 4: Kanji to Number
    print("\n4. Kanji to Number Conversion:")
    print("-" * 60)
    kanji = "一万二千三百四十五"
    number = ConvertKanji(kanji)
    print(f"  {kanji} -> {number}")

    # Example 5: Complex sentence
    print("\n5. Complex Sentence:")
    print("-" * 60)
    text = "2024年3月15日、東京で会議があります。"
    phonemes, tokens = g2p(text)
    print(f"Input: {text}")
    print(f"Phonemes: {phonemes[:len(phonemes)//2][:100]}...")

    print("\n" + "=" * 60)
    print("Example completed!")
    print("=" * 60)

if __name__ == "__main__":
    main()
