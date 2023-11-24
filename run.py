#!/usr/bin/env python
from loguru import logger
import Game

log_format = "{time:YYYY-MM-DD HH:mm:ss.SSS} | {level} | {message} | " + \
             "{extra[script]} | {extra[description]} | {extra[params]}"
log_config = {
    "handlers": [],
    "extra": {"script": "Game.py", "description": "", "params": ""}
}
logger.configure(**log_config)
logger.add("snake.log", format=log_format,  retention="1 day")


def main():
    menu = Game.Menu()
    score_board = Game.ScoreBoard()

    # play = Game.Play("#", "*")
    play = Game.Play("█", "░")
    logger.info('GAME_STARTED', script="run.py", description='snake game was started')
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
            logger.info('GAME_ENDED', script="run.py", description='snake game was ended')
            break


if __name__ == "__main__":
    main()



