import math
from SudokuBoard import *
from BoardState import *


# A sudoku game in charge of storing the state of the board and checking
# if the puzzle is completed

class SudokuGame(SudokuBoard):
    def __init__(self, board_file):
        super().__init__(board_file)
        self.board_file = board_file
        self.r = 0
        self.c = 0
        self.puzzle = []

    def __start__(self):
        self.puzzle = super().__create_board__()

    def __check_row(self, r):
        for k in range(0, 9):
            if (self.board_matrix[r][k]) == '0':
                return False
            elif (self.board_matrix[r].index(self.board_matrix[r][k]) != 8 - self.board_matrix[r][::-1].index(
                    self.board_matrix[r][k])):
                return False
        return True

    def __check_col(self, c):
        board_col = []
        for i in range(0, 9):
            board_col.insert(i, self.board_matrix[i][c])
        for k in range(0, 9):
            if (board_col[k]) == '0':
                return False
            elif (board_col.index(board_col[k])) != (8 - board_col[::-1].index(board_col[k])):
                return False
        return True

    def __check_square(self, c, r):
        ci = math.ceil(self.c / 3)
        ri = math.ceil(self.r / 3)
        board_sqr = ''
        for i in range((ri - 1) * 3, ri * 3):
            for j in range((ci - 1) * 3, ci * 3):
                board_sqr += str(self.board_matrix[i][j])
        for k in range(0, 9):
            if board_sqr[k] == '0':
                return False
            elif board_sqr.index(board_sqr[k]) != 8 - board_sqr[::-1].index(board_sqr[k]):
                return False
        return True

    # return true if the board is full and false otherwise
    def is_board_full(self):
        for i in range(0, 9):
            for j in range(0, 9):
                if self.board_matrix[i][j] == '0':
                    return False
        return True

    # return true if the board is full and false otherwise
    def check_win(self):
        for i in range(0, 9):
            for j in range(0, 9):
                if self.board_matrix[i][j] == '0':
                    return BoardState.NOT_FULL
        flag = True
        for i in range(0, 9):
            for j in range(0, 9):
                if (i % 3 == 0) and (j % 3 == 0):
                    flag = self.__check_row(i) and self.__check_col(j) and self.__check_square(i, j)
                else:
                    flag = self.__check_row(i) and self.__check_col(j)
                if not flag:
                    break
            if not flag:
                break
        return BoardState.FULL_AND_RIGHT if flag else BoardState.FULL_AND_WRONG
