# Class generates Sudoku boards, stores them and solves them.
import random
import copy

class SudokuBoard():

    def __init__(self):
        self.empty_board = []
        self.solved_board = []
        self.puzzle_board = [[0 for i in range(9)] for j in range(9)]
        self.solver_message = ""
        
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
        # Generates a randomised first line to be the seed_row
        # Then the remainder is zeroed
        # Boards are solved from this
        seed_row_initial = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        board = [[0 for i in range(9)] for j in range(9)]
        random.shuffle(seed_row_initial)
        board[0] = seed_row_initial
        return board
        
    def find_empty(self, board):
        # Find empty cells
        for row in range(0, 9):
            for col in range(0, 9):
                if board[row][col] == 0: return row, col

        return None
    
    def check_valid(self, board, num, pos):
        # Check if the inputted number is allowed, against rows, columns and squares
        # Check rows
        for i in range(0, 9):
            if board[pos[0]][i] == num and pos[1] != i:
                return False
        
        # Check columns
        for i in range(0, 9):
            if board[i][pos[1]] == num and pos[0] != i:
                return False
        
        # Check squares
        square_x = pos[1] // 3
        square_y = pos[0] // 3

        for i in range(square_y*3, square_y*3 + 3):
            for j in range(square_x*3, square_x*3 + 3):
                if board[i][j] == num and (i,j) != pos:
                    return False
        
        return True

    def solve_board(self, board, visual=False):
        # Backtracking algorithm
        # Find empty cell in 9 x 9 grid

        empty_squares = self.find_empty(board)
        if not empty_squares:
            self.solved_board = board
            return True # If there are no empty squares, it is solved
        else:
            row, col = empty_squares
        
        for i in range(1, 10):
            if self.check_valid(board, i, (row, col)):
                board[row][col] = i # Generate valid numbers and place in the empty squares

                if self.solve_board(board):
                    self.solved_board = board
                    return True # Check if the board has been solved after placing values
                    

                board[row][col] = 0 # If not, then reset the previous number

    def remove_nums(self, board, r_num=25):
        # Remove up to x numbers in board using the board and selected number to remove.
        # Generates a puzzle board
        # Deep Copying is necessary to sotre the solution and puzzle seperately.
        removed_board = copy.deepcopy(board)
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

            removed_board[x][y] = 0
    
        return removed_board


    def get_solved_board(self):
        return self.solved_board
    
    def get_puzzle_board(self):
        return self.puzzle_board

    def gen_puzzle_board(self):
        # Generate a puzzle board in one function
        # Stores the solution for the generated puzzle board in the class
        board = self.gen_board()
        self.solve_board(board)
        solution = self.get_solved_board()
        puzzle_board = self.remove_nums(board) # Turn board into a puzzle
        
        return puzzle_board, solution

    def disp_board(self, board):
        for i in range(len(board)): print(board[i])
    
    def get_solver_message(self):
        return self.solver_message
    

sudoku = SudokuBoard()

puzzle, solution = sudoku.gen_puzzle_board()

print("\nOriginal Puzzle: \n")
sudoku.disp_board(solution)

print("\nPuzzle to be solved:\n")
sudoku.disp_board(puzzle)


