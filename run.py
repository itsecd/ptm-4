#!/usr/bin/env python
import sys
from loguru import logger
import Game

log_format = "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | " \
             "<level>{message}</level> | " + \
             "<cyan>{extra[script]}</cyan> | " + \
             "<cyan>{extra[description]}</cyan> | " + \
             "<blue>{extra[params]}</blue>"
log_config = {
    "handlers": [{"sink": "snake.log", "format": log_format}],
    "extra": {"script": "Game.py", "description": "", "params": ""}
}
logger.configure(**log_config)


def main():
    menu = Game.Menu()
    score_board = Game.ScoreBoard()

    # play = Game.Play("#", "*")
    play = Game.Play("█", "░")

    logger.info('GAME_START', script="run.py", description='snake game was started')
    while 1:
        menu.start

        if menu.selected_item == 0:
            # Volta pro menu se a tela for redimencionada
            try:
                play.start
            except:
                pass

            score_board.add_score(play.score[:])

        elif menu.selected_item == 1:
            score_board.start

        else:
            logger.info('GAME_END', script="run.py", description='snake game was ended')
            break


if __name__ == "__main__":
    main()



