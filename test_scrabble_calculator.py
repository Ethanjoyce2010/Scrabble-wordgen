import pytest
from scrabble calculator import calculate_max_score, find_best_placement, is_word_possible, LANGUAGE_CONFIGS

def test_calculate_max_score_basic():
    # Test a simple word with default multipliers
    word = "QUIZ"
    letter_values = LANGUAGE_CONFIGS["English"]["letter_values"]
    assert calculate_max_score(word, letter_values) == 10 + 1 + 1 + 10  # Q+U+I+Z

def test_calculate_max_score_with_multipliers():
    word = "QUIZ"
    letter_values = LANGUAGE_CONFIGS["English"]["letter_values"]
    letter_multipliers = [2, 1, 1, 3]  # Double Q, Triple Z
    word_multiplier = 2
    expected = (10*2 + 1*1 + 1*1 + 10*3) * 2
    assert calculate_max_score(word, letter_values, letter_multipliers, word_multiplier) == expected

def test_find_best_placement():
    word = "JAZZ"
    config = LANGUAGE_CONFIGS["English"]
    max_score, letter_mults, word_mult = find_best_placement(word, config)
    # Should return a positive score and valid multipliers
    assert max_score > 0
    assert len(letter_mults) == len(word)
    assert word_mult in (1, 2, 3, 6)

def test_is_word_possible_true():
    word = "QUIZ"
    config = LANGUAGE_CONFIGS["English"]
    assert is_word_possible(word, config) is True

def test_is_word_possible_false():
    word = "ZZZZZZZZZZZZZZZ"  # 15 Z's, only 1 in English
    config = LANGUAGE_CONFIGS["English"]
    assert is_word_possible(word, config) is False