from loguru import logger
import Game


logger_format = "{time:YYYY-MM-DD HH:mm:ss} | {level} | {message} | {extra[file]} | {extra[transcript]}"
logger_config = {
    "handlers": [],
    "extra": {"file": "", "transcript": ""}
}
logger.configure(**logger_config)
logger.add("app.log", rotation="500 MB", level="INFO", format=logger_format)

def main():
    menu = Game.Menu()
    score_board = Game.ScoreBoard()

    #play = Game.Play("#", "*")
    play = Game.Play("█", "░")

    logger.info("GAME_STARTED", file="run.py", transcript="The game has started")
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
            logger.info("GAME_OVER", file="run.py", transcript="The game is over")
            break


if __name__ == "__main__":
    main()