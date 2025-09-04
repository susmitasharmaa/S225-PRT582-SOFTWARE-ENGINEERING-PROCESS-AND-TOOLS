import random
import threading


class HangmanEngine:
    """
    Hangman game engine class.
    Handles game logic, word/phrase selection, guesses, lives, and timeout.
    """

    def __init__(self, words=None, phrases=None, lives=6, time_limit=15, level="basic"):
        """
        Initialize the game engine.
        :param words: list of simple words (basic mode)
        :param phrases: list of multi-word phrases (intermediate mode)
        :param lives: number of wrong guesses allowed
        :param time_limit: seconds allowed per guess
        :param level: "basic" or "intermediate"
        """
        # Use default words/phrases if not provided
        self.words = words or ["python", "hangman", "testing", "pytest", "unittest"]
        self.phrases = phrases or ["open ai", "machine learning", "unit testing"]

        self.lives = lives
        self.time_limit = time_limit
        self.level = level

        # Initialize the first game
        self.reset()

    def reset(self):
        """
        Reset the game state for a new round.
        Picks a new word or phrase based on level.
        """
        # Choose the answer based on level
        self.answer = random.choice(self.words if self.level == "basic" else self.phrases)

        self.guessed = set()              # letters guessed so far
        self.remaining_lives = self.lives  # lives left
        self.revealed = self._mask_word()  # masked word/phrase
        self._timeout_flag = False         # track if timer ran out
        self._timer = None                 # threading.Timer object

    def _mask_word(self):
        """
        Return a masked version of the answer.
        Un-guessed letters are replaced with '_'.
        Spaces are preserved.
        """
        return "".join(
            c if c == " " or c.lower() in self.guessed else "_" for c in self.answer
        )

    def start_timer(self, on_timeout_callback):
        """
        Start a countdown timer for the current guess.
        If time runs out, the callback is triggered.
        """
        self.cancel_timer()  # stop previous timer if running
        self._timeout_flag = False
        self._timer = threading.Timer(
            self.time_limit, lambda: self._set_timeout(on_timeout_callback)
        )
        self._timer.start()

    def cancel_timer(self):
        """Stop the current timer and reset timeout flag."""
        if self._timer and self._timer.is_alive():
            self._timer.cancel()
        self._timer = None
        self._timeout_flag = False

    def _set_timeout(self, callback):
        """
        Mark that time has run out and execute the given callback function.
        Typically reduces a life.
        """
        self._timeout_flag = True
        callback()

    def timed_out(self):
        """Reduce remaining lives by 1 due to timeout."""
        self.remaining_lives -= 1

    def guess(self, letter):
        """
        Process a player's guess.
        :param letter: single alphabet character
        :return: (status, message)
            status: True/False for correct/incorrect, or "invalid"/"already"
        """
        letter = letter.lower()
        if len(letter) != 1 or not letter.isalpha():
            return "invalid", "Please guess a single alphabet letter."

        if letter in self.guessed:
            return "already", f"'{letter}' was already guessed."

        # Record the guess
        self.guessed.add(letter)

        # Check if guess is correct
        if letter in self.answer.lower():
            self.revealed = self._mask_word()
            return True, f"Good guess! '{letter}' is in the answer."
        else:
            self.remaining_lives -= 1
            return False, f"Wrong guess! '{letter}' is not in the answer."

    def is_won(self):
        """Check if the game is won (all letters revealed)."""
        return "_" not in self._mask_word()

    def is_lost(self):
        """Check if the game is lost (no lives left)."""
        return self.remaining_lives <= 0
