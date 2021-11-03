# sudoku_solver
Project written in Python

Sudoku_Solver generates text based boards based on a seed row (1-9) that is randomised. Boards are generated with as solved. Solver method and can have varied difficulty.

Difficulty scales based on how many values are removed from the pre-generated and pre-solved board.

Sudoku_gui generates a GUI using Tkinter that imports boards generated in Sudoku_Solver and provides a GUI.

Users can attempt to solve the GUI puzzle by clicking and entering numbers between 1 and 9. Correct values are automatically locked in and coloured green.

Alternatively, the board can demonstrate backtracking and solve the puzzle. The 'backtracking' compares the guess values to the already known solved value - used to simulate the program solving itself.
