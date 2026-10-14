
"""
Solve the 8-puzzle using various search algorithms, including
two Best-First algorithms: (1) MisplacedTiles and (2) ManhattenDistance
as heuristics.

# originally implemented in Python v2.x by Kelsey Hichens '13
# converted to v3.x (mdl, 08/01/2012)
      % 2to3 -w code.py

# this code is mostly unfinished (mdl, 09/18/2026)
"""
   
from BoardClass import *

#=====================================================
def main():

    b = BoardClass()
    b.initializePuzzleBoard()

    print("\nStarting Board")
    print(b)

    if ( BestFirstSearch(b) ):
        print("YES")
    else:
        print("DANG!")


#=====================================================
def BestFirstSearch(startingBoard):
    """Solve 8puzzle by Best-First Search"""

    FOUT = open("results.csv", 'w')
	
    import queue
    
    # Create a PriorityQueue instance
    # each item PUSHED (put) onto the Queue will be a tuple:  (heuristicScore, tieBreakerValue, theNode)
    Q = queue.PriorityQueue()	
    numberOfItemsAddedToQueue = 0

    startingBoard.Heuristic = startingBoard.getHeuristic_MisplacedTiles(BoardClass.GOAL)

    """To handle ties (two boards with the same priority score), we'll use a second
       argument for TIEBREAKERS, thus boards added later will be inserted AFTER in the Queue"""
    Q.put( (startingBoard.Heuristic, numberOfItemsAddedToQueue, startingBoard) )
    numberOfItemsAddedToQueue += 1

    Visited = [startingBoard]

    foundSolution = False
    nextTry = 0


    while (not Q.empty()):
        item = Q.get()
        print(f"\tPriority: {item[0]}, Value: {item[1]}")

        heuristicScore = item[0]
        tiebreakerValue = item[1]
        currentBoard = item[2]

        if (currentBoard.isGoal()):
            print("Found a solution!")
            foundSolution = True
            break

        # generate all possible moves from the current board
        nextMoves = currentBoard.createChildrenBoards()










    # if we get here (after the while loop), Q is empty and no solution found (??)
    print("No Solution ... ???")
    FOUT.close()

    return foundSolution
#=====================================================





#-----------\
# START HERE \
#-----------------------------------------------------------
if __name__ == '__main__':
    main()

#-----------------------------------------------------
