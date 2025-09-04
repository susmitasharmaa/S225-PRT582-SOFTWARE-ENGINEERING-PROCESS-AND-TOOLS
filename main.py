import time
import sys
import msvcrt   # Windows-specific module for keyboard input
from hangman import HangmanEngine

def play_game():
    print("Welcome to Hangman!\n")

    # Ask the player which difficulty they want
    while True:
        level = input("Choose level - (b)asic or (i)ntermediate (b/i): ").strip().lower()
        if level in ("b", "basic"):
            lvl = "basic"
            break
        if level in ("i", "intermediate"):
            lvl = "intermediate"
            break
        print("Please enter 'b' or 'i'.")

    # Create the game engine with the chosen level
    game = HangmanEngine(level=lvl)

    while True:
        game.reset()
        print("\nNew Game Started! (type 'quit' to exit anytime)\n")

        # Keep looping until the player either wins or runs out of lives
        while not game.is_won() and not game.is_lost():
            print("Word: ", game.revealed)                 # show current state of the word
            print("Lives remaining:", game.remaining_lives)

            print(f"You have {game.time_limit} seconds to enter a letter...")
            guess = None
            start_time = time.time()

            # Wait for input, but also count down the seconds left
            while True:
                if msvcrt.kbhit():  # check if a key was pressed
                    guess = msvcrt.getwch()  # read the key
                    if guess == "\r":        # ignore Enter key
                        continue
                    break  # exit once a key is captured

                # Show countdown timer while waiting for input
                elapsed = int(time.time() - start_time)
                remaining = game.time_limit - elapsed
                sys.stdout.write(f"\rTime left: {remaining} seconds ")
                sys.stdout.flush()

                if remaining <= 0:  # ran out of time
                    break
                time.sleep(0.5)

            print()  # move cursor to new line

            # If time ran out and no letter was entered
            if not guess:
                print("\n Time's up! You lost one life.")
                game.timed_out()
            else:
                guess = guess.lower().strip()
                if guess == "quit":
                    print("Quitting game. The answer was:", game.answer)
                    return
                result, msg = game.guess(guess)
                print(msg)

        # Decide end of game message
        if game.is_won():
            print("\n Congratulations, you won! The word was:", game.answer)
        else:
            print("\n Game Over! The word was:", game.answer)

        # Ask if player wants to go again
        again = input("\nPlay again? (y/n): ").strip().lower()
        if again != "y":
            print("Thanks for playing. Goodbye!")
            break

# Run the game if this file is the main program
if __name__ == "__main__":
    play_game()
