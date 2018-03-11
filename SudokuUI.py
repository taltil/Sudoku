from tkinter import *
import tkinter.messagebox
from SudokuGame import *
from Stack import *
from BoardState import *


# responsible for board drawing and receiving input from user

class SudokuUI(Frame, SudokuGame):
    def __init__(self, master, board_file):
        Frame.__init__(self, master)
        SudokuGame.__init__(self, board_file)
        Stack.__init__(self)
        self.board_matrix = SudokuBoard.__create_board__(self)
        self.board_file = board_file
        self.master = master
        self.pack()
        self.__init_ui()

    def __init_ui(self):
        self.margin = 20
        self.cell_size = 50
        self.width = 2 * self.margin + 9 * self.cell_size
        self.height = 2 * self.margin + 9 * self.cell_size
        self.lastr = 0
        self.lastc = 0
        self.canvas = Canvas(self, height=self.height, width=self.width, bg='white')
        self.canvas.pack()
        self.resetButton = Button(self, text='Reset', command=self.reset_board, bg='white', fg='black')
        self.resetButton.pack(side=LEFT)
        self.exitButton = Button(self, text='Quit', command=self.finish_game, bg='white', fg='black')
        self.exitButton.pack(side=RIGHT)
        self.undoButton = Button(self, text='Undo', command=self.undo, bg='white', fg='black')
        self.undoButton.pack(side=LEFT, padx=25)
        self.__draw_grid()
        self.__draw_puzzle(self.board_matrix)
        self.mouse_click()

    def reset_board(self):
        SudokuGame.__start__(self)
        self.board_matrix = SudokuBoard.__create_board__(self)
        self.__draw_puzzle(self.board_matrix)

    def finish_game(self):
        # show massage box to verify quiting and exit if user want to quit
        m_exit = tkinter.messagebox.askyesno('Quit?', 'Are you sure?')
        if m_exit > 0:
            self.master.destroy()
            return

    def __draw_grid(self):
        a = self.margin
        b = self.width - self.margin
        line = a
        i = 0
        while line <= b:
            if i % 3 == 0:
                self.canvas.create_line(line, a, line, b, fill='blue')
                self.canvas.create_line(a, line, b, line, fill='blue')
            else:
                self.canvas.create_line(line, a, line, b, fill='grey')
                self.canvas.create_line(a, line, b, line, fill='grey')
            i += 1
            line += self.cell_size

    def __draw_puzzle(self, board_matrix):
        self.canvas.delete("numbers")
        start = self.margin + (self.cell_size / 2)  # zero point (x,y of first square)
        for i in range(0, 9):
            for j in range(0, 9):
                answer = board_matrix[i][j]
                if answer != '0':
                    self.canvas.create_text(start + j * 50, start + i * 50, text=answer, tag="numbers", fill='black')

    def paint_cell_red(self):
        r = self.margin + (self.r * self.cell_size)  # converting to pixals
        c = self.margin + (self.c * self.cell_size)  # converting to pixals
        self.canvas.create_line(c, r, c, r + self.cell_size, fill='red')
        self.canvas.create_line(c + self.cell_size, r, c, r, fill='red')
        self.canvas.create_line(c + self.cell_size, r + self.cell_size, c + self.cell_size, r, fill='red')
        self.canvas.create_line(c, r + self.cell_size, c + self.cell_size, r + self.cell_size, fill='red')

    def winner(self):
        top = Toplevel(self.master)
        frame_win = Frame(top, width=200, height=200, bg='white')
        label_win = Label(top, text="You won!!!", fg="blue", bg='white', font=("Helvetica", 24))
        label_win.pack()
        label_win.place(x=20, y=70)
        frame_win.pack()
        self.master.wait_window(top)

    def new_number(self, num):
        self.board_matrix[self.r][self.c] = str(num)
        Stack.push(self, [self.r, self.c])
        self.canvas.create_text(self.margin + (self.cell_size / 2) + self.c * 50,
                                self.margin + (self.cell_size / 2) + self.r * 50, text=num, tag="numbers", fill='green')

        board_state= SudokuGame.check_win(self)
        if board_state==BoardState.FULL_AND_RIGHT:
                self.winner()
        elif board_state==BoardState.FULL_AND_WRONG:
                tkinter.messagebox.showinfo("Full Board", "Something is not right!!")
        self.__draw_grid()

    def get_number(self, event):
        num = event.char
        try:
            num = int(num)
            if 9 >= num >= 1:
                self.new_number(num)
        except Exception as e:
            print(e)

    def get_xy(self, event):
        self.__draw_grid()
        self.canvas.focus_set()
        x = event.x
        y = event.y
        self.c = int((x - self.margin) / self.cell_size)
        self.r = int((y - self.margin) / self.cell_size)
        if (self.board_matrix[self.r][self.c]) == '0':
            self.paint_cell_red()
            self.canvas.bind("<Key>", self.get_number)

    def mouse_click(self):
        self.canvas.bind("<Button-1>", self.get_xy)

    def undo(self):
        if not Stack.is_empty(self):
            [self.lastr, self.lastc] = Stack.pop(self)
            self.board_matrix[self.lastr][self.lastc] = '0'
            temp_board = SudokuBoard.__create_board__(self)
            self.__draw_puzzle(temp_board)
            start = self.margin + (self.cell_size / 2)  # zero point (x,y of first square middle point)
            for i in range(0, 9):
                for j in range(0, 9):
                    board_square = self.board_matrix[i][j]
                    temp_square = temp_board[i][j]
                    if board_square != '0' and board_square != temp_square:
                        answer = board_square
                        self.canvas.create_text(start + j * 50, start + i * 50, text=answer, tag="numbers",
                                                fill='green')
        else:
            tkinter.messagebox.showinfo(message="Board is already reset")
