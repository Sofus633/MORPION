from usefulfunctions import *

def checklines(actualboard):
    posible = actualboard[0][0]
    for val in actualboard:
        for value in val :
            print(posible , value)
            if posible == value:
                posible = value
            else:
                posible = None
        if posible != None:
            return posible
    return None

def checkcolumn(actualboard):
    possible = actualboard[0][0]  
    for row in actualboard:
        if row[0] != possible:  
            return None
    return possible

def chackall(actualboard):
    colones = checkcolumn(actualboard)
    lines = checklines(actualboard)
    return colones if colones != None else lines

test_cases = [
    ([[1, 1, 1], [1, 4, 5], [0, 6, 7]], 1),  # All same in the first column
    ([[1, 2, 7], [2, 4, 7], [3, 6, 7]], 7),  # Different values in column
    ([[1, 2, 3]], 1),  # Single row
    ([[1], [1], [1]], 1),  # Single column
    ([[None, 2, 3], [None, 4, 5], [None, 6, 7]], None),  # None values in column
    ([[5, 2], [5, 4], [5, 6]], 5),  # All same values in the first column
    ([[3, 7], [8, 7], [3, 9]], None),  # Mixed values in the first column
    ([[1], [2], [1]], None),  # Two different values in a single column
    ([[0, 0, 0], [0, 0, 0], [0, 0, 0]], 0),  # All zeros in the first column
    ([[1, 2], [1, 2], [1, 3]], 1),  # First column same, second column different
    ([[1, 1], [1, 2], [1, 3]], 1),  # First column same, second column different
    ([[1, 1], [2, 1], [1, 1]], None),  # Only one element in first column differs
]

for i, (board, expected) in enumerate(test_cases):
    result = chackall(board)
    assert result == expected, f"Test case {i + 1} failed: expected {expected}, got {result}"
