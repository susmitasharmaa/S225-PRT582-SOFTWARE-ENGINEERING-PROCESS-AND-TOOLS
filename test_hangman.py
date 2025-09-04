"""
Unit tests for HangmanEngine using Pytest.
"""


from hangman import HangmanEngine


def test_word_generated_basic():
    """Check that a basic word is picked correctly."""
    g = HangmanEngine(words=["hello"], level="basic")
    g.reset()
    assert g.answer == "hello"


def test_phrase_generated_intermediate():
    """Check that an intermediate phrase is picked correctly."""
    g = HangmanEngine(phrases=["good day"], level="intermediate")
    g.reset()
    assert g.answer == "good day"


def test_correct_guess_reveals():
    """Test that a correct guess reveals letters."""
    g = HangmanEngine(words=["hello"], level="basic")
    g.reset()
    res, _ = g.guess("h")
    assert res is True
    assert g.revealed.startswith("h")


def test_incorrect_guess_loses_life():
    """Test that an incorrect guess reduces lives by 1."""
    g = HangmanEngine(words=["hello"], lives=3, level="basic")
    g.reset()
    res, _ = g.guess("z")
    assert res is False
    assert g.remaining_lives == 2


def test_game_won():
    """Test winning condition when all letters guessed."""
    g = HangmanEngine(words=["hi"], level="basic")
    g.reset()
    g.guess("h")
    g.guess("i")
    assert g.is_won() is True


def test_game_lost():
    """Test losing condition when lives run out."""
    g = HangmanEngine(words=["hi"], lives=1, level="basic")
    g.reset()
    _ = g.guess("z")
    assert g.is_lost() is True


def test_timeout_deducts_life():
    """Test that timeout deducts one life."""
    g = HangmanEngine(words=["hello"], lives=2, level="basic")
    g.reset()
    g.timed_out()
    assert g.remaining_lives == 1
