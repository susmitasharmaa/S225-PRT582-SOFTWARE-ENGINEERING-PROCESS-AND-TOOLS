import random
import threading

class HangmanEngine:
    def __init__(self, words=None, phrases=None, lives=6, time_limit=15, level="basic"):
        # words = simple single words, phrases = multi-word strings
        # lives = number of wrong guesses allowed
        # time_limit = seconds allowed for one guess
        # level = difficulty setting ("basic" uses words, "intermediate" uses phrases)
        self.words = words or ["python", "hangman", "testing", "pytest", "unittest"]
        self.phrases = phrases or ["open ai", "machine learning", "unit testing"]
        self.lives = lives
        self.time_limit = time_limit
        self.level = level
        self.reset()

    def reset(self):
        # Pick a new word/phrase depending on the level
        if self.level == "basic":
            self.answer = random.choice(self.words)
        else:
            self.answer = random.choice(self.phrases)

        # Set up initial state for a fresh game
        self.guessed = set()               # letters already tried
        self.remaining_lives = self.lives  # lives left
        self.revealed = self._mask_word()  # masked version of the answer
        self._timeout_flag = False         # used for timing guesses
        self._timer = None

    def _mask_word(self):
        # Hide letters that haven’t been guessed yet, but keep spaces visible
        return "".join([c if (c == " " or c.lower() in self.guessed) else "_" for c in self.answer])

    def start_timer(self, on_timeout_callback):
        """
        Start a countdown for the current guess.
        If the timer runs out, trigger the callback (like losing a turn).
        """
        self.cancel_timer()  # stop any old timer first
        self._timeout_flag = False
        self._timer = threading.Timer(self.time_limit, lambda: self._set_timeout(on_timeout_callback))
        self._timer.start()

    def cancel_timer(self):
        # Stop and reset the timer if it’s currently running
        if self._timer and self._timer.is_alive():
            self._timer.cancel()
        self._timer = None
        self._timeout_flag = False

    def _set_timeout(self, callback):
        # Flag that time is up and run the given callback function
        self._timeout_flag = True
        callback()

    def timed_out(self):
        # If time is up, reduce one life (can be used in testing)
        self.remaining_lives -= 1

    def guess(self, letter):
        """
        Handle a player’s guess.
        Returns: 
          - "invalid" → input isn’t a single letter
          - "already" → letter was guessed before
          - True → correct guess
          - False → wrong guess
        """
        letter = letter.lower()
        if len(letter) != 1 or not letter.isalpha():
            return ("invalid", "Please guess a single alphabet letter.")

        if letter in self.guessed:
            return ("already", f"'{letter}' was already guessed.")

        # Record the guess
        self.guessed.add(letter)

        # Check if the guessed letter is in the word/phrase
        if letter in self.answer.lower():
            self.revealed = self._mask_word()
            return (True, f"Good guess! '{letter}' is in the answer.")
        else:
            self.remaining_lives -= 1
            return (False, f"Wrong guess! '{letter}' is not in the answer.")

    def is_won(self):
        # Win when there are no underscores left (all letters revealed)
        return "_" not in self._mask_word()

    def is_lost(self):
        # Lose if no lives remain
        return self.remaining_lives <= 0
