# sudoku_solver
Project written in Python

Project used to practice Tkinter (first attempt at a GUI with Python.)

Sudoku_Solver generates text based boards based on a seed row (1-9) that is randomised. Boards are generated with as solved. Solver method and can have varied difficulty.

Difficulty scales based on how many values are removed from the pre-generated and pre-solved board.

Sudoku_gui generates a GUI using Tkinter that imports boards generated in Sudoku_Solver and provides a GUI.

Users can attempt to solve the GUI puzzle by clicking and entering numbers between 1 and 9. Correct values are automatically locked in and coloured green.

Alternatively, the board can demonstrate backtracking and solve the puzzle. Backtracking is a blind solution, the program will attempt to solve itself and stop when it finds a value that satisfies the current state of the row. It will continue forward until it either solves the board or runs out of valid values (then begins backtracking).


![image](https://user-images.githubusercontent.com/64046690/166142170-a86252ef-59c9-4d90-bc55-85751fbee733.png)

