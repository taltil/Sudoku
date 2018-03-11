# sudoku board representation as matrix

class SudokuBoard(object):
    def __init__(self, board_file):
        self.board_file = board_file
        self.board_matrix = []

    def __create_board__(self):
        board_matrix = []
        with open(self.board_file, 'r') as b_file:
            data = b_file.readlines()
        assert (len(data) == 9), 'Board data has an error'  # verify the board has only 9 lines
        for i in range(0, 9):
            try:
                int(data[i])  # verify the line is integer
            except:
                print('Board data has an error')
                break
            line = []  # creating sublist for each line
            for j in range(0, 9):
                line.insert(j, data[i][j])
            board_matrix.insert(i, line)
        return board_matrix
