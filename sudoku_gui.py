from tkinter import Tk, Canvas, Frame, Button, BOTH, TOP, BOTTOM
import time
from sudoku_solver import SudokuBoard

MARGIN = 20
SIDE = 50
WIDTH = HEIGHT = MARGIN * 2 + SIDE * 9
delay = 0.1

class SudokuUI(Frame):
    def __init__(self, parent):

        # Load an initial board
        self.sudoku = SudokuBoard()

        # UI Code
        Frame.__init__(self, parent)
        self.parent = parent
        self.disp_row, self.disp_col = -1, -1

        self.board_loaded = False

        self.__generate_interface()

        pass

    def __generate_interface(self):
        # Generate Tkinter window
        # Generate interface elements, including buttons

        self.parent.title("Sudoku Solver")
        self.pack(fill=BOTH)
        self.canvas = Canvas(self,
                            width=WIDTH,
                            height=HEIGHT)
        self.canvas.pack(fill=BOTH, side=TOP)

        draw_button = Button(self, 
                            text="Load New Puzzle", 
                            command=self.draw_command)

        draw_button.pack(fill=BOTH, side=BOTTOM)

        solve_button = Button(self,
                            text="Solve Puzzle",
                            command=self.draw_answers_command)
        solve_button.pack(fill=BOTH, side=BOTTOM)

        # TODO: Add Clear Answers Button
        # TODO: Add Solve Button

        self.__draw_grid()
        self.puzzle_board, self.solution = self.__get_board()

    def __get_board(self):
        puzzle_board, solution = self.sudoku.gen_puzzle_board(level="medium")
        return puzzle_board, solution

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

    def __get_num_coords(self, i, j):
        # Get coordinates for text generation
        x = MARGIN + j * SIDE + SIDE/2
        y = MARGIN + i * SIDE + SIDE/2

        return (x,y)

    def __draw_numbers(self, difficulty, original=False, answers=False, visual_solve=False):
        # Load numbers into the board
        self.canvas.delete("numbers")
        self.canvas.delete("solution")
        # TODO: Change difficulty levels

        # Loads new board
        self.puzzle_board, self.solution = self.__get_board()

            # Load in original numbers
            # Consider refactoring the below...
        for i in range(9):
            for j in range(9):
                answer = self.puzzle_board[i][j]
                if answer != 0:
                    x, y = self.__get_num_coords(i,j)
                    self.canvas.create_text(
                        x,y, text=answer, tags="numbers", fill="black"
                    )
                    self.update()   #Tkinter.update function to refresh screen
                    time.sleep(delay)
        self.board_loaded = True

        # Consider seperating out for a solution drawing
    def __draw_solution(self):
        if self.board_loaded:
            for i in range(9):
                for j in range(9):
                    answer = self.solution[i][j]
                    if self.puzzle_board[i][j] == 0:
                        x, y = self.__get_num_coords(i,j)
                        self.canvas.create_text(
                            x,y, text=answer, tags="solution", fill="sea green"
                        )
                        self.update()
                        time.sleep(delay)

        
        # TODO: Code to generate the iteration and solving.
        #       Will need to generate another internal function to do the backtracking.
    
    def draw_command(self):
        # Call the draw_numbers function for the button
        self.__draw_numbers(difficulty="medium", original=True)
    
    def draw_answers_command(self):
        # Call the draw_numbers function for answer button
        self.__draw_solution()

    def visual_solver(self, board):
        # Function for the visual solving
        pass

    def __clear_all(self):
        pass

    def __user_inputs(self):
        pass

root = Tk()
SudokuGame = SudokuUI(root)
root.geometry(f"{WIDTH}x{HEIGHT+120}")
root.mainloop()