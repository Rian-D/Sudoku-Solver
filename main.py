import numpy as np

def find_empty_location(sudoku):
    """
    Finds an empty cell (with value 0) in the Sudoku grid.
    Returns the row and column index as a tuple, or None if no empty cells are found.
    """
    for row in range(9):
        for col in range(9):
            if sudoku[row, col] == 0:
                return row, col
    return None

def is_valid(sudoku, num, row, col):
    """
    Checks if placing `num` in `sudoku[row][col]` is valid.
    """
    # Check the row
    if num in sudoku[row, :]:
        return False

    # Check the column
    if num in sudoku[:, col]:
        return False

    # Check the 3x3 grid
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    if num in sudoku[start_row:start_row + 3, start_col:start_col + 3]:
        return False

    return True

def find_best_empty_location(sudoku):
    """
    Finds the best empty cell (with value 0) to fill by using the minimum remaining values (MRV) heuristic.
    Returns the row and column index as a tuple, or None if no empty cells are found.
    """
    best_location = None
    min_options = 10  # More than the maximum possible options (1-9)

    for row in range(9):
        for col in range(9):
            if sudoku[row, col] == 0:
                options = [num for num in range(1, 10) if is_valid(sudoku, num, row, col)]
                if len(options) < min_options:
                    min_options = len(options)
                    best_location = (row, col)

    return best_location

def solve_sudoku(sudoku):
    """
    Solves the Sudoku puzzle using backtracking with improved heuristics.
    """
    empty_location = find_best_empty_location(sudoku)
    if not empty_location:
        return True  # No empty cells left, puzzle solved

    row, col = empty_location

    for num in range(1, 10):
        if is_valid(sudoku, num, row, col):
            # Place the number
            sudoku[row, col] = num

            # Recursively solve the rest of the puzzle
            if solve_sudoku(sudoku):
                return True

            # Backtrack
            sudoku[row, col] = 0

    return False

def is_valid_sudoku(sudoku):
    """
    Validates the input Sudoku grid to ensure no duplicate numbers
    in any row, column, or 3x3 subgrid.
    """
    for row in range(9):
        if not is_unique(sudoku[row, :]):
            return False

    for col in range(9):
        if not is_unique(sudoku[:, col]):
            return False

    for start_row in range(0, 9, 3):
        for start_col in range(0, 9, 3):
            subgrid = sudoku[start_row:start_row + 3, start_col:start_col + 3].flatten()
            if not is_unique(subgrid):
                return False

    return True

def is_unique(array):
    """
    Helper function to check if an array contains unique non-zero values.
    """
    array = array[array > 0]  # Exclude zeros
    return len(array) == len(set(array))

def sudoku_solver(sudoku):
    """
    Entry point for solving a Sudoku puzzle. Takes a 9x9 NumPy array as input and returns the solved puzzle.
    If no solution exists or the input is invalid, returns a 9x9 array with all values set to -1.
    """
    if not is_valid_sudoku(sudoku):
        print("Invalid Sudoku input.")
        return np.full((9, 9), -1)

    # Make a copy to avoid modifying the original input
    sudoku_copy = sudoku.copy()

    if solve_sudoku(sudoku_copy):
        return sudoku_copy
    else:
        return np.full((9, 9), -1)
