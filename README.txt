SUDOKU PROJECT - Artificial Intelligence Fall 2021

The objective of Sudoku is to fill a 9x9 grid with the numbers 1-9 so that each column, row, and 3x3 sub-grid (or box)
contains one of each digit. You may try out the game here: sudoku.com. Sudoku has 81 variables, i.e. 81 tiles.
The variables are named by row and column, and are valued from 1 to 9 subject to the constraints that no two cells in
the same row, column, or box may be the same.

Frame your problem in terms of variables, domains, and constraints. We suggest representing a Sudoku board with a
Python dictionary, where each key is a variable name based on location, and value of the tile placed there. Using
variable names Al... A9... I1... I9, the board above has:
• sudoku dict["B1"] = 2, and
• sudoku dict["E2"] = 9.
We give value zero to a tile that has not yet been filled.

In the starter zip, sudokus start.txt, contains hundreds of sample unsolved Sudoku boards, and sudokus finish.txt the
corresponding solutions. Each board is represented as a single line of text, starting from the top-left corner of the
board, and listed left-to-right, top-to-bottom.

Your program will generate output.txt, containing lines of text representing the finished Sudoku boards.

The results_stats.txt contains the results, including the:
• number of boards you could solve from sudokus start.txt,
• running time statistics: min, max, mean, and standard deviation.