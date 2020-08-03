from tkinter import Tk, Canvas, Frame, Button, BOTH, TOP, BOTTOM
import time
from sudoku_solver import SudokuBoard

MARGIN = 20
SIDE = 50
WIDTH = HEIGHT = MARGIN * 2 + SIDE * 9

class SudokuUI(Frame):
    def __init__(self, parent):

        # Load an initial board
        self.sudoku = SudokuBoard()
        self.empty_board = self.sudoku.gen_board()

        # UI Code
        Frame.__init__(self, parent)
        self.parent = parent
        self.disp_row, self.disp_col = -1, -1

        self.__generate_interface()
        pass

    def __generate_interface(self):
        # Generate Tkinter window

        self.parent.title("Sudoku Solver")
        self.pack(fill=BOTH)
        self.canvas = Canvas(self,
                            width=WIDTH,
                            height=HEIGHT)
        self.canvas.pack(fill=BOTH, side=TOP)

        self.__draw_grid()
        self.__draw_numbers(original=True, answers=True)


    def __draw_grid(self):
        # Draw the initial grid
        # 9 x 9 with blue lines to divide the 3 x 3 squares
        for i in range(10):
            colour = "blue" if i % 3 == 0 else "gray"

            # Vertical lines
            x0 = MARGIN + i * SIDE
            y0 = MARGIN
            x1 = MARGIN + i * SIDE
            y1 = HEIGHT - MARGIN

            self.canvas.create_line(x0, y0, x1, y1, fill=colour)

            # Horizontal lines
            x0 = MARGIN
            y1 = MARGIN + i * SIDE
            x1 = WIDTH - MARGIN
            y0 = MARGIN + i * SIDE

            self.canvas.create_line(x0, y0, x1, y1, fill=colour)
        pass

    def __draw_numbers(self, original=False, answers=False):
        # Load numbers into the board
        # TODO: Load solution
        self.canvas.delete("numbers")

        puzzle_board, solution = self.sudoku.gen_puzzle_board()

        if original:
            for i in range(9):
                for j in range(9):
                    answer = puzzle_board[i][j]
                    if answer != 0:
                        x = MARGIN + j * SIDE + SIDE/2
                        y = MARGIN + i * SIDE + SIDE/2
                        self.canvas.create_text(
                            x,y, text=answer, tags="numbers", fill="black"
                        )
        if answers:
            for i in range(9):
                for j in range(9):
                    answer = solution[i][j]
                    if puzzle_board[i][j] == 0:
                        x = MARGIN + j * SIDE + SIDE/2
                        y = MARGIN + i * SIDE + SIDE/2
                        self.canvas.create_text(
                            x,y, text=answer, tags="numbers", fill="sea green"
                        )
        pass

    def __clear_all(self):
        pass

    def __user_inputs(self):
        pass

root = Tk()
SudokuGame = SudokuUI(root)
root.geometry(f"{WIDTH}x{HEIGHT+40}")
root.mainloop()