import os
import logging
from rich.console import Console
from rich.table import Table
from rich.live import Live
from src.modules.wordle import Wordle

def setupLogger():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    format = logging.Formatter('%(asctime)s  %(levelname)s  %(message)s')
    handler = logging.FileHandler('worldle.log')
    handler.setLevel(logging.INFO)
    handler.setFormatter(format)
    logger.addHandler(handler)
    return logger

def clear():
    if os.name == 'nt':
        _ = os.system('cls')
    else:
        _ = os.system('clear')
        
def main():
    logger = setupLogger()
    logger.info("Start game")

    puzzle = Wordle(logger)
    console = Console()
    table = Table(title="Guesses", box=None)
    console.print(table)

    retries_pending = 6

    while retries_pending:
        puzzle.get_user_guess(remaining=retries_pending)
        status, result = puzzle.check_word()
        clear()
        with Live(table):
            msg_row = [f'[black on {i["color"]}] {i["letter"]} [/black on {i["color"]}]' for i in result]
            table.add_row(*msg_row)
            table.add_row("")
        if status:
            retries_pending = 0
            print(console.print('\n :thumbs_up: Wow, you aced it!! \n'))
            logger.info("Game is won!")
        else:
            retries_pending -= 1

    if not status:
        console.print(f'\n\n☹️  [bold red]Correct Word is {puzzle.chosen_word.upper()} [/bold red]')
        logger.info("Game is lost")


if __name__ == "__main__":
    main()