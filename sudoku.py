#!/usr/bin/env python
# coding:utf-8

"""
Each sudoku board is represented as a dictionary with string keys and
int values.
e.g. my_board['A1'] = 8
"""
import statistics
import sys
import copy
from time import time

ROW = "ABCDEFGHI"
COL = "123456789"


def print_board(board):
    """Helper function to print board in a square."""
    print("-----------------")
    for i in ROW:
        row = ''
        for j in COL:
            row += (str(board[i + j]) + " ")
        print(row)


def board_to_string(board):
    """Helper function to convert board dictionary to string for writing."""
    ordered_vals = []
    for r in ROW:
        for c in COL:
            ordered_vals.append(str(board[r + c]))
    return ''.join(ordered_vals)


def backtracking(board):
    """Takes a board and returns solved board."""
    dom_dict = copy.deepcopy(board)
    for key, value in dom_dict.items():
        if value == 0:
            dom_dict[key] = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        else:
            dom_dict[key] = [value]
    for key, value in board.items():
        if value != 0:
            dom_dict = reduce_domain(key, dom_dict, board)
    solved_board = backtracking_helper(board, dom_dict)
    return solved_board


def backtracking_helper(board, dom_dict):
    if board_completed(board):
        return board

    var = select_variable(dom_dict, board)

    for choice in dom_dict[var]:
        consistent_dom = value_consistent(choice, var, board, dom_dict)
        if consistent_dom:
            new_board = consistent_dom[1]
            new_dom = consistent_dom[0]
            result = backtracking_helper(new_board, new_dom)
            if result:
                return result
    return None


def value_consistent(choice, var, board, dom_dict):
    test_board = copy.deepcopy(board)
    test_dom_dict = copy.deepcopy(dom_dict)
    test_board[var] = choice
    test_dom_dict[var] = [choice]
    new_dom_dict = reduce_domain(var, test_dom_dict, test_board)
    for value in new_dom_dict.values():
        if len(value) == 0:
            return False
    return new_dom_dict, test_board


def select_variable(dom_dict, board):
    min_len = 10
    min_len_name = ""
    for key, value in dom_dict.items():
        if min_len > len(value) > 1:
            min_len = len(value)
            min_len_name = key
        elif min_len > len(value) == 1:
            if board[key] == 0:
                min_len = len(value)
                min_len_name = key
    return min_len_name


def board_completed(board):
    for value in board.values():
        if value == 0:
            return False
    return True


def domain_done(dom_dict):
    for value in dom_dict.values():
        if len(value) > 1:
            return False
    return True


def reduce_domain(square, dom_dict, board):
    location = square
    row = location[0]
    column = location[1]
    value = board[location]
    row_dict = {0: ["A", "B", "C"],
                1: ["D", "E", "F"],
                2: ["G", "H", "I"]}
    column_dict = {0: [1, 2, 3],
                   1: [4, 5, 6],
                   2: [7, 8, 9]}
    for key in dom_dict.keys():
        search_row = key[0]
        search_column = key[1]
        if (search_row == row or search_column == column) and (key != location):
            if value in dom_dict[key]:
                dom_dict[key].remove(value)
        for i in row_dict.values():
            for j in column_dict.values():
                if row in i and int(column) in j:
                    for i_row in i:
                        for j_column in j:
                            square_string = str(i_row) + str(j_column)
                            if (value in dom_dict[square_string]) and (square_string != location):
                                dom_dict[square_string].remove(value)
    return dom_dict


if __name__ == '__main__':
    if len(sys.argv) > 1:

        # Running sudoku solver with one board $python3 sudoku.py <input_string>.
        print(sys.argv[1])
        # Parse boards to dict representation, scanning board L to R, Up to Down
        board = {ROW[r] + COL[c]: int(sys.argv[1][9 * r + c])
                 for r in range(9) for c in range(9)}

        solved_board = backtracking(board)

        # Write board to file
        out_filename = 'output.txt'
        outfile = open(out_filename, "w")
        outfile.write(board_to_string(solved_board))
        outfile.write('\n')

    else:
        # Running sudoku solver for boards in sudokus_start.txt $python3 sudoku.py

        #  Read boards from source.
        src_filename = 'sudokus_start.txt'
        finish_filename = 'sudokus_finish.txt'
        try:
            srcfile = open(src_filename, "r")
            finishfile = open(finish_filename, "r")
            sudoku_list = srcfile.read()
            sudoku_solution = finishfile.read()
        except:
            print("Error reading the sudoku file %s" % src_filename)
            exit()
        try:
            finishfile = open(finish_filename, "r")
            sudoku_solution = finishfile.read()
        except:
            print("Error reading the sudoku file %s" % finish_filename)
            exit()

        # Setup output file
        out_filename = 'output.txt'
        outfile = open(out_filename, "w")

        count = 0
        total_times = []
        # Solve each board using backtracking
        for line_s, line_f in zip(sudoku_list.split("\n"), sudoku_solution.split("\n")):

            if len(line_s) < 9:
                continue

            # Parse boards to dict representation, scanning board L to R, Up to Down
            board = {ROW[r] + COL[c]: int(line_s[9 * r + c])
                     for r in range(9) for c in range(9)}
            board_finish = {ROW[r] + COL[c]: int(line_f[9 * r + c])
                            for r in range(9) for c in range(9)}

            # Print starting board. TODO: Comment this out when timing runs.
            # print_board(board)

            # Solve with backtracking
            start_time = time()
            solved_board = backtracking(board)
            end_time = time()

            if solved_board == board_finish:
                total_times.append(end_time - start_time)
                count += 1

            # Print solved board. TODO: Comment this out when timing runs.
            # print_board(solved_board)

            # Write board to file
            outfile.write(board_to_string(solved_board))
            outfile.write("\n")

        stats_filename = 'results_stats.txt'
        statsfile = open(stats_filename, "w")

        statsfile.write("Number of Solved Boards : " + str(count))
        statsfile.write("\n")
        min_time = min(total_times)
        max_time = max(total_times)
        avg_time = sum(total_times) / len(total_times)
        std_time = statistics.stdev(total_times)
        statsfile.write("Minimum Time : " + str(min_time))
        statsfile.write("\n")
        statsfile.write("Maximum Time : " + str(max_time))
        statsfile.write("\n")
        statsfile.write("Mean : " + str(avg_time))
        statsfile.write("\n")
        statsfile.write("Standard Deviation : " + str(std_time))

        print("Finishing all boards in file.")
