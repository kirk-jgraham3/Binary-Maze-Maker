# Binary-Maze-Maker
Command line Python program that generates playable Mazes stored in efficient binary files. The project currently implements either Kruskal's or DFS (user's choice) for the maze generation. There is an AI that finds the most efficient path through the maze by implementing an A* Search.

The files are described more in depth in sections below.


# Using the Programs
Follow any prompts for the required input. 

Inputs are very basic, for example:  
`Y` or `N` to make a choice, numerical values for dimensions and picking from lists, and `q` to Quit at a specific point in the program. 

Use `Ctrl+C` to immediately end any process at any time.


# The Maze Generators - binGenDFS.py, binGenKruskal.py
These programs use the respective algorithm to generate a square maze of user-specified dimensions.  
Walls are either `_` or `|`.  
The start and end do not currently have visual markers, but the coordinates are stored in the binary files.  
Dimensions can range from 5 to 50, but <25 is recommended if the user wants to watch it generate without much flickering.  
Users have the option to watch the algorithm work ("dig" paths through a grid). Then, the option to save the resulting maze to a `.bin` file (simply type the name excluding extension when prompted).

**The only other difference between using the two:**  
Kruskal will prompt the user for start and end coordinates.  
Meanwhile, DFS currently chooses both randomly.

Run: `python binGenKruskal.py` or `python binGenKruskal.py`


# Play - binPlay.py
Select a locally stored maze from a list. 
Navigate the maze by using WASD or Arrow Keys to move the player (`o`).  
Start and End coordinates will be displayed under the maze. 
Once you reach the end the game will end with the message "You Win!"

Run: `python binPlay.py`


# A* - binAStar.py
Select a locally stored maze from a list. 
The AI will immediately attempt to find the most efficient solution to the maze. 
It will print the actions and score it finds, then ask if you would like to watch the solution play out.

Run: `python binAStar.py`


# All - mainBin.py
This just runs all programs: generate, then A*, then play.

Run: `python mainBin.py`


# Understanding the Binary File and Maze
Here is an example file I generated with the DFS algorithm:  
```
00000010 00000101  
00000100 00000101  
001010101010  
011000101011  
010011001011  
010001010001  
010110110101  
011010101111  
```

**The first line:** This line contains 2 bytes corresponding respectively to the Y and X coordinates of the Start.  
* in this case, the Start is at Y=2, X=5  

**The second line:** Similar to the first, these 2 bytes hold the Y and X coordinates of the End. 
* in this case, the End is at Y=4, X=5  

After these first 2 lines, the binary can be broken up into sets of 2 bits. Each row is a row in the maze and every 2 bits indicates the walls in its corresponding cell within the maze.  
`00 -> 0 -> '  '`  
`01 -> 1 -> ' |'`  
`10 -> 2 -> '_ '`  
`01 -> 3 -> '_|'`

Initially a maze starts out as a full grid contained in a 2D array, so each cell in this array is initialized to 3 (`'_|'`) then changed as walls are deconstructed to connect cells and form paths.

The binary from this example file is read and interpreted by the programs as:  
```
00 10 10 10 10 10 --> 0 2 2 2 2 2 --> '  _ _ _ _ _ '  
01 10 00 10 10 11 --> 1 2 0 2 2 3 --> ' |_   _ _ _|'  
01 00 11 00 10 11 --> 1 0 3 0 2 3 --> ' |  _|  _ _|'  
01 00 01 01 00 01 --> 1 0 1 1 0 1 --> ' |   | |   |'  
01 01 10 11 01 01 --> 1 1 2 3 1 1 --> ' | |_ _| | |'  
01 10 10 10 11 11 --> 1 2 2 2 3 3 --> ' |_ _ _ _|_|'  
```

Finally, the maze is printed such that Y=0, X=0 is the top left corner. Y increases moving down, X increases moving right. Therefore, the Start and End of this file are as indicated below.
```
 0 1 2 3 4 5
0  _ _ _ _ _   
1 |_   _ _ _|  
2 |  _|  _ s̲|  
3 |   | |   |  
4 | |_ _| |e|  
5 |_ _ _ _|_|  
```
***Notice:*** Even though the first cell of the array is (0,0) the first **internal cell** of the maze is (1,1). (0,0) actually lies outside the playable area of the maze. In fact, this goes for all cells where Y=0 or X=0 since they construct the top and left borders for the maze.

That should about cover anything of importance regarding the maze and binary construction/format.

# Future Plans
There are a couple features that could be implemented differently (or better). 
However, this program is really designed for my own use and experimenting. Therefore, refactoring for improved efficiency is not a primary focus or concern.  

If I happen across anything I find particularly annoying with the code, I will make impromptu changes.  

At some point, I may want to try out different generation algorithms (such as BFS or Prim's) since the patterns are very interesting.  

One very obvious feature to add will be saving the solution found by the AI to a binary file.  

All in, I am mostly satisfied with the current state and functionality of the code. I do not have any **_major_** changes planned.

**_In the Further Future:_**
I do have plans for this to be utilized as a system for creating levels in a future Android app. 
Hence the binary. I wanted files with a small footprint just in case I ever need to put them in a database.
