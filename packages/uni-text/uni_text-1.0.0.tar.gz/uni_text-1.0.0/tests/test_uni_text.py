import json
from pathlib import Path

import pytest
from uni_text import UniText

REPO_ROOT = Path(__file__).resolve().parents[3]
REMOVE_PUNCT_FIXTURE = REPO_ROOT / "shared_testdata" / "uni-text" / "remove-punctuations.json"

with REMOVE_PUNCT_FIXTURE.open(encoding="utf-8") as fixture_file:
    REMOVE_PUNCT_CASES = json.load(fixture_file)


@pytest.mark.parametrize(
    "case",
    REMOVE_PUNCT_CASES,
    ids=[case["id"] for case in REMOVE_PUNCT_CASES],
)
def test_remove_punctuations_matches_fixture(case):
    assert UniText.remove_punctuations(case["input"]) == case["expected"]


@pytest.mark.parametrize(
    ("char", "expected"),
    [
        (".", True),
        ("！", True),
        ("…", True),
        ("a", False),
        ("", False),
        ("..", False),
    ],
)
def test_is_punctuation_behaviour(char: str, expected: bool):
    assert UniText.is_punctuation(char) is expected


def test_remove_consecutive_punctuations_collapses_sequences():
    assert UniText.remove_consecutive_punctuations("你好，，，世界！！？。") == "你好，世界！"
    assert UniText.remove_consecutive_punctuations("Mix...?!") == "Mix."


def test_is_cjk_character_range():
    assert UniText.is_cjk_character(ord("你")) is True
    assert UniText.is_cjk_character(ord("あ")) is True
    assert UniText.is_cjk_character(ord("한")) is True
    assert UniText.is_cjk_character(ord("A")) is False


def test_is_sentence_end_with_punctuation():
    assert UniText.is_sentence_end_with_punctuation("结束。") is True
    assert UniText.is_sentence_end_with_punctuation("end?") is True
    assert UniText.is_sentence_end_with_punctuation("終わり？") is True
    assert UniText.is_sentence_end_with_punctuation("끝...") is True
    assert UniText.is_sentence_end_with_punctuation("hello") is False
