"""
Hangman game engine module.
Includes HangmanEngine class for game logic/guess handling/lives/timers.
"""

import random
import threading


class HangmanEngine:  # pylint: disable=too-many-instance-attributes,too-many-arguments,too-many-positional-arguments
    """Game logic game engine class of Hangman game."""

    def __init__(self, words=None, phrases=None, lives=6, time_limit=15, level="basic"):
        """
        Initialize the game engine.

    param words: single words for basic mode
        param phrases: intermediate mode multi-word phrases list.
        param lives: amount of incorrect guesses allowed.
        param time_limit seconds per guess
        param level: basic or intermediate
        """
        self.words = words or ["python", "hangman", "testing", "pytest", "unittest"]
        self.phrases = phrases or ["open ai", "machine learning", "unit testing"]
        self.lives = lives
        self.time_limit = time_limit
        self.level = level
        self.answer = None
        self.guessed = set()
        self.remaining_lives = self.lives
        self.revealed = None
        self._timeout_flag = False
        self._timer = None
        self.reset()
    def reset(self):
        """Clear the playing field , a new round begins."""
        if self.level == "basic":
            self.answer = random.choice(self.words)
        else:
            self.answer = random.choice(self.phrases)


        self.answer = random.choice(self.words if self.level == "basic" else self.phrases)
        self.guessed = set()               # letters already guessed
        self.remaining_lives = self.lives  # lives remaining
        self.revealed = self._mask_word()  # masked word/phrase
        self._timeout_flag = False         # timeout tracker
        self._timer = None                 # threading.Timer instance


    def _mask_word(self):
        """Give back the existing masked word/phrase beside 
        the letters that have been gussed back. """
        return "".join(
            c if c == " " or c.lower() in self.guessed else "_"
            for c in self.answer
        )

    def start_timer(self, on_timeout_callback):
        """
        Begin countdown timer to make a guess.

        param on timeout callback:call to make in case of time expiry.
        """
        self.cancel_timer()
        self._timeout_flag = False
        self._timer = threading.Timer(
            self.time_limit, lambda: self._set_timeout(on_timeout_callback)
        )
        self._timer.start()

    def cancel_timer(self):
        """Cancel the current timer and reset timeout flag."""
        if self._timer and self._timer.is_alive():
            self._timer.cancel()
        self._timer = None
        self._timeout_flag = False

    def _set_timeout(self, callback):
        """Handle timeout event and execute callback."""
        self._timeout_flag = True
        callback()

    def timed_out(self):
        """Deduct one life due to timeout."""
        self.remaining_lives -= 1
    def guess(self, letter):
        """
        Handle a player's guess.

        :param letter: single alphabet character
        :return: tuple(status, message)
        """
        letter = letter.lower()
        if len(letter) != 1 or not letter.isalpha():
            return "invalid", "Please guess a single alphabet letter."

        if letter in self.guessed:
            return "already", f"'{letter}' was already guessed."

        self.guessed.add(letter)

        if letter in self.answer.lower():
            self.revealed = self._mask_word()
            return True, f"Good guess! '{letter}' is in the answer."
        self.remaining_lives -= 1
        return False, f"Wrong guess! '{letter}' is not in the answer."

    def is_won(self):
        """Check if the game is won (all letters revealed)."""
        return "_" not in self._mask_word()

    def is_lost(self):
        """Check if the game is lost (no lives left)."""
        return self.remaining_lives <= 0
