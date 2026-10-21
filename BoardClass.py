# BoardClass.py
""" Class for instances of 8puzzle Boards
"""
  
import string

class BoardClass():
    """NxN board to solve [(N^2)-1]-puzzle"""

    # class members (all instances/objects use these same values)
    N = 3

    GOAL  = [ [0, 1, 2], [3, 4, 5], [6, 7, 8] ]

    # used with Manhatten Distance heuristic only:
    #    hash table of (row,col) locations for each tile
    #    (set in initializeBoard() below)
    #    e.g.  BoardClass.GoalTiles[0] = [0,0]
    GoalTiles = {}


    #=====================================================
    def __init__(self):
        """CTOR
        """

        # setup board (set bogus values)
        self.Board = [ [-1, -1, -1], [-1, -1, -1], [-1, -1, -1] ]
        # (X,Y) = current location of the EMPTY TILE (0)
        self.X = -1   # ROW
        self.Y = -1   # COL

        # root
        self.Parent = None

        import math
        self.Heuristic = 0
        self.Score = 0


    #=====================================================
    def copyCTOR(self):
        """Copy CTOR
        """
        newBoard = BoardClass()
        newBoard.Board = []
        for nextRow in self.Board:
            newRow = []
            for nextTile in nextRow:
                newRow.append(nextTile)
            newBoard.Board.append(newRow)
        newBoard.X = self.X
        newBoard.Y = self.Y
        newBoard.Parent = self.Parent
        newBoard.Heuristic = self.Heuristic
        newBoard.Score = self.Score
        return newBoard

    #=====================================================
    def isSolveable(self : BoardClass) -> int:
        """Check if the current board is solveable (i.e. can be solved to reach the GOAL board)
        """

        # count number of inversions
        inversions = 0
        for row in range(0, BoardClass.N):
            for col in range(0, BoardClass.N):
                tile = self.Board[row][col]
                if (tile != 0):  # don't count the empty tile
                    for nextRow in range(row, BoardClass.N):
                        startCol = col + 1 if (nextRow == row) else 0
                        for nextCol in range(startCol, BoardClass.N):
                            nextTile = self.Board[nextRow][nextCol]
                            if (nextTile != 0):  # don't count the empty tile
                                if (tile > nextTile):
                                    inversions += 1
                

        #print("Inversions: ", inversions)

        return (inversions % 2 == 0)
    #=====================================================
    def randomizeBoard(self):
        """Randomly shuffle the board (and set the location of the empty tile)"""
        import random

        # create a list of all tiles (0-8)
        allTiles = []
        for row in range(0, BoardClass.N):
            for col in range(0, BoardClass.N):
                allTiles.append(self.Board[row][col])

        # shuffle the list
        random.shuffle(allTiles)

        # put the shuffled tiles back into the board
        for row in range(0, BoardClass.N):
            for col in range(0, BoardClass.N):
                self.Board[row][col] = allTiles.pop()
                if (self.Board[row][col] == 0):
                    self.X = row
                    self.Y = col
    #=====================================================
    def calculateHeuristic(self, heuristicType : str) -> int:
        """Calculate the heuristic value for the current board based on the specified heuristic type."""
        if heuristicType == "Misplaced":
            return self.getHeuristic_MisplacedTiles(BoardClass.GOAL)
        elif heuristicType == "Manhattan":
            return self.computeDistanceFromGoal()
        else:
            return 0 # Default case if heuristic type is not recognized
    #=====================================================
    def initializePuzzleBoard(self, heuristicType : str) -> int: 
        """Set actual (row,col) locations for each tile in the GOAL board
        and initialize the starting board"""

        #Initialize the board to a random state (and set the location of the empty tile)
        self.Board = [ [0, 1, 2], [3, 4, 5], [6, 7, 8] ]

        while True:
            # set (row,col) locations for each tile in the GOAL
            self.randomizeBoard()

            for row in range(0, BoardClass.N):
                for col in range(0, BoardClass.N):
                    BoardClass.GoalTiles[ BoardClass.GOAL[row][col] ] = [row, col]

            """Starting board set up"""
            # should be random when doing experiments (2do)

            #easy (4 moves)
            #self.Board = [ [3, 1, 2], [4, 7, 5], [6, 8, 0] ]

            # starting location of OPEN (0) tile
            #self.X = 2
            #self.Y = 2

            #medium
            #self.Board = [ [3, 2, 5], [4, 1, 8], [6, 0, 7] ]
            #self.X = 2
            #self.Y = 1
            # X and Y mean where is the blank tile

            # hard
            #self.Board = [ [1, 4, 5], [3, 0, 2], [6, 7, 8] ]
            #self.X = 1
            #self.Y = 1

            assert ( self.Board[self.X][self.Y] == 0 )

            if (self.isSolveable()):
                break
            else:
                print("Board in NOT solveable state, re-initialize ...")

        self.Heuristic = self.calculateHeuristic(heuristicType)
        self.Score = self.Heuristic

    #=====================================================
    def createChildrenBoards(self, heuristicType : str) -> int:
        """ Creates the set of potential children Boards from the current Board """
        row = self.X
        col = self.Y

        assert( (row >=0 and row < BoardClass.N)
                and
                (col >=0 and col < BoardClass.N) )

        newChildrenBoards = []

        parentPathScore = self.Score - self.Heuristic
        childPathScore = parentPathScore + 1

        # UP(NORTH): slide empty (0) space up
        if ( row != 0 ):
            newBoard = self.copyCTOR()
            newBoard.Parent = self
            newBoard.Board[row-1][col], newBoard.Board[row][col] = newBoard.Board[row][col], newBoard.Board[row-1][col]
            newBoard.X = row-1
            newBoard.Heuristic = newBoard.calculateHeuristic(heuristicType)
            newBoard.Score = childPathScore + newBoard.Heuristic
            newChildrenBoards.append( newBoard )

        # RIGHT(EAST): slide empty (0) space to right
        if ( col != (self.N - 1) ):
            #print("Try East ...")
            newBoard = self.copyCTOR()
            newBoard.Parent = self
            newBoard.Board[row][col+1], newBoard.Board[row][col] = newBoard.Board[row][col], newBoard.Board[row][col+1]
            newBoard.Y = col+1
            newBoard.Heuristic = newBoard.calculateHeuristic(heuristicType)
            newBoard.Score = childPathScore + newBoard.Heuristic
            newChildrenBoards.append( newBoard )


        # DOWN(SOUTH): slide empty (0) space down
        if ( row != (self.N - 1) ):
            #print("Try South ...")
            newBoard = self.copyCTOR()
            newBoard.Parent = self
            newBoard.Board[row+1][col], newBoard.Board[row][col] = newBoard.Board[row][col], newBoard.Board[row+1][col]
            newBoard.X = row+1
            newBoard.Heuristic = newBoard.calculateHeuristic(heuristicType)
            newBoard.Score = childPathScore + newBoard.Heuristic
            newChildrenBoards.append( newBoard )

        # LEFT(WEST): slide empty (0) space to left
        if ( col != 0 ):
            #print("Try West ...")
            newBoard = self.copyCTOR()
            newBoard.Parent = self
            newBoard.Board[row][col-1], newBoard.Board[row][col] = newBoard.Board[row][col], newBoard.Board[row][col-1]
            newBoard.Y = col-1
            newBoard.Heuristic = newBoard.calculateHeuristic(heuristicType)
            newBoard.Score = childPathScore + newBoard.Heuristic
            newChildrenBoards.append( newBoard )
            

        return newChildrenBoards

    #=====================================================
    def computeDistanceFromGoal(self) -> int:
        """Computes the Manhatten Distance from the Goal board,
        where Manhatten Distance = (sum of misplaced distances for all tiles)"""

        sum = 0

        for row in range(0, BoardClass.N):
            for col in range(0, BoardClass.N):
                tile = self.Board[row][col]
                if (tile != 0):  # don't count the empty tile
                    goalRow = BoardClass.GoalTiles[tile][0]
                    goalCol = BoardClass.GoalTiles[tile][1]


                    sum += abs(row - goalRow) + abs(col - goalCol)


        self.ManhattenDistance = sum

        return sum

        #print self
        #print "Manhatten Distance: ", sum
        #junk = raw_input("Slowing Down (hit enter to continue) ....")

    #=====================================================
    def __str__(self) -> None:
        """ Prints the current Board positions """

        print("-------------")
        print("| %d | %d | %d |" % (self.Board[0][0], self.Board[0][1], self.Board[0][2]))
        print("-------------")
        print("| %d | %d | %d |" % (self.Board[1][0], self.Board[1][1], self.Board[1][2]))
        print("-------------")
        print("| %d | %d | %d |" % (self.Board[2][0], self.Board[2][1], self.Board[2][2]))
        print("-------------")

        return ""

    #=====================================================
    def getHeuristic_MisplacedTiles(self, other) -> int:
       """ H = misplacedTiles """
       
       numberMisplaced = 0

       for row in range(0, BoardClass.N):
           for col in range(0, BoardClass.N):
               if (self.Board[row][col] != other[row][col]):
                   numberMisplaced += 1
       

       #print "EQ: ", numberMisplaced
       return (numberMisplaced)

    #=====================================================
    def sameBoard(self, otherBoard) -> bool:
        """Check if two boards are exactly identical in tile placement;
        (note that this is different from metric of __eq__
        """


        for row in range(0, BoardClass.N):
            for col in range(0, BoardClass.N):
                if (self.Board[row][col] != otherBoard.Board[row][col]):
                    return False

        return True
    

    """ if you use a priority queue, you probably won't need to implement the
        RELATIONAL operators below; however, if you do need to compare two boards:
        if (Board1 > Board2):   # test by Board1.Heuristic < Board2.Heuristic
        then you must implement each relational operator
    """

    #=====================================================
    def __eq__(self, other) -> bool:

        same = False  # assume the worst


        return (self.Heuristic == other.Heuristic)

   #=====================================================
    def __ne__(self, other) -> bool:

        same = False  # assume the worst


        return (self.Heuristic != other.Heuristic)

    #=====================================================
    def __lt__(self, other) -> bool:

        same = False  # assume the worst

        return (self.Heuristic < other.Heuristic)

    #=====================================================
    def __le__(self, other) -> bool:

        same = False  # assume the worst


        return (self.Heuristic <= other.Heuristic)
