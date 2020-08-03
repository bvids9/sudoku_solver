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
        self.empty_board = self.sudoku.gen_board()

        # UI Code
        Frame.__init__(self, parent)
        self.parent = parent
        self.disp_row, self.disp_col = -1, -1

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

        # TODO: Add Clear Answers Button
        # TODO: Add Solve Button

        self.__draw_grid()


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


    def __draw_numbers(self, difficulty, original=False, answers=False, visual_solve=False):
        # Load numbers into the board
        self.canvas.delete("numbers")
        # TODO: Change difficulty levels
        # Consider refactoring the board_generation into a seperate function.
        puzzle_board, solution = self.sudoku.gen_puzzle_board(level=difficulty)

        if original:    # Load in original numbers
            for i in range(9):
                for j in range(9):
                    answer = puzzle_board[i][j]
                    if answer != 0:
                        x = MARGIN + j * SIDE + SIDE/2
                        y = MARGIN + i * SIDE + SIDE/2
                        self.canvas.create_text(
                            x,y, text=answer, tags="numbers", fill="black"
                        )
                        self.update()   #Tkinter.update function to refresh screen
                        time.sleep(delay)
        if answers:
            for i in range(9):
                for j in range(9):
                    answer = solution[i][j]
                    if puzzle_board[i][j] == 0:
                        x = MARGIN + j * SIDE + SIDE/2
                        y = MARGIN + i * SIDE + SIDE/2
                        self.canvas.create_text(
                            x,y, text=answer, tags="solution", fill="sea green"
                        )
                        self.update()
                        time.sleep(delay)

        
        # Code to generate the iteration and solving.
        # Will need to generate another internal function
    
    def draw_command(self):
        # Call the draw_numbers function for the button
        self.__draw_numbers(difficulty="medium", original=True)
    
    def draw_answers_command(self):
        # Call the draw_numbers function for answer button
        self.__draw_numbers(difficulty="medium", original=False, answers=True)

    def visual_solver(self, board):
        # Function for the visual solving
        pass

    def __clear_all(self):
        pass

    def __user_inputs(self):
        pass

root = Tk()
SudokuGame = SudokuUI(root)
root.geometry(f"{WIDTH}x{HEIGHT+40}")
root.mainloop()