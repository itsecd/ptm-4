import logging

from game import minesweeper

logging.basicConfig(filename='minesweeper.log', level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')
playing = True
while playing:
    restart = ""

    print("\nCLI Python Minesweeper by espy, v1.1.1\nhttps://github.com/espy02/cli-python-minesweeper\n")
    print("Select the difficulty:\n\n1. Beginner - 10x10 / 10 mines\n2. Intermediate - 16x16 / 40 mines\n3. Expert - 30x16 / 99 mines\n4. Custom\n")

    difficulty = input("Difficulty (1/2/3/4): ")
    print(f'Selected difficulty: {difficulty}')

    match difficulty:
        case "1":
            input("\nNote: to select a cell, enter the number of the row, and the number of the column, separated by a comma.\nExample: 4,5\nPress enter to continue.")
            logging.info("Created field with 10 rows, 10 columns, 10 mines")
            minesweeper(rows=10, columns=10, mines=10)

        case "2":
            input("\nNote: to select a cell, enter the number of the row, and the number of the column, separated by a comma.\nExample: 4,5\nPress enter to continue.")
            logging.info("Created field with 16 rows, 16 columns, 40 mines")
            minesweeper(rows=16, columns=16, mines=40)

        case "3":
            input("\nNote: to select a cell, enter the number of the row, and the number of the column, separated by a "
                  "comma.\nExample: 4,5\nPress enter to continue.")
            logging.info("Created field with 30 rows, 16 columns, 99 mines")
            minesweeper(rows=30, columns=16, mines=99)

        case "4":
            try:
                rows = int(input("Rows: "))
                columns = int(input("Columns: "))
                mines = int(input("Mines: "))
            except ValueError:
                rows = 0
                columns = 0
                mines = 0

            if rows == 0 or columns == 0:
                logging.error("Not enough rows/columns!")
                print("\nNot enough rows/columns!")
                restart = "y"

            elif mines > (rows * columns):
                logging.error("Too many bombs!")
                print("\nToo many bombs!")
                restart = "y"
            elif mines <= 0:
                logging.error("Not Enough bombs!")
                print("\nNot Enough bombs!")
                restart = "y"

            else:
                logging.info(f"Created field with {rows} rows, {columns} columns, {mines} mines")
                input("\nNote: to select a cell, enter the number of the row, and the number of the column, separated by a comma.\nExample: 4,5\nPress enter to continue.")
                minesweeper(rows, columns, mines)

        case _:
            logging.error("Invalid difficulty selected.")
            restart = "y"

    while restart != "y" and restart != "n":
        logging.info(f'Asking for restart the game...')
        restart = input("Do you want to restart? (y/n): ")
        logging.debug(f'Restart choice: {restart}')

        match restart:
            case "n":
                playing = False
            case _:
                pass
