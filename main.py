import time
import sys
import msvcrt  # Windows-specific module for keyboard input
from hangman import HangmanEngine


def play_game():
    """Run the Hangman command-line interface game."""
    print("Welcome to Hangman!\n")

    # Ask the player to choose difficulty level
    while True:
        level = input("Choose level - (b)asic or (i)ntermediate (b/i): ").strip().lower()
        if level in ("b", "basic"):
            lvl = "basic"
            break
        if level in ("i", "intermediate"):
            lvl = "intermediate"
            break
        print("Please enter 'b' or 'i'.")

    game = HangmanEngine(level=lvl)

    while True:
        game.reset()
        print("\nNew Game Started! (type 'quit' to exit anytime)\n")

        # Main guessing loop
        while not game.is_won() and not game.is_lost():
            print("Word: ", game.revealed)             # Show current word state
            print("Lives remaining:", game.remaining_lives)
            print(f"You have {game.time_limit} seconds to enter a letter...")

            guess = None
            start_time = time.time()

            # Input loop with countdown timer
            while True:
                if msvcrt.kbhit():
                    guess = msvcrt.getwch()
                    if guess == "\r":  # ignore Enter key
                        continue
                    break

                elapsed = int(time.time() - start_time)
                remaining = game.time_limit - elapsed
                sys.stdout.write(f"\rTime left: {remaining} seconds ")
                sys.stdout.flush()

                if remaining <= 0:
                    break
                time.sleep(0.5)

            print()

            # Handle timeout
            if not guess:
                print("\nTime's up! You lost one life.")
                game.timed_out()
            else:
                guess = guess.lower().strip()
                if guess == "quit":
                    print("Quitting game. The answer was:", game.answer)
                    return
                result, msg = game.guess(guess)
                print(msg)

        # Game result
        if game.is_won():
            print("\nCongratulations, you won! The word was:", game.answer)
        else:
            print("\nGame Over! The word was:", game.answer)

        # Ask if player wants to play again
        again = input("\nPlay again? (y/n): ").strip().lower()
        if again != "y":
            print("Thanks for playing. Goodbye!")
            break


if __name__ == "__main__":
    play_game()
