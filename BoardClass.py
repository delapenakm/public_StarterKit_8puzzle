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
        self.Heuristic = math.inf


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

        newBoard.ManhattenDistance = self.ManhattenDistance

        return newBoard

    #=====================================================
    def initializePuzzleBoard(self):
        """Set actual (row,col) locations for each tile in the GOAL board
        and initialize the starting board"""

        # set (row,col) locations for each tile in the GOAL
        for row in range(0, BoardClass.N):
            for col in range(0, BoardClass.N):
                BoardClass.GoalTiles[ BoardClass.GOAL[row][col] ] = [row, col]

        """Starting board set up"""
        # should be random when doing experiments (2do)

        #easy (4 moves)
        self.Board = [ [3, 1, 2], [4, 7, 5], [6, 8, 0] ]

        # starting location of OPEN (0) tile
        self.X = 2
        self.Y = 2

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

        self.computeDistanceFromGoal()

    #=====================================================
    def createChildrenBoards(self):
        """ Creates the set of potential children Boards from the current Board """
        row = self.X
        col = self.Y

        assert( (row >=0 and row < BoardClass.N)
                and
                (col >=0 and col < BoardClass.N) )

        newChildrenBoards = []

        # UP(NORTH): slide empty (0) space up
        if ( row != 0 ):
            print("Try North ...")
            newBoard = self.copyCTOR()
            newBoard.Parent = self
            newBoard.Board[row-1][col], newBoard.Board[row][col] = newBoard.Board[row][col], newBoard.Board[row-1][col]
            newBoard.X = row-1
            newChildrenBoards.append( newBoard )

        # RIGHT(EAST): slide empty (0) space to right
        if ( col != (self.N - 1) ):
            print("Try East ...")
            newBoard = self.copyCTOR()
            newBoard.Parent = self
            newBoard.Board[row][col+1], newBoard.Board[row][col] = newBoard.Board[row][col], newBoard.Board[row][col+1]
            newBoard.Y = col+1
            newChildrenBoards.append( newBoard )


        # DOWN(SOUTH): slide empty (0) space down
        if ( row != (self.N - 1) ):
            print("Try South ...")
            newBoard = self.copyCTOR()
            newBoard.Parent = self
            newBoard.Board[row+1][col], newBoard.Board[row][col] = newBoard.Board[row][col], newBoard.Board[row+1][col]
            newBoard.X = row+1
            newChildrenBoards.append( newBoard )

        # LEFT(WEST): slide empty (0) space to left
        if ( col != 0 ):
            print("Try West ...")
            newBoard = self.copyCTOR()
            newBoard.Parent = self
            newBoard.Board[row][col-1], newBoard.Board[row][col] = newBoard.Board[row][col], newBoard.Board[row][col-1]
            newBoard.Y = col-1
            newChildrenBoards.append( newBoard )
            

        return newChildrenBoards

    #=====================================================
    def computeDistanceFromGoal(self):
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

        #print self
        #print "Manhatten Distance: ", sum
        #junk = raw_input("Slowing Down (hit enter to continue) ....")

    #=====================================================
    def __str__(self):
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
    def getHeuristic_MisplacedTiles(self, other):
       """ H = misplacedTiles """
       
       numberMisplaced = 0

       for row in range(0, BoardClass.N):
           for col in range(0, BoardClass.N):
               if (self.Board[row][col] != other[row][col]):
                   numberMisplaced += 1
       

       #print "EQ: ", numberMisplaced
       return (numberMisplaced)

    #=====================================================
    def sameBoard(self, otherBoard):
        """Check if two boards are exactly identical in tile placement;
        (note that this is different from metric of __eq__
        """

        same = False  # assume the worst

        for row in range(0, BoardClass.N):
            for col in range(0, BoardClass.N):
                if (self.Board[row][col] == otherBoard.Board[row][col]):
                    same = True
                else:
                    same = False
                    break


        return same
    

    """ if you use a priority queue, you probably won't need to implement the
        RELATIONAL operators below; however, if you do need to compare two boards:
        if (Board1 > Board2):   # test by Board1.Heuristic < Board2.Heuristic
        then you must implement each relational operator
    """

    #=====================================================
    def __eq__(self, other):

        same = False  # assume the worst


        return (self.getHeuristic_MisplacedTiles()  == other.getHeuristic_MisplacedTiles())

   #=====================================================
    def __ne__(self, other):

        same = False  # assume the worst


        return (self.getHeuristic_MisplacedTiles() != other.getHeuristic_MisplacedTiles())

    #=====================================================
    def __lt__(self, other):

        same = False  # assume the worst




        return same

    #=====================================================
    def __le__(self, other):

        same = False  # assume the worst




        return same
