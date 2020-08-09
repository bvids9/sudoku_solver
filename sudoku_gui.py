from tkinter import Tk, Canvas, Frame, Button, BOTH, TOP, BOTTOM, Label, font, Message, Toplevel
import time
from sudoku_solver import SudokuBoard

MARGIN = 20 # Margin padding the Grid
SIDE = 50   # Cell side length 
WIDTH = HEIGHT = MARGIN * 2 + SIDE * 9  # Size of Grid
delay = 0.1 # Time delay in seconds



class SudokuUI(Frame):
    def __init__(self, parent):

        # Load an initial board
        self.sudoku = SudokuBoard()

        # UI Code
        Frame.__init__(self, parent)
        self.parent = parent
        self.disp_row, self.disp_col = -1, -1

        self.board_loaded = False
        self.solving = False
        self.solved = False
        self.message_log = ""
        self.user_answer = ""
        self.difficulty = "hard"
        self.set_difficulty = False

        self.__generate_interface()

        pass

    def __generate_interface(self):
        # Generate Tkinter window
        # Generate interface elements, including buttons

        self.parent.title("Sudoku Solver")
        self.parent.resizable(width=False, height=False)
        self.grid(row=0, column=0)
        self.canvas = Canvas(self,
                            width=WIDTH,
                            height=HEIGHT
                            )
        self.canvas.grid(row=0, column=0)

        draw_button = Button(self, 
                            text="Load New Puzzle", 
                            command=self.draw_command)

        draw_button.grid(row=1, column=0, sticky="ew")

        solve_button = Button(self,
                            text="Solve Puzzle",
                            command=self.draw_answers_command)
        solve_button.grid(row=2, column=0, sticky="ew")

        self.lbl_message_log = Message(self, fg="black", bg="gray82", bd=3, width=400)
        self.lbl_message_log.grid(row=3, column=0, sticky="ew")

        self.__draw_grid()

        # Bind functions
        self.canvas.bind("<Button-1>", self.__click_square)
        self.canvas.bind("<Key>", self.__key_press)

    def __get_board(self, level):
        puzzle_board, solution = self.sudoku.gen_puzzle_board(level=level)
        return puzzle_board, solution

    def __draw_grid(self):
        # Draw the initial grid
        # 9 x 9 with blue lines to divide the 3 x 3 squares
        for i in range(10):
            if i % 3 == 0:
                colour = "blue"
                width = 2
            else:
                colour = "gray"
                width = 1

            # Vertical lines
            x0 = MARGIN + i * SIDE
            y0 = MARGIN
            x1 = MARGIN + i * SIDE
            y1 = HEIGHT - MARGIN

            self.canvas.create_line(x0, y0, x1, y1, fill=colour, width=width)

            # Horizontal lines
            x0 = MARGIN
            y1 = MARGIN + i * SIDE
            x1 = WIDTH - MARGIN
            y0 = MARGIN + i * SIDE

            self.canvas.create_line(x0, y0, x1, y1, fill=colour, width=width)

    def __get_num_coords(self, i, j):
        # Get coordinates for text generation
        # Returns middle of cells
        x = MARGIN + j * SIDE + SIDE/2
        y = MARGIN + i * SIDE + SIDE/2

        return (x,y)

    def __init_draw_numbers(self, difficulty, original=False, answers=False, visual_solve=False):
        if not self.solving:
            # Load numbers into the board
            self.canvas.delete("numbers")
            self.canvas.delete("solution")
            self.disp_row, self.disp_col = -1, -1
            self.delete_v_solve()

            # Loads new board
            self.puzzle_board, self.solution = self.__get_board(self.difficulty)

            # Print board to GUI
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
                        self.lbl_message_log['text'] = f"Loading {str(self.difficulty).title()} Board..."
        self.lbl_message_log['text'] = f"{str(self.difficulty).title()} Board Loaded!"
        self.board_loaded = True
        self.solved = False

    def __draw_solver(self, board):

        # Visualisation of the backtracking algorithm
        # A repeat of the sudoku_solver.py function, but broken down to allow visualising

        if not self.solved and self.board_loaded:   # Make sure there is a board loaded AND it hasn't been solved
            self.solving = True
            empty_squares = self.sudoku.find_empty(board)
            if not empty_squares:
                self.lbl_message_log['text'] = "Solved!"
                self.solved = True
                self.solving = False
                return True
            else:
                row, col = empty_squares
            
            for i in range(1, 10):
                # Select the square and display the cycling of solutions
                # Then delete immediately after, if a valid guess is found, the solution code block will enter it.
                x,y = self.__get_num_coords(row, col)

                self.disp_solv_num(i, x,y, row, col, "black")
                self.disp_selection(row, col)
                self.lbl_message_log['text'] = "Guessing..."
                self.update()
                time.sleep(0.05)

                self.canvas.delete(f"v_solve{row}{col}", f"selection{row}{col}")
                
                if self.sudoku.check_valid(board, i, (row, col)):
                    # Get square coordinates and draw the selection to indicate solving
                    x,y = self.__get_num_coords(row, col)
                    self.disp_selection(row, col)
                    self.update()

                    # When solution found, refresh number and selection to green
                    board[row][col] = i
                    self.disp_confirmation(row, col)

                    # Create Tag each generated solution
                    self.disp_solv_num(i, x, y, row, col, "sea green")
                    self.lbl_message_log['text'] = "Solving..."

                    self.update()
                    time.sleep(delay*2)
                    if self.__draw_solver(board): # Recursive function, ie the function calls itself
                        return True

            
                    board[row][col] = 0
                    self.canvas.delete(f"v_solve{row}{col}", f"selection{row}{col}") # Delete if backtracking
                    self.lbl_message_log['text'] = "Backtracking..."

                    self.update()
                    time.sleep(delay*2)

    def delete_v_solve(self):
        # Delete numbers generated by the solver at __draw_solver
        for row in range(0, 9):
            for col in range(0, 9):
                self.canvas.delete(f"v_solve{row}{col}", f"selection{row}{col}")

    def draw_command(self):
        # Call the draw_numbers function for the button
        if not self.solving:
            if self.set_difficulty:
                self.__init_draw_numbers(difficulty=self.difficulty, original=True)
                self.set_difficulty = False
            else:
                self.lbl_message_log['text'] = "Select a puzzle difficulty first."
                self.difficulty_window()

    def difficulty_window(self):
        # Messagebox for selecting the difficulty
        options = Toplevel()
        options.title("Difficulty Setting")
        win_x = self.winfo_rootx()
        win_y = self.winfo_rooty()

        x = int((win_x/2) + (WIDTH/2))+200
        y = int((win_y/2) + (HEIGHT/2))

        options.geometry("300x100+{}+{}".format(x, y))
        message = "Choose your puzzle difficulty"
        Label(options, text=message).pack()

        Button(options, 
                text="Easy - Solve for 25 Numbers", 
                command=lambda:[self.choose_puzzle("easy"), options.destroy(), self.draw_command()]).pack()

        Button(options, text="Medium - Solve for 45 Numbers",
                command=lambda:[self.choose_puzzle("medium"), options.destroy(), self.draw_command()]).pack()

        Button(options, text="Hard - Solve for 64 Numbers", 
                command=lambda:[self.choose_puzzle("hard"), options.destroy(), self.draw_command()]).pack()

    def choose_puzzle(self, level):
        # Assign difficulty level at button press in the messagebox
        self.difficulty = level
        self.set_difficulty = True

    def draw_answers_command(self):
        # Call the draw_numbers function for answer button
        # Wipe previous selection and any pending answers that are incorrect (ie last guess)
        self.canvas.delete(f"selection{self.disp_row}{self.disp_col}", f"v_solve{self.disp_row}{self.disp_col}")
        self.disp_row, self.disp_col = -1, -1   # Reset selection flags
        self.__draw_solver(self.puzzle_board)

    def get_selection_coords(self, row, col):
        
        x0 = MARGIN + col*SIDE
        y0 = MARGIN + row*SIDE
        
        x1 = x0 + SIDE
        y1 = y0 + SIDE

        return x0, y0, x1, y1

    def disp_selection(self, row, col):
        # Draw red rectangle at currently analysed square
        x0, y0, x1, y1 =  self.get_selection_coords(row, col)
        self.canvas.create_rectangle(x0, y0, x1, y1, outline="red", tags=f"selection{row}{col}")
    
    def disp_confirmation(self, row, col):
        # When moving on from the selected square (ie found a correct number), turn rectangle green
        for rectangle in self.canvas.find_withtag(f"selection{row}{col}"): self.canvas.itemconfig(rectangle, outline="green", width=2)
    
    def disp_solv_num(self, number, x, y, row, col, colour):
        # Draw numbers during the solver visualisation as they are generated
        text_font = font.Font(size=11, weight="bold") 
        self.canvas.create_text(
        x,y, text=number,font=text_font, tags=f"v_solve{row}{col}", fill=colour, 
        )
    
    def disp_solution(self):
        # Displays the solution instantly
        # Not a true backtracking or display of how the program works.
        # Currently unused.
        if self.board_loaded:
            self.solving = True
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

        self.solving = False
        
    def __click_square(self, event):
        # Detect if a square has been clicked
        # 0. Make sure the board hasn't been filled or solved
        # 1. Make sure within boundaries
        # 2. Get the coordinates square that is clicked
        # 3. Setup the cursor and display (activate square), if not already selected and if not filled with base puzzle
        # 4. Allow inputs etc etc or deselect if clicked again

        if not self.solved and not self.solving and self.board_loaded:
            mouse_x, mouse_y = event.x, event.y
            #
            if (MARGIN < mouse_x < WIDTH + MARGIN and MARGIN < mouse_y < HEIGHT + MARGIN):
                self.canvas.focus_set()

                row, col = int((mouse_y - MARGIN) / SIDE), int((mouse_x - MARGIN) / SIDE)
                
                # Check if clicking the same square, if yes, deselect it
                if (row, col) == (self.disp_row, self.disp_col):
                    self.canvas.delete(f"selection{row}{col}", f"v_solve{row}{col}")
                    self.disp_row, self.disp_col = -1, -1


                # Check if the square already has values in it and we haven't selected anywhere else
                elif (self.puzzle_board[row][col] == 0 and (self.disp_row, self.disp_col) == (-1, -1)):
                    # print(f"x,y coords are {row, col}\n mouse_x, mouse_y is {mouse_x, mouse_y}")
                    self.disp_selection(row, col)
                    self.lbl_message_log['text'] = ("Square selected. Enter a number...")
                    self.disp_row, self.disp_col = row, col
                    # Allow inputs

    def __key_press(self, event):
        # Make sure not solving, a board is loaded and board is not solved
        if not self.solved and not self.solving and self.board_loaded:
            # Check to make sure that the entered value is valid
            # Draw and update the numbers, grey for placeholder
            solution = self.sudoku.get_solved_board()
            x, y = self.__get_num_coords(self.disp_row, self.disp_col)
            
            # Make sure something is selected
            if (self.disp_row >= 0 and self.disp_col >= 0):
                # Get the number input
                if event.char in "123456789":
                    self.user_answer = int(event.char)
                    self.canvas.delete(f"v_solve{self.disp_row}{self.disp_col}") # Clear out the previous answer
                    self.disp_solv_num(self.user_answer, x, y, self.disp_row, self.disp_col, colour="grey")
                    
                    # Only allow correct numbers
                    if solution[self.disp_row][self.disp_col] == self.user_answer:
                        self.puzzle_board[self.disp_row][self.disp_col] = self.user_answer

                        self.disp_solv_num(self.user_answer, x, y, self.disp_row, self.disp_col, colour="black")
                        self.canvas.delete(f"selection{self.disp_row}{self.disp_col}")
                        self.disp_row, self.disp_col = -1, -1
                        self.lbl_message_log['text'] = (f"{self.user_answer} is correct!")
                        time.sleep(delay)
                        check_empty = self.sudoku.find_empty(self.puzzle_board)

                        if not check_empty:
                            self.lbl_message_log['text'] = (f"Solved!")
                    else:
                        self.lbl_message_log['text'] = (f"{self.user_answer} is incorrect. Try again.")




root = Tk()

# Centre in screen
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

root_x = (screen_width/2) - (WIDTH/2)
root_y = (screen_height/2) - (HEIGHT/2)

SudokuGame = SudokuUI(root)
root.geometry(f"{WIDTH}x{HEIGHT+80}+{int(root_x)}+{int(root_y)}")
root.mainloop()