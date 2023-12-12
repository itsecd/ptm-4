import logging

from game import minesweeper

playing = True
logging.basicConfig(level=logging.INFO, filename="log_file.log", filemode="w")
logging.info("Start")
while playing:
    restart = ""

    print("\nCLI Python Minesweeper by espy, v1.1.1\nhttps://github.com/espy02/cli-python-minesweeper\n")
    print("Select the difficulty:\n\n1. Beginner - 10x10 / 10 mines\n2. Intermediate - 16x16 / 40 mines\n3. Expert - 30x16 / 99 mines\n4. Custom\n")
    difficulty = input("Difficulty (1/2/3/4): ")

    match difficulty:
        case "1":
            logging.info("Selected difficulty: 10x10 / 10 mines")
            input("\nNote: to select a cell, enter the number of the row, and the number of the column, separated by a comma.\nExample: 4,5\nPress enter to continue.")
            minesweeper(rows = 10, columns = 10, mines = 10)

        case "2":
            logging.info("Selected difficulty: 16x16 / 40 mines")
            input("\nNote: to select a cell, enter the number of the row, and the number of the column, separated by a comma.\nExample: 4,5\nPress enter to continue.")
            minesweeper(rows = 16, columns = 16, mines = 40)

        case "3":
            logging.info("Selected difficulty: 30x16 / 99 mines")
            input("\nNote: to select a cell, enter the number of the row, and the number of the column, separated by a comma.\nExample: 4,5\nPress enter to continue.")
            minesweeper(rows = 30, columns = 16, mines = 99)

        case "4":
            logging.info("Selected difficulty: custom")
            try:
                rows = int(input("Rows: "))
                columns = int(input("Columns: "))
                mines = int(input("Mines: "))
                logging.info(f"Difficulty: Rows: rows, Columns: columns, Mines: mines")
            except ValueError:
                rows = 0
                columns = 0
                mines = 0
                logging.info("Difficulty: rows = 0, columns = 0, mines = 0")

            if rows == 0 or columns == 0:
                print("\nNot enough rows/columns!")
                restart = "y"
                logging.info("Restart")

            elif mines > (rows * columns):
                print("\nToo many bombs!")
                restart = "y"
                logging.info("Restart. Too many bombs.")

            else:
                input("\nNote: to select a cell, enter the number of the row, and the number of the column, separated by a comma.\nExample: 4,5\nPress enter to continue.")
                logging.info("Field and number of mines are configured")
                minesweeper(rows, columns, mines)

        case _:
            restart = "y"
            logging.info("Restart")

    while restart != "y" and restart != "n":
        restart = input("Do you want to restart? (y/n): ")
        match restart:
            case "n":
                playing = False
                logging.info("Exit")
            case _:
                pass