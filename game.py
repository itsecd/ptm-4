import logging

from functions import *

logging.basicConfig(level=logging.INFO, filename="log_file.log", filemode="w")

def minesweeper(rows, columns, mines):
    '''
    The main function of the program.
    Check functions.py for a detailed explanation of each function used in this module.
    '''
    cellsWithMines = minesCoordinates(rows, columns, mines)
    cells = cellsCoordinates(rows, columns)

    points = 0
    totalPoints = (rows * columns) - mines
    flags = mines
    moves = 0
    lastMove = [points, flags]
    selectedCells = []
    
    playing = True

    while playing:
        showCells(points, totalPoints, flags, moves, cells, columns)
        print("1. Cell\n2. Flag\n")
        choice = input("Select (1/2): ")

        match choice:
            case "1":
                cellChosen = input("Select cell: ")
                try:
                    rowChosen = int(cellChosen.split(",")[0].strip())
                    columnChosen = int(cellChosen.split(",")[1].strip())
                    logging.info(f"The cell is selected. Chosen row: rowChosen, Chosen column: columnChosen")
                except (ValueError, IndexError):
                    rowChosen = 0
                    columnChosen = 0
                    logging.info(f"The cell is not selected. Chosen row: rowChosen, Chosen column: columnChosen")

                if [rowChosen, columnChosen] in cellsWithMines and cells[rowChosen][columnChosen] != "F":
                    playing = False
                    moves += 1
                    showMines(cellsWithMines, cells)
                    showCells(points, totalPoints, flags, moves, cells, columns)
                    logging.info("Loss")
                    print("You lost!")

                elif rowChosen > 0 and rowChosen <= rows and columnChosen > 0 and columnChosen <= columns \
                and cells[rowChosen][columnChosen] != "F" and [rowChosen, columnChosen] not in selectedCells:

                    selectedCellMinesAround = checkMinesAround(rowChosen, columnChosen, rows, columns, cellsWithMines)
                    cells[rowChosen][columnChosen] = selectedCellMinesAround
                    selectedCells.append([rowChosen, columnChosen])
                    points += 1

                    points = checkCellsAround(rowChosen, columnChosen, rows, columns, selectedCells, cellsWithMines, cells, selectedCellMinesAround, points)

                if points == totalPoints:
                    playing = False
                    moves += 1
                    showMines(cellsWithMines, cells)
                    showCells(points, totalPoints, flags, moves, cells, columns)
                    logging.info("Winning")
                    print("You win!")

            case "2":
                cellChosen = input("Select cell: ")
                try:
                    rowChosen = int(cellChosen.split(",")[0].strip())
                    columnChosen = int(cellChosen.split(",")[1].strip())
                    logging.info(f"The cell is selected. Chosen row: rowChosen, Chosen column: columnChosen")
                except (ValueError, IndexError):
                    rowChosen = 0
                    columnChosen = 0
                    logging.info(f"The cell is not selected. Chosen row: rowChosen, Chosen column: columnChosen")

                flags = addFlag(rowChosen, rows, columnChosen, columns, cells, flags, mines)
                logging.info("Added flag")

            case _:
                pass
        
        moves = checkMoves(points, flags, moves, lastMove)