// README.txt

FILES:
BoardClass.py - Python file used to establish methods and functions of the class BoardClass
EightPuzzle_Main.py - Main python file used to run test boards for solving, includes functions
For both search algorithms 
test_BoardClass.py - pytesting file for BoardClass.py
Manhattan_AStar_Results.csv - csv file containing statistics for A* using Manhattan Distance with easy starting board
Misplaced_AStar_Results.csv - csv file containing statistics for A* using Misplaced Tiles with easy starting board
Manhattan_BestSearch_Results.csv - csv file containing statistics for Best-First Search Method using Manhattan Distance with easy starting board
Misplaced_BestSearch_Results.csv - csv file containing statistics for Best-First using Misplaced Distance with easy starting board

STATUS:
My program appears to be working. I did attempt all parts listed in the spec. Functions used for pytesting are stored in separate file (test_BoardClass.py). I did attempt to calculate average times for A*, but it was taking a very long time so I could not include averages. My current setup is when you run the program, it will run both A* and Best-First Search on Misplaced Tile Heuristic with a random board. To change the heuristic, you must change the call to foundSolution, maxQueueSize = AStarSearch(b, "Manhattan"), or foundSolution, maxQueueSize = BestFirstSearch(b, "Manhattan"). To test the starting boards, you must also comment out my code that is being used to randomize the board in BoardClass.py. This is on lines 118 and 122, and then uncomment the starting board code. 

kmd
10/19/26