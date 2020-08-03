# Generate a Sudoku Board
import random

class SudokuBoard():

    def __init__(self):
        self.board = []
        # Other stuff...

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
                

    def gen_numbers(self):
        # Generate a 9 x 9 board
        # Generate individual lines via randomising the seed, three numbers at a time.
        seed_row_initial = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        lines = []

        # generate empty list of lists
        for i in range(9):
            lines.append([0])
            
        random.shuffle(seed_row_initial)
        lines[0] = self.shuffle_row(seed_row_initial)
        print(f"Sudoku Row 1: {lines[0]}")

        for ind in range(1, len(lines)):
            lines[ind] = self.shuffle_row(lines[ind-1]) # Take the previous row, shuffle and apply to current row.
            print(f"Sudoku Row {ind+1}: {lines[ind]}")
        
        self.board = lines  # Use generated lines for the board
        
    
    def check_board(self):
        # Check Board is Full.
        for row in range(0, 9):
            for col in range(0, 9):
                if self.board[row][col] == 0:
                    return False

        return True
    
    def check_square(self, board, rmin, rmax):
        # Check squares by row
        square = []
        if col<3:
            square = [board[i][0:3] for i in range(rmin, rmax)]
        elif col<6:
            square = [board[i][3:6] for i in range(rmin, rmax)]
        else:
            square = [board[i][6:9] for i in range(rmin, rmax)]
        return square

    def solve_board(self):
        board = self.board
        # Find next empty cell
        for i in range(0, 81):
            row = i//9  # Approximate row by rounding down
            col = i%9   # Approximate column by remainder
            for value in range(1,10):
                if not(value in board[row]): # Check if the number exists in the row
                    if not value in (for ind in range(0,8): board[ind][col]): # Check if the value exists in the columns
                        # Determine which of the 9 squares this area is in
                        square = []
                        if row<3:
                            square = check_square(board, 0, 3)
                        elif row<6:
                            square = check_square(board, 3, 6)
                        else:
                            square = check_square(board, 6, 9)
                        
                        # Check if the value has been used in this 3x3 square
                        if not value in (square[0] + square[1] + square[2]):
                            board[row][col] = value

    def remove_nums(self):
        pass

    def disp_board(self):
        pass

board = SudokuBoard()
board.gen_numbers()