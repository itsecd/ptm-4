import logging
from functions import *


minesweeper_logger = logging.getLogger()
logging.basicConfig(filename='logs.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


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
    minesweeper_logger.info("Game started")
    while playing:
        showCells(points, totalPoints, flags, moves, cells, columns)
        print("1. Cell\n2. Flag\n")
        choice = input("Select (1/2): ")

        match choice:
            case "1":
                minesweeper_logger.info("Cell selected")
                cellChosen = input("Select cell: ")
                try:
                    rowChosen = int(cellChosen.split(",")[0].strip())
                    columnChosen = int(cellChosen.split(",")[1].strip())
                    minesweeper_logger.info(f"Entered coordinates: {rowChosen}, {columnChosen}")
                except (ValueError, IndexError):
                    minesweeper_logger.error("Incorrect coordinates have been entered")
                    rowChosen = 0
                    columnChosen = 0

                if [rowChosen, columnChosen] in cellsWithMines and cells[rowChosen][columnChosen] != "F":
                    playing = False
                    moves += 1
                    showMines(cellsWithMines, cells)
                    showCells(points, totalPoints, flags, moves, cells, columns)
                    minesweeper_logger.info("Game over, you lost")
                    print("You lost!")

                elif rowChosen > 0 and rowChosen <= rows and columnChosen > 0 and columnChosen <= columns \
                        and cells[rowChosen][columnChosen] != "F" and [rowChosen, columnChosen] not in selectedCells:

                    selectedCellMinesAround = checkMinesAround(rowChosen, columnChosen, rows, columns, cellsWithMines)
                    cells[rowChosen][columnChosen] = selectedCellMinesAround
                    selectedCells.append([rowChosen, columnChosen])
                    points += 1

                    points = checkCellsAround(rowChosen, columnChosen, rows, columns, selectedCells, cellsWithMines,
                                              cells, selectedCellMinesAround, points)
                    minesweeper_logger.info("Cell opened")

                if points == totalPoints:
                    playing = False
                    moves += 1
                    showMines(cellsWithMines, cells)
                    showCells(points, totalPoints, flags, moves, cells, columns)
                    minesweeper_logger.info("You win")
                    print("You win!")

            case "2":
                minesweeper_logger.info("Flag selected")
                cellChosen = input("Select cell: ")
                try:
                    rowChosen = int(cellChosen.split(",")[0].strip())
                    columnChosen = int(cellChosen.split(",")[1].strip())
                    minesweeper_logger.info(f"Entered coordinates: {rowChosen}, {columnChosen}")
                except (ValueError, IndexError):
                    minesweeper_logger.error("Incorrect coordinates have been entered")
                    rowChosen = 0
                    columnChosen = 0

                flags = addFlag(rowChosen, rows, columnChosen, columns, cells, flags, mines)
                minesweeper_logger.info("Flag added")

            case _:
                minesweeper_logger.warning("Incorrect input")
                pass

        moves = checkMoves(points, flags, moves, lastMove)