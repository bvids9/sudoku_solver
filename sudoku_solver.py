# Generate a Sudoku Board
import random
import time
from tkinter import Tk, Canvas, Frame, Button, BOTH, TOP, BOTTOM

margin = 20
side = 50
width = height = margin * 2 + side * 9

class SudokuBoard(Frame):

    def __init__(self, parent):
        self.empty_board = []
        self.solved_board = []
        self.puzzle_board = [[0 for i in range(9)] for j in range(9)]
        self.solver_message = ""
        
        # UI_stuff
        Frame.__init__(self, parent)
        self.parent = parent

        self.disp_row, self.disp_col = -1, -1
        
        self.__generate_interface()

    def __generate_interface(self):
        # Generate the tkinter interface
        self.parent.title("Sudoku - Solver")
        self.pack(fill=BOTH)
        self.canvas = Canvas(self, 
                            width=width,
                            height=height)
        
        self.canvas.pack(fill=BOTH, side=TOP)

        # Load Puzzle button
        load_button = Button(self,
                            text="Load Puzzle",
                            command=self.__load_board)
        load_button.pack(fill=BOTH,side=TOP)

        # TODO: Solve button
        solve_button = Button(self,
                             text="Solve Puzzle",
                             command=self.solve_board(self.puzzle_board)
        )

        solve_button.pack(fill=BOTH,side=TOP)
        # TODO: Finish Clear Button
        clear_button= Button(self,
                            text="Clear Answers",
                            command=self.clear_all)
        clear_button.pack(fill=BOTH,side=BOTTOM)

        self.clear_all()
        self.__draw_grid()
        


    def __draw_grid(self):
        # Draw grid 9x9 with blue lines to divide into 3 x 3 squares

        for i in range(10):
            colour = "blue" if i % 3 == 0 else "gray"

            x0 = margin + i * side
            y0 = margin
            x1 = margin + i * side
            y1 = height - margin

            self.canvas.create_line(x0, y0, x1, y1, fill=colour)

            x0 = margin
            y0 = margin + i * side
            x1 = width - margin
            y1 = margin + i * side
            self.canvas.create_line(x0, y0, x1, y1, fill=colour)

    def __load_board(self):
        # Load the board from the Sudoku class
        self.empty_board = self.gen_board()
        self.solved_board = self.solve_board(self.empty_board)
        
        self.puzzle_board = self.remove_nums(self.solved_board)


        # Draw the puzzle on the board
        self.canvas.delete("numbers")
        # Cycle through the loaded board
        for i in range(9):
            for j in range(9):
                answer = self.puzzle_board[i][j]
                if answer != 0:
                    x = margin + j* side + side / 2
                    y = margin + i * side + side / 2
                    self.canvas.create_text(
                        x, y, text=answer, tags="numbers", fill="black"
                    )


    def clear_all(self):
        # Clear all information and board display
        self.empty_board = []
        self.solved_board = []
        self.puzzle_board = []
        self.solver_message = ""
        self.canvas.delete("numbers")
        self.canvas.delete("solution")
        pass
    
    def user_inputs(self):
        # Handle keypresses and mouse clicks.
        pass

    def fixed_indexes(self):
        # generate three unique numbers to use as shuffling indexes
        fixed_indexes = []
        while len(fixed_indexes) < 3:
            random_int = random.randrange(1, 9)
            if random_int not in fixed_indexes: fixed_indexes.append(random_int)
        # print(f"Fixed indexes: {fixed_indexes}")
        return fixed_indexes
    
    def contains(self, list1, list2):
        # function to cycle through lists and compare entries
        # lists must be equal length
        list1.sort()
        list2.sort()
        contains = False

        for i in range(len(list1)):
            if list1[i] in list2:
                contains = True
        return contains

    def unique_lists(self, list1, list2):
        while self.contains(list1, list2):  # While the lists contain values of each other
            list1 = self.fixed_indexes()   # Change the first list until it isn't.
        return list1, list2
                
    def shuffle_row(self, row):
        # Function works as advertised, however the algorithm needs a rethink.

        # Generate a pair of unique index lists
        ind_a = self.fixed_indexes()
        ind_b = self.fixed_indexes()

        # Make sure they're unique
        ind_a, ind_b = self.unique_lists(ind_a, ind_b)
     
        # print(f"Ind_a is: {ind_a}")
        # print(f"Ind_b is: {ind_b}")

        # Randomise a row using the initial input row
        rand_r1 = row[:] # Reshuffled row   
        rand_r2 = row[:] # Original row

        # print(f"Randomised seed_row: {row}")

        # Cycle through the given row at each index and swap it around.
        for i in range(len(ind_a)):
            rand_r1[ind_a[i]] = rand_r1[ind_b[i]] # Swap in the first row
            rand_r1[ind_b[i]] = rand_r2[ind_a[i]] # Swap using the original as a reference (ie values have been changed)  
        
        # print(f"Reshuffled Row: {rand_r1}")

        return rand_r1
                
    def gen_board(self):
        # Generate a 9 x 9 board
        # Generate individual lines via randomising the seed, three numbers at a time.
        seed_row_initial = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        board = [[0 for i in range(9)] for j in range(9)]
        random.shuffle(seed_row_initial)
        board[0] = seed_row_initial
        return board
        
    def check_board(self, board):
        # Check Board is Full.
        for row in range(0, 9):
            for col in range(0, 9):
                if board[row][col] == 0:
                    return False
        return True
    
    def check_square(self, board, rmin, rmax, col):
        # Check squares by row
        square = []
        if col<3:
            square = [board[i][0:3] for i in range(rmin, rmax)]
        elif col<6:
            square = [board[i][3:6] for i in range(rmin, rmax)]
        else:
            square = [board[i][6:9] for i in range(rmin, rmax)]
        return square

    def solve_board(self, board, visual=False):
        # Backtracking algorithm
        # Find empty cell in 9 x 9 grid
        for ind in range(0, 81):
            row = ind//9  # Approximate row by rounding down, ie 17 // 9 = 1, 18 // 2 = 2...
            col = ind%9   # Approximate column by remainder, ie 17 % 9 = 8

            if board[row][col]==0:  # If cell is empty (ie 0), cycle numbers to fill in it
                for value in range(1,10):
                    # Check if the number exists in the row
                    if not(value in board[row]):
                        # Check column
                        if value not in (board[i][col] for i in range(0,8)):
                            # Determine which of the 9 squares this area is in (eg Square 4 = rows 3-6, col 0-3)
                            square = []
                            if row<3: # Top 3 rows
                                square = self.check_square(board, 0, 3, col)

                            elif row<6: # Middle...
                                square = self.check_square(board, 3, 6, col)

                            else:
                                square = self.check_square(board, 6, 9, col)
                                    
                            # Check if the value has been used in this 3x3 square

                            if not value in (square[0] + square[1] + square[2]):
                                board[row][col] = value

                                if visual==True:
                                    for i in range(9):
                                        for j in range(9):
                                            original_board = self.puzzle_board
                                            answer = original_board[i][j]
                                            x = margin + j* side + side / 2
                                            y = margin + i * side + side / 2
                                            self.canvas.create_text(
                                                x, y, text=value, 
                                                tags="solution", 
                                                fill="sea green")
                                            # time.sleep(0.001)                                    

                                if self.check_board(board):
                                    print("Board solved.")
                                    self.solved_board = board # Record solved board
                                    return board
                                else:
                                    if self.solve_board(board):
                                        return board
                                        self.solved_board = board  # Record solved board

                # If after iterating through the entire board, no valid place to put value is found, exit loop and backtrack
                break
        print("Backtracking...")
        board[row][col] = 0
        self.board = board

    def remove_nums(self, board, r_num=25):
        # Remove up to x numbers in board using the board and selected number to remove.
        # Generates a puzzle board

        remove_row = []
        remove_col = []
        counter = 0
        while counter < r_num:
            x = random.randrange(0, 9)
            y = random.randrange(0, 9)
            if (x, y) not in (remove_row, remove_col): 
                remove_row.append(x)
                remove_col.append(y)
                counter = counter + 1
        
        for i in range(0, r_num):
            x = remove_row[i]
            y = remove_col[i]

            board[x][y] = 0

        self.puzzle_board = board
        return board  

    def get_solved_board(self):
        return self.solved_board
    
    def get_puzzle_board(self):
        return self.puzzle_board

    def disp_board(self, board):
        for i in range(len(board)): print(board[i])
    
    def get_solver_message(self):
        return self.solver_message
    





# Left over tests
root = Tk()
SudokuBoard(root)
root.geometry(f"{width}x{height+100}")
root.mainloop()

# sudoku = SudokuBoard()

# empty_board = sudoku.gen_board()

# solution = sudoku.solve_board(empty_board)

# print("\nOriginal Puzzle: \n")
# sudoku.disp_board(solution)

# puzzle = sudoku.remove_nums(solution)

# print("\nPuzzle to be solved:\n")
# sudoku.disp_board(puzzle)
# 

