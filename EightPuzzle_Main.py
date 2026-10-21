
"""
Solve the 8-puzzle using various search algorithms, including
two Best-First algorithms: (1) MisplacedTiles and (2) ManhattenDistance
as heuristics.

# originally implemented in Python v2.x by Kelsey Hichens '13
# converted to v3.x (mdl, 08/01/2012)
      % 2to3 -w code.py

# this code is mostly unfinished (mdl, 09/18/2026)
# Started implementing and finishing necessary methods in BoardClass.py (kmd, 10/10/2026)
# Added to BestFirstSearch method in EightPuzzle_Main.py (kmd, 10/11/2026)
# Added to AStarSearch method in EightPuzzle_Main.py (kmd, 10/15/2026)
# Combined Manhattan and Misplaced heuristics to be ran in one file (kmd, 10/16/2026)
# Started implementing AStarSearch algorithim in EightPuzzle_Main.py (kmd, 10/17/2026)
# Worked on creating helper trial functions for BestFirstSearch and AStarSearch (kmd, 10/18/2026)
# Created a new file for unit testing the BoardClass.py methods (kmd, 10/18/2026)
# Worked on necessary documentation for EightPuzzle_Main.py functions (kmd, 10/18/2026)

Purpose: To solve the 8-Puzzle board based on two algorithims (A* and Best-First) using two 
Heuristics (Manhattan or Misplaced Tiles). 

INPUT: There is no user input in this program.

OUTPUT: See attatched report "K.delapena_Program2_Report"


"""
   
import csv
import time

from BoardClass import *

#=====================================================
def main():

    b = BoardClass()
    b.initializePuzzleBoard("Misplaced")

    foundSolution, maxQueueSize = BestFirstSearch(b, "Manhattan")
    if (foundSolution):
        print("YES")
    else:
        print("DANG!")

    foundSolution, maxQueueSize = AStarSearch(b, "Manhattan")
    if (foundSolution):
        print("YES")
    else:
        print("DANG!")

    #BestFirstSearch_Trials()
    #AStarSearch_Trials()

#=====================================================
def printSearchStats(currentBoard : BoardClass, algorithimName : str, heursticType : str) -> None:
#=====================================================
    """ Helper function to print the search stats after a solution is found. """

    # Establish an empty path list and set the current board to the starting board
    path = []
    board = currentBoard

    # Do not include parent boards in the path, only include the children boards that lead to the solution
    while board is not None:
        path.append(board)
        board = board.Parent

    # Reverse the path to show the moves from the starting board to the solution
    path.reverse()
    numberOfMoves = len(path) - 1

    # Print the search stats to the console
    print("SEARCH ALGORITHM: ", algorithimName)
    print("HEURISTIC: ", heursticType)
    print("DONE!! Number of moves to solve puzzle: ", numberOfMoves)

    # Print starting board to console 
    print("\nStarting Board")
    print(path[0])

    # Print each move and the board state after the move to the console
    for board in range(1, len(path)):
        print("Move # ", board)
        print(path[board])

    # end printSearchStats()
#=====================================================
def calculateHeuristic(board : BoardClass, heuristicType : str) -> int:
    """Calculate the heuristic value for a given board based on the specified heuristic type."""

    # Check the heuristic type and call the appropriate method from the BoardClass to calculate the heuristic value
    if heuristicType == "Misplaced":
        return board.getHeuristic_MisplacedTiles(BoardClass.GOAL)
    elif heuristicType == "Manhattan":
        return board.computeDistanceFromGoal()
    else:
        return 0 # Default case if heuristic type is not recognized

    # end calculateHeuristic()
#=====================================================
def BestFirstSearch(startingBoard : BoardClass, heuristicType : str) -> tuple[bool, int]:
    """Solve 8puzzle by Best-First Search"""


    # Open .csv file to write the results of the search, commented out in trials
    FOUT = open(heuristicType + "_BestSearch_Results.csv", 'w')
    writer = csv.writer(FOUT)
    writer.writerow(["Board Number Tried", "Size of Queue", "Size of Visited List", "Time (Seconds) so far"])

	
    import queue
    
    # Create a PriorityQueue instance
    # each item PUSHED (put) onto the Queue will be a tuple:  (heuristicScore, tieBreakerValue, theNode)
    Q = queue.PriorityQueue()	
    numberOfItemsAddedToQueue = 0

    startingBoard.Heuristic = calculateHeuristic(startingBoard, heuristicType)

    """To handle ties (two boards with the same priority score), we'll use a second
       argument for TIEBREAKERS, thus boards added later will be inserted AFTER in the Queue"""
    Q.put( (startingBoard.Heuristic, numberOfItemsAddedToQueue, startingBoard) )
    numberOfItemsAddedToQueue += 1

    Visited = [startingBoard]

    foundSolution = False
    nextTry = 0
    numberofMoves = 0
    maxQueueSize = 0

    # Start the timer to measure the time taken for the search
    startTime = time.time()

    # While the queue is not empty, continue searching for the solution
    while (not Q.empty()):
        item = Q.get()
        # Record max queue size for trials
        if (Q.qsize() > maxQueueSize):
            maxQueueSize = Q.qsize()

        heuristicScore = item[0]
        tiebreakerValue = item[1]
        currentBoard = item[2]

        writer.writerow([nextTry, Q.qsize(), len(Visited), time.time() - startTime])

        # Check if the current board is the goal state by calculating its heuristic value
        if (calculateHeuristic(currentBoard, heuristicType) == 0):
            # End Time if goal is found 
            endTime = time.time()
            printSearchStats(currentBoard, "Best-First Search", heuristicType)
            print("Time taken: ", f"{endTime - startTime:.5f}", "seconds")
            foundSolution = True
            # Break loop
            break

        # generate all possible moves from the current board
        nextMoves = currentBoard.createChildrenBoards(heuristicType)

        # For each possible move, calculate its heuristic value and check if it has already been visited.
        #  If not, add it to the priority queue and mark it as visited.
        for move in nextMoves:

            if move is None:
                continue

            # determine the heuristic value for child board
            move.Heuristic = calculateHeuristic(move, heuristicType)

            # check if this board has already been visited
            alreadyVisited = False
            for v in Visited:
                if (move.sameBoard(v)):
                    alreadyVisited = True
                    break

            # if board has not been visited, add to queue
            if (not alreadyVisited):
                Q.put( (move.Heuristic, numberOfItemsAddedToQueue, move) )
                numberOfItemsAddedToQueue += 1
                Visited.append(move)
        
        # record number of attempts to find solution for trials
        nextTry += 1

        
    # if we get here (after the while loop), Q is empty and no solution found (??)
    FOUT.close()

    return foundSolution, maxQueueSize

    # end BestFirstSearch()
#=====================================================
def BestFirstSearch_Trials() -> None:
    """Run a series of trials of Best-First Search, and record the results in a CSV file"""

    # Open .csv file to write the results of the search
    FOUT = open("BestSearch_Trials.csv", 'w')
    writer = csv.writer(FOUT)
    writer.writerow(["Heuristic", "Average Search Time (Seconds)", "Average Max Queue Size"])

    # Test both heuristics 
    for heuristic in ["Misplaced", "Manhattan"]:
        # Initialize variables to track average time and max queue size
        avg_Time = 0.0
        avg_MaxQueueSize = 0
        
        # Run 1000 trials for each heuristic
        for trial in range(1, 1001):
            b = BoardClass()
            b.initializePuzzleBoard(heuristic)

            # Start the timer for the trial
            trialStartTime = time.time()

            # Identify MaxQueueSize for the trial by running BestFirstSearch
            _, maxQueueSize = BestFirstSearch(b, heuristic)

            # Add all times to avg_Time
            avg_Time += (time.time() - trialStartTime)
            # Add all maxQueueSizes to avg_MaxQueueSize
            avg_MaxQueueSize += maxQueueSize

        # Calculate the average time and max queue size for the trials
        average_Time = avg_Time / 1000.0
        average_MaxQueueSize = avg_MaxQueueSize / 1000.0

        # Store results in the .csv file for each heuristic
        writer.writerow([heuristic, f"{average_Time:.5f}", f"{average_MaxQueueSize:.5f}"])

    

    print("Trials complete. Results written to BestSearch_Trials.csv")

    FOUT.close()

    # end BestFirstSearch_Trials()
#=====================================================
def AStarSearch(startingBoard : BoardClass, heuristicType : str) -> tuple[bool, int]:
    """Solve 8puzzle by A* Search"""

    # Open a .csv file to store data in
    FOUT = open(heuristicType + "_AStar_Results.csv", 'w')
    writer = csv.writer(FOUT)
    writer.writerow(["Board Number Tried", "Size of Queue", "Size of Visited List", "Time (Seconds) so far"])

    import queue
    
    # Create a PriorityQueue instance
    # each item PUSHED (put) onto the Queue will be a tuple:  (heuristicScore, tieBreakerValue, theNode)
    Q = queue.PriorityQueue()	
    numberOfItemsAddedToQueue = 0

    # Set starting heurisitc and score
    startingBoard.Heuristic = calculateHeuristic(startingBoard, heuristicType)
    startingBoard.Score = startingBoard.Heuristic
    
    """To handle ties (two boards with the same priority score), we'll use a second
       argument for TIEBREAKERS, thus boards added later will be inserted AFTER in the Queue"""
    Q.put( (startingBoard.Score, numberOfItemsAddedToQueue, startingBoard) )
    numberOfItemsAddedToQueue += 1
    
    Visited = [startingBoard]

    foundSolution = False
    nextTry = 0
    maxQueueSize = 0
    
    # Start the time for trials
    startTime = time.time()

    # Store max queue sizes for trials 
    while (not Q.empty()):
        item = Q.get()
        if (Q.qsize() > maxQueueSize):
            maxQueueSize = Q.qsize()
    
        heuristicScore = item[0]
        tiebreakerValue = item[1]
        currentBoard = item[2]

        # Store stats for each move in .csv file 
        writer.writerow([nextTry, Q.qsize(), len(Visited), time.time() - startTime])
    
        # Check if currentBoard is the goal state
        if (currentBoard.calculateHeuristic(heuristicType) == 0):
            # End time once solution is found
            endTime = time.time()
            printSearchStats(currentBoard, "A* Search", heuristicType)
            print("Time taken: ", f"{endTime - startTime:.5f}", "seconds")
            foundSolution = True
            break
    
        # generate all possible moves from the current board
        nextMoves = currentBoard.createChildrenBoards(heuristicType)

        # Check children boards
        for move in nextMoves:

            if move is None:
                continue

            # Calculate heuristic and score 
            move.Heuristic = move.calculateHeuristic(heuristicType)
            move.Score = currentBoard.Score - currentBoard.Heuristic + 1 + move.Heuristic  # g(n) + h(n)
    
            # check if this board has already been visited
            alreadyVisited = False
            for v in Visited:
                if (move.sameBoard(v)):
                    alreadyVisited = True
                    break

            # If not, put on queue
            if (not alreadyVisited):
                Q.put((move.Score, numberOfItemsAddedToQueue, move))
                numberOfItemsAddedToQueue += 1
                Visited.append(move)
            
    
        nextTry += 1

    FOUT.close()

        
    return foundSolution, maxQueueSize

# end AStarSearch()

#=====================================================
def AStarSearch_Trials() -> None:
    """Run a series of trials of A* Search, and record the results in a CSV file"""

    # Open csv file to store results
    FOUT = open("AStarSearch_Trials.csv", 'w')
    writer = csv.writer(FOUT)
    writer.writerow(["Heuristic", "Average Search Time (Seconds)", "Average Max Queue Size"])

    # Check both heuristic types
    for heuristic in ["Misplaced", "Manhattan"]:
        avg_Time = 0.0
        avg_MaxQueueSize = 0
        
        # Start 1000 trials
        for trial in range(1, 1001):
            b = BoardClass()
            b.initializePuzzleBoard(heuristic)

            # time each trial
            trialStartTime = time.time()

            # calculate maxQueueSize
            _, maxQueueSize = AStarSearch(b, heuristic)

            # store  time/queue size for each trial
            avg_Time += (time.time() - trialStartTime)
            avg_MaxQueueSize += maxQueueSize

        # Divide by 1000 to compute average
        average_Time = avg_Time / 1000.0
        average_MaxQueueSize = avg_MaxQueueSize / 1000.0

        # store in .csv file
        writer.writerow([heuristic, f"{average_Time:.5f}", f"{average_MaxQueueSize:.5f}"])

    

    print("Trials complete. Results written to AStarSearch_Trials.csv")

    FOUT.close()

# end AStarSearch_Trials()


#-----------\
# START HERE \
#-----------------------------------------------------------
if __name__ == '__main__':
    main()

#-----------------------------------------------------
