import os
import logging
from rich.console import Console
from rich.table import Table
from rich.live import Live
from wordle import Wordle

logger1 = logging.getLogger("main")
logger1.setLevel(logging.INFO)
handler1 = logging.FileHandler("main.log", mode='w')
formatter1 = logging.Formatter(
    "%(name)s %(asctime)s %(levelname)s %(message)s")
handler1.setFormatter(formatter1)
logger1.addHandler(handler1)


def clear():
    if os.name == 'nt':
        _ = os.system('cls')
        logger1.info("Terminal cleared successfully")
    else:
        _ = os.system('clear')
        logger1.info("Terminal cleared successfully on Unix-like system")


def main():
    puzzle = Wordle()
    console = Console()
    table = Table(title="Guesses", box=None)
    console.print(table)

    retries_pending = 6

    while retries_pending:
        puzzle.get_user_guess(remaining=retries_pending)
        logger1.info("User guess: %s", puzzle.user_guess)

        status, result = puzzle.check_word()
        logger1.info("Word check result: %s", result)

        clear()
        with Live(table):
            msg_row = [
                f'[black on {i["color"]}] {i["letter"]} [/black on {i["color"]}]' for i in result]
            table.add_row(*msg_row)
            table.add_row("")

        if status:
            retries_pending = 0
            logger1.info("User successfully guessed the word.")
            print(console.print('\n :thumbs_up: Wow, you aced it!! \n'))
        else:
            retries_pending -= 1

    if not status:
        logger1.info("User failed to guess the word. Correct word: %s",
                     puzzle.chosen_word.upper())
        console.print(
            f'\n\n☹️  [bold red]Correct Word is {puzzle.chosen_word.upper()} [/bold red]')


if __name__ == "__main__":
    main()
