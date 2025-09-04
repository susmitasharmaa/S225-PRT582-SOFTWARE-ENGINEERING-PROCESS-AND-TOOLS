import pytest
from hangman import HangmanEngine

# Check if a word is picked correctly when using "basic" mode
def test_word_generated_basic():
    g = HangmanEngine(words=["hello"], level="basic")
    g.reset()
    assert g.answer == "hello"

# Check if a phrase is picked correctly when using "intermediate" mode
def test_phrase_generated_intermediate():
    g = HangmanEngine(phrases=["good day"], level="intermediate")
    g.reset()
    assert g.answer == "good day"

# Guessing a correct letter should reveal part of the word
def test_correct_guess_reveals():
    g = HangmanEngine(words=["hello"], level="basic")
    g.reset()
    res, msg = g.guess("h")
    assert res is True
    assert g.revealed.startswith("h")  # the word should now start with "h"

# Guessing a wrong letter should reduce the number of lives
def test_incorrect_guess_loses_life():
    g = HangmanEngine(words=["hello"], lives=3, level="basic")
    g.reset()
    res, msg = g.guess("z")
    assert res is False
    assert g.remaining_lives == 2  # one life should be lost

# Winning condition: all letters guessed correctly
def test_game_won():
    g = HangmanEngine(words=["hi"], level="basic")
    g.reset()
    g.guess("h")
    g.guess("i")
    assert g.is_won() is True

# Losing condition: lives run out after wrong guesses
def test_game_lost():
    g = HangmanEngine(words=["hi"], lives=1, level="basic")
    g.reset()
    g.guess("z")  # wrong guess immediately ends the game
    assert g.is_lost() is True

# Timeout should deduct one life
def test_timeout_deducts_life():
    g = HangmanEngine(words=["hello"], lives=2, level="basic")
    g.reset()
    g.timed_out()
    assert g.remaining_lives == 1
