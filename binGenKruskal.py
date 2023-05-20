import ast
import math
import random
import time, os, sys

maze = []
visited = []
end = (0,0)
start = (0,0)
watch = False

# generates square maze with start and end using Kruskal's algorithm
def generate_maze(n):
    n = n+2 #need extra space for outer walls and junk row/col
    global maze, start, end
    # initialize maze
    maze = [[3 for j in range(n)] for i in range(n)] # 3 corresponds to '_|' in binary
    for i in range(0,n):
        maze[i][0] = 1 # 1 corresponds to '|' in binary
        maze[0][i] = 2 # 2 corresponds to '_' in binary
    maze[0][0] = 0 # 0 corresponds to ' ' in binary
    
    # Kruskal's algorithm to remove walls
    walls = []
    for i in range(1, n-1):
        for j in range(1, n-1):
            walls.append(((i, j), (i+1, j))) # vertical wall
            walls.append(((i, j), (i, j+1))) # horizontal wall
    random.shuffle(walls)
    sets = [{(i, j)} for i in range(1, n-1) for j in range(1, n-1)]
    for wall in walls:
        if watch: print_maze(maze)
        curr, next = wall
        set_curr = next_set = None
        for set in sets:
            if curr in set:
                set_curr = set
            if next in set:
                next_set = set
        if set_curr != next_set:
            connectCells(curr, next)
            if next_set is not None:
                set_curr |= next_set
                sets.remove(next_set)
    
    maze[n-1][n-1] = 0
    maze[n-1][0] = 0
    for i in range(1, n-1):
        maze[n-1][i] = 0
        maze[n-2][i] = maze[n-2][i]+2
        
    del maze[0][n-1]
    for i in range(1, n-1):
        del maze[i][n-1]
        maze[i][n-2] = maze[i][n-2]+1
    del maze[n-1]
    if watch: print_maze(maze)

# this function connects 2 cells by removing the wall between them
def connectCells(curr, next):
    global maze, end
    d = (next[0]-curr[0], next[1]-curr[1])
    if(d==(1,0)): #D
        if(maze[curr[0]][curr[1]] == 2): # corresponds to '_ '
            maze[curr[0]][curr[1]] = 0 # corresponds to '  '
        else: maze[curr[0]][curr[1]] = 1 # corresponds to ' |'
        
    if(d==(-1,0)): #U
        maze[next[0]][next[1]] = 1 # corresponds to '|'
        
    if(d==(0,1)): #R
        if(maze[curr[0]][curr[1]] == 1): # corresponds to ' |'
            maze[curr[0]][curr[1]] = 0 # corresponds to '  '
        else: maze[curr[0]][curr[1]] = 2 # corresponds to '_ '
        
    if(d==(0,-1)): #L
        maze[next[0]][next[1]] = 2 # corresponds to '_ '

def print_maze(maze):
    m = maze_to_str(maze)
    os.system('cls')
    print(m)
    
def maze_to_str(maze):
    m = ''
    for row in maze:
        for col in row:
            if(col==0): m += '  '
            elif(col==1): m += ' |'
            elif(col==2): m += '_ '
            elif(col==3): m += '_|'
        m += '\n'
    return m

def maze_to_binary(maze, start_pos, end_pos):
    binary_str = ""
    binary_str += '{:08b}'.format(start_pos[0])
    binary_str += '{:08b}'.format(start_pos[1])
    binary_str += '\n'
    binary_str += '{:08b}'.format(end_pos[0])
    binary_str += '{:08b}'.format(end_pos[1])
    binary_str += '\n'
    for row in maze:
        for col in row:
            if col == 3:
                binary_str += '11'
            elif col == 2:
                binary_str += '10'
            elif col == 1:
                binary_str += '01'
            else:
                binary_str += '00'
        binary_str += '\n'
    return binary_str.encode('utf-8')

def save_maze(f,maze):
    if not os.path.exists("./mazes"):
        os.makedirs("./mazes")
    with open('./mazes/'+f+'.bin', "wb") as f:
        f.write(maze_to_binary(maze, start, end))

def main():
    q = ''
    while not q == 'q':
        global maze, watch, start, end
        os.system('cls')
        size=0
        while(size > 100 or size < 5):
            size = int(input('Size (from 5 to 50): '))

        yn = input('Watch? (Y/N):  ')
        if(yn=='y' or yn=='Y'):
            watch=True

        lim = sys.getrecursionlimit()
        sys.setrecursionlimit(1000000)
        generate_maze(size)
        sys.setrecursionlimit(lim)

        if not watch:
            yn = input('Print? (Y/N):  ')
            if(yn=='y' or yn=='Y'):
                print_maze(maze)
        start = ast.literal_eval(input('Enter the start as Y,X: '))
        end = ast.literal_eval(input('Enter the end as Y,X: '))
        print("start: ", start)
        print("end: ", end)
        yn = input('Save? (Y/N):  ')
        if(yn=='y' or yn=='Y'):
            f = input('save-file name: ')
            save_maze(f,maze)
            size = os.path.getsize('./mazes/'+f+'.bin')
            print(f"Size of maze: {size} bytes")
        q = input("q to Quit maze generating with Kruskal: ")

if __name__ == "__main__":
    main()