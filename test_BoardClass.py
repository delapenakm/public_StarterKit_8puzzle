# Unit Testing for the 8-Puzzle Project
# Some of these unit tests were created with the help of ChatGPT, as
# I had some issues with implementing

import pytest

from BoardClass import *

def test_board_initialization():
    """Test that Board Class initalizes the board correctly."""
    board = BoardClass()
    assert board.Board == [[-1, -1, -1], [-1, -1, -1], [-1, -1, -1]] # Check if board is in Goal State

def test_randomize_board():
    """Test that Board Class randomizes the board correctly."""
    board = BoardClass()
    board.randomizeBoard()
    assert board.Board != [[0, 1, 2], [3, 4, 5], [6, 7, 8]] # Check if board is not in Goal State

def test_is_goal_state():
    """Test that Board Class correctly identifies the goal state."""
    board = BoardClass()
    board.Board = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
    assert board.Board == board.GOAL # Check if board is in Goal State

    board.randomizeBoard()
    assert board.Board != board.GOAL # Check if board is not in Goal State

def test_calculate_heuristic():
    """Test that Board Class correctly calculates the heuristic."""
    board = BoardClass()

    for row in range(BoardClass.N):
        for col in range(BoardClass.N):
            BoardClass.GoalTiles[BoardClass.GOAL[row][col]] = [row, col]

    board.Board = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
    
    board.Heuristic = board.calculateHeuristic("Misplaced")
    assert board.Heuristic == 0

    board.Heuristic = board.calculateHeuristic("Manhattan")
    assert board.Heuristic == 0

    board.randomizeBoard()

    board.Heuristic = board.calculateHeuristic("Misplaced")
    assert board.Heuristic > 0

    board.Heuristic = board.calculateHeuristic("Manhattan")
    assert board.Heuristic > 0  

def test_is_solveable():
    """Test whether a board is solvable."""
    board = BoardClass()

    board.Board = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
    assert board.isSolveable() == True

    board.Board = [[1, 0, 2], [3, 4, 5], [6, 7, 8]]
    assert board.isSolveable() == True

    board.Board = [[0, 2, 1], [3, 4, 5], [6, 7, 8]]
    assert board.isSolveable() == False

def test_same_board():
    """Test whether two boards have the same arrangement."""
    board1 = BoardClass()
    board2 = BoardClass()

    board1.Board = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
    board2.Board = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]

    assert board1.sameBoard(board2) == True

    board2.Board = [[1, 0, 2], [3, 4, 5], [6, 7, 8]]
    assert board1.sameBoard(board2) == False

def test_copy_board():
    """Test that a board is copied correctly."""
    board = BoardClass()
    board.Board = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
    board.X = 0
    board.Y = 0

    copiedBoard = board.copyCTOR()

    assert copiedBoard.Board == board.Board
    assert copiedBoard is not board
    assert copiedBoard.X == board.X
    assert copiedBoard.Y == board.Y

    copiedBoard.Board[0][0] = 8
    assert board.Board[0][0] == 0

def test_create_children_boards():
    """Test that the correct number of child boards is generated."""
    board = BoardClass()

    for row in range(BoardClass.N):
        for col in range(BoardClass.N):
            BoardClass.GoalTiles[BoardClass.GOAL[row][col]] = [row, col]

    # Blank in the top-left corner
    board.Board = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
    board.X = 0
    board.Y = 0
    board.Heuristic = board.calculateHeuristic("Manhattan")
    board.Score = board.Heuristic

    children = board.createChildrenBoards("Manhattan")
    assert len(children) == 2

    # Blank in the center
    board.Board = [[1, 2, 3], [4, 0, 5], [6, 7, 8]]
    board.X = 1
    board.Y = 1
    board.Heuristic = board.calculateHeuristic("Manhattan")
    board.Score = board.Heuristic

    children = board.createChildrenBoards("Manhattan")
    assert len(children) == 4
