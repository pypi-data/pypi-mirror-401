"""
Unicode Text Processing Module

Provides utilities for text processing, including punctuation detection,
punctuation removal, and CJK character detection.
"""

import logging
import sys
import unicodedata
from collections import OrderedDict

logger = logging.getLogger(__name__)


class UniText:
    """
    Utility class for Unicode text processing.

    All methods are static and provide a simple interface for working with
    text data, including punctuation handling and CJK character detection.
    """

    # Unified sentence-ending punctuation set to support multi-language text
    SENTENCE_END_PUNCTUATIONS = {
        "。",  # Full-width period used in CJK sentences
        "？",  # Full-width question mark
        "！",  # Full-width exclamation mark
        "；",  # Full-width semicolon
        "…",  # Single-character ellipsis
        "……",  # Six-dot ellipsis frequently used in CJK
        ".",  # ASCII period
        "?",  # ASCII question mark
        "!",  # ASCII exclamation mark
        ";",  # ASCII semicolon
        "...",  # Three-dot ellipsis
    }

    # Hyphen/dash variants that should be preserved
    HYPHEN_CHARS = {
        "-",  # hyphen-minus
        "‐",  # hyphen
        "‑",  # non-breaking hyphen
        "‒",  # figure dash
        "–",  # en dash
        "—",  # em dash
        "―",  # horizontal bar
        "﹘",  # small em dash
        "﹣",  # small minus
        "－",  # fullwidth hyphen-minus
        "−",  # minus sign
    }

    # Arithmetic symbols to preserve
    ARITHMETIC_SIGNS = {
        "+",  # Addition sign
        "＋",  # Full-width addition sign
        "±",  # Plus-minus sign
        "∓",  # Minus-plus sign
        "×",  # Multiplication sign
        "✕",  # Heavy multiplication X
        "✖",  # Multiplication X symbol
        "÷",  # Division sign
        "∕",  # Division slash
        "·",  # Middle dot used in math expressions
        "∙",  # Bullet operator
    }

    # Greek numeral markers
    GREEK_NUMERAL_SIGNS = {
        "ʹ",  # U+02B9 modifier letter prime (used interchangeably)
        "ˈ",  # U+02C8 modifier letter vertical line
        "ʹ",  # U+0374 greek numeral sign
        "͵",  # U+0375 greek lower numeral sign
        "·",  # U+00B7 middle dot (also used as άνω τελεία)
        "·",  # U+0387 greek ano teleia
    }

    # Currency symbols to preserve (all Unicode Sc category)
    CURRENCY_SIGNS = frozenset(chr(code_point) for code_point in range(sys.maxunicode + 1) if unicodedata.category(chr(code_point)) == "Sc")

    # Simple LRU caches for expensive operations
    _REMOVE_PUNCT_CACHE: "OrderedDict[str, str]" = OrderedDict()
    _SENTENCE_END_CACHE: "OrderedDict[str, bool]" = OrderedDict()
    _CACHE_MAX_SIZE = 2048

    @staticmethod
    def _is_word_char(char: str) -> bool:
        """Check if character is a Unicode letter or digit."""
        if not char:
            return False
        category = unicodedata.category(char)
        return category.startswith("L") or category.startswith("N")

    @staticmethod
    def is_punctuation(char: str) -> bool:
        """
        Check if a character is a punctuation mark.

        Uses Unicode category to determine punctuation. All categories starting
        with "P" are considered punctuation.

        Args:
            char: Character to check.

        Returns:
            bool: True if the character is punctuation, False otherwise.
        """
        if not char or len(char) != 1:
            return False
        return unicodedata.category(char).startswith("P")

    @staticmethod
    def remove_punctuations(text: str) -> str:
        """
        Remove punctuation marks from text.

        Uses Unicode category to remove punctuation, but preserves the following
        special cases:
        - Apostrophes (') in English contractions and possessives, e.g., "don't", "John's", "workers'"
        - Percent signs (%)
        - Hyphens/dashes (包含 Unicode 破折号)
        - Thousand separators (,) when surrounded by digits
        - Decimal points (.) when used in numbers, e.g., "99.5", "3.14", ".5"
        - Arithmetic symbols (+, ±, ×, ÷ 等)
        - Slashes (/) when used in dates, fractions, or units, e.g., "2024/01/01", "1/2", "km/h"

        Args:
            text: Original text (may contain punctuation).

        Returns:
            str: Text with punctuation removed (special characters preserved).
        """
        if not text:
            return text

        cached = UniText._get_cached_result(UniText._REMOVE_PUNCT_CACHE, text)
        if cached is not None:
            return cached

        normalized_text = unicodedata.normalize("NFKC", text)
        if not normalized_text:
            return normalized_text

        decimal_separator = UniText._detect_decimal_separator(normalized_text)
        result = []
        length = len(normalized_text)

        for i, char in enumerate(normalized_text):
            original_char = text[i] if i < len(text) else char

            if not UniText.is_punctuation(char):
                result.append(original_char)
                continue

            if char == "'":
                if UniText._should_keep_apostrophe(normalized_text, i):
                    result.append(original_char)
                continue

            if char in {".", ","}:
                if UniText._should_keep_decimal_separator(normalized_text, i, char, decimal_separator):
                    result.append(original_char)
                    continue
                if UniText._should_keep_grouping_separator(normalized_text, i, char):
                    result.append(original_char)
                continue

            if char == "/":
                if UniText._should_keep_slash(normalized_text, i):
                    result.append(original_char)
                continue

            if char == "%":
                result.append(original_char)
                continue

            if char in UniText.HYPHEN_CHARS or char in UniText.ARITHMETIC_SIGNS or char in UniText.GREEK_NUMERAL_SIGNS or char in UniText.CURRENCY_SIGNS:
                result.append(original_char)
                continue

        cleaned = "".join(result)
        UniText._cache_result(UniText._REMOVE_PUNCT_CACHE, text, cleaned)
        return cleaned

    @staticmethod
    def remove_consecutive_punctuations(text: str) -> str:
        """
        Remove consecutive punctuation marks, keeping only the first one.

        Uses `is_punctuation()` to detect punctuation. When consecutive punctuation
        marks are encountered (regardless of whether they are the same), only the
        first one is kept, and all subsequent consecutive punctuation marks are removed.

        Examples:
            "你好，，，世界" -> "你好，世界"
            "这是。。。测试" -> "这是。测试"
            "多个！！！感叹号" -> "多个！感叹号"
            "混合，。，。标点" -> "混合，标点" (keep first punctuation, remove subsequent consecutive punctuation)
            "测试！？。结束" -> "测试！结束" (keep first punctuation, remove subsequent consecutive punctuation)

        Args:
            text: Original text (may contain repeated punctuation).

        Returns:
            str: Text with consecutive punctuation removed.
        """
        if not text:
            return text

        result = []
        prev_is_punc = False

        for char in text:
            is_punc = UniText.is_punctuation(char)

            # If current character is punctuation and previous character is also punctuation, skip (regardless of whether they are the same)
            if is_punc and prev_is_punc:
                continue

            # Otherwise add to result
            result.append(char)
            prev_is_punc = is_punc

        return "".join(result)

    @staticmethod
    def is_cjk_character(code_point: int) -> bool:
        """
        Check if a Unicode code point is a CJK character.

        CJK character ranges include:
        - CJK Unified Ideographs: 0x4E00-0x9FFF
        - CJK Extension A: 0x3400-0x4DBF
        - CJK Extension B: 0x20000-0x2A6DF
        - CJK Extension C: 0x2A700-0x2B73F
        - CJK Extension D: 0x2B740-0x2B81F
        - CJK Extension E: 0x2B820-0x2CEAF
        - CJK Extension F: 0x2CEB0-0x2EBEF
        - CJK Extension G: 0x30000-0x3134F
        - CJK Extension H: 0x31350-0x323AF
        - CJK Extension I: 0x2EBF0-0x2EE5F
        - CJK Compatibility Ideographs: 0xF900-0xFAFF
        - CJK Compatibility Ideographs Supplement: 0x2F800-0x2FA1F
        - Hiragana: 0x3040-0x309F
        - Katakana: 0x30A0-0x30FF
        - Hangul Syllables: 0xAC00-0xD7AF
        - Bopomofo (Zhuyin): 0x3100-0x312F

        Args:
            code_point: Unicode code point (integer).

        Returns:
            bool: True if the code point is a CJK character, False otherwise.
        """
        return (
            (0x4E00 <= code_point <= 0x9FFF)  # CJK Unified Ideographs
            or (0x3400 <= code_point <= 0x4DBF)  # CJK Extension A
            or (0x20000 <= code_point <= 0x2A6DF)  # CJK Extension B
            or (0x2A700 <= code_point <= 0x2B73F)  # CJK Extension C
            or (0x2B740 <= code_point <= 0x2B81F)  # CJK Extension D
            or (0x2B820 <= code_point <= 0x2CEAF)  # CJK Extension E
            or (0x2CEB0 <= code_point <= 0x2EBEF)  # CJK Extension F
            or (0x30000 <= code_point <= 0x3134F)  # CJK Extension G
            or (0x31350 <= code_point <= 0x323AF)  # CJK Extension H
            or (0x2EBF0 <= code_point <= 0x2EE5F)  # CJK Extension I
            or (0xF900 <= code_point <= 0xFAFF)  # CJK Compatibility Ideographs
            or (0x2F800 <= code_point <= 0x2FA1F)  # CJK Compatibility Ideographs Supplement
            or (0x3040 <= code_point <= 0x309F)  # Hiragana
            or (0x30A0 <= code_point <= 0x30FF)  # Katakana
            or (0xAC00 <= code_point <= 0xD7AF)  # Hangul Syllables
            or (0x3100 <= code_point <= 0x312F)  # Bopomofo (Zhuyin)
        )

    @staticmethod
    def is_sentence_end_with_punctuation(text: str) -> bool:
        """
        Check if text ends with sentence-ending punctuation (language-agnostic).

        Uses a unified punctuation set to support mixed-language content without
        requiring the caller to specify language type.

        Args:
            text: Text to check (can be a single character or multiple characters, e.g., "段。", "end.")

        Returns:
            bool: True if text ends with sentence-ending punctuation, False otherwise.
        """
        if not text:
            return False

        cached = UniText._get_cached_result(UniText._SENTENCE_END_CACHE, text)
        if cached is not None:
            return cached

        normalized_text = unicodedata.normalize("NFKC", text)
        for punct in UniText.SENTENCE_END_PUNCTUATIONS:
            if normalized_text.endswith(punct):
                UniText._cache_result(UniText._SENTENCE_END_CACHE, text, True)
                return True

        UniText._cache_result(UniText._SENTENCE_END_CACHE, text, False)
        return False

    @staticmethod
    def _get_cached_result(cache: "OrderedDict[str, object]", key: str):
        cached = cache.get(key)
        if cached is not None:
            cache.move_to_end(key)
        return cached

    def _should_keep_apostrophe(text: str, index: int) -> bool:
        if index == 0:
            return False

        prev_char = text[index - 1]
        if not UniText._is_word_char(prev_char):
            return False

        next_char = text[index + 1] if index < len(text) - 1 else ""

        if next_char and next_char.isalpha():
            return True

        return index == len(text) - 1 or (next_char and next_char.isspace()) or (next_char and UniText.is_punctuation(next_char))

    @staticmethod
    def _should_keep_decimal_separator(text: str, index: int, char: str, decimal_separator: str | None) -> bool:
        use_char_as_decimal = decimal_separator == char or (decimal_separator is None and char == ".")
        if not use_char_as_decimal:
            return False

        length = len(text)
        prev_char = text[index - 1] if index > 0 else ""
        next_char = text[index + 1] if index < length - 1 else ""
        prev_is_space = bool(prev_char) and prev_char.isspace()
        next_is_space = bool(next_char) and next_char.isspace()

        if prev_char.isdigit() and next_char.isdigit():
            return True

        if prev_char.isdigit() and (index == length - 1 or next_is_space):
            return True

        if not prev_char and next_char.isdigit():
            return True

        if index > 0 and index < length - 1 and next_char.isdigit() and (prev_is_space or (prev_char and UniText.is_punctuation(prev_char))):
            return True

        return False

    @staticmethod
    def _should_keep_slash(text: str, index: int) -> bool:
        if index <= 0 or index >= len(text) - 1:
            return False
        return UniText._is_word_char(text[index - 1]) and UniText._is_word_char(text[index + 1])

    @staticmethod
    def _cache_result(cache: "OrderedDict[str, object]", key: str, value: object) -> None:
        cache[key] = value
        cache.move_to_end(key)
        if len(cache) > UniText._CACHE_MAX_SIZE:
            cache.popitem(last=False)

    @staticmethod
    def _should_keep_grouping_separator(text: str, index: int, separator: str) -> bool:
        """
        Decide whether a separator acts as a thousands grouping char (e.g., comma in 1,234).
        """
        if index <= 0 or index >= len(text) - 1:
            return False

        prev_char = text[index - 1]
        next_char = text[index + 1]

        if not prev_char.isdigit() or not next_char.isdigit():
            return False

        digits_to_left = 0
        for i in range(index - 1, -1, -1):
            char = text[i]
            if char.isdigit():
                digits_to_left += 1
            elif char == separator:
                break
            elif char.isspace():
                continue
            else:
                break

        if digits_to_left == 0 or digits_to_left > 3:
            return False

        digits_to_right = 0
        for i in range(index + 1, len(text)):
            char = text[i]
            if char.isdigit():
                digits_to_right += 1
            elif char == separator:
                break
            elif char.isspace():
                continue
            else:
                break

        return digits_to_right == 3

    @staticmethod
    def _detect_decimal_separator(text: str) -> str | None:
        """
        Detect likely decimal separator by scanning for '.' or ',' near the end.
        """
        candidates = []
        for separator in (".", ","):
            idx = text.rfind(separator)
            while idx != -1:
                if idx == 0 or idx >= len(text) - 1:
                    idx = text.rfind(separator, 0, idx)
                    continue
                if not text[idx - 1].isdigit():
                    idx = text.rfind(separator, 0, idx)
                    continue
                digits_after = 0
                for char in text[idx + 1 :]:
                    if char.isdigit():
                        digits_after += 1
                    elif char.isspace():
                        continue
                    else:
                        break
                if 0 < digits_after <= 3:
                    candidates.append((idx, separator))
                    break
                idx = text.rfind(separator, 0, idx)

        if not candidates:
            return None

        candidates.sort(key=lambda item: item[0], reverse=True)
        return candidates[0][1]
