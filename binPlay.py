import os, time
import keyboard
from binGenDFS import print_maze, maze_to_str

maze = [[]]
visited = [[]]
end = (0,0)
start = (0,0)
watch = False
score = 0

def can_go_up(y,x):
    # check space above for bottom wall
    if(maze[y-1][x]==2 or maze[y-1][x]==3):
        return False
    return True

def can_go_down(y,x):
    # check current space for side wall
    if(maze[y][x]==2 or maze[y][x]==3):
        return False
    return True

def can_go_left(y,x):
    # check left space for side wall or start (dont want to leave maze)
    if(maze[y][x-1]==1 or maze[y][x-1]==3):
        return False
    return True

def can_go_right(y,x):
    # check current space for bottom wall
    if(maze[y][x]==1 or maze[y][x]==3):
        return False
    return True

def getkey():
    key = None
    while key is None:
        event = keyboard.read_event()
        if event.event_type == 'down':
            key = event.name
    return key

def print_str(maze_str):
    os.system('cls')
    for row in maze_str:
        for col in row:
            print(col, end='')
        print()

def move_marker(curr,prev):
    global score
    score = score + 1
    m=maze_to_str(maze).split('\n')
    maze_str = []
    for row in m:
        maze_str.append([row[i:i+2] for i in range(0, len(row)-1, 2)])
    #move marker and underline if bottom wall
    space=maze_str[curr[0]][curr[1]]
    if not can_go_down(curr[0], curr[1]):
        maze_str[curr[0]][curr[1]] = space.replace("_","o\u0332")
    else:
        maze_str[curr[0]][curr[1]] = space.replace(" ","o", 1)
    #clear prev space
    maze_str[prev[0]][prev[1]] = maze_str[prev[0]][prev[1]].replace("o\u0332","_").replace("o"," ")
    print_str(maze_str)
    
def play():
    global maze, start, end, score
    score = -1
    #initialize position to start
    curr = (start[0], start[1])
    move_marker(curr, (0,0))
    
    print("Use WASD or Arrow Keys to move")
    print('Start: Y='+str(start[0])+', X='+str(start[1]))
    print('End: Y='+str(end[0])+', X='+str(end[1]))
    
    while not curr == end:
        prev = curr
        dir = getkey()
        
        if dir=='w' or dir=="up":
            if not can_go_up(curr[0],curr[1]): continue
            dir = 'up'
            curr = (curr[0]-1, curr[1])
        
        elif dir=='a' or dir=="left":
            if not can_go_left(curr[0],curr[1]): continue
            dir = 'left'
            curr = (curr[0], curr[1]-1)
        
        elif dir=='s' or dir=="down":
            if not can_go_down(curr[0],curr[1]): continue
            dir = 'down'
            curr = (curr[0]+1, curr[1])
        
        elif dir=='d' or dir=="right":
            if not can_go_right(curr[0],curr[1]): continue
            dir = 'right'
            curr = (curr[0], curr[1]+1)
            
        else:
            dir = 'invalid'
            continue
        
        move_marker(curr,prev)
        print("Use WASD or Arrow Keys to move")
        print('Current Pos: Y='+str(curr[0])+', X='+str(curr[1]))
        print('Start: Y='+str(start[0])+', X='+str(start[1]))
        print('End: Y='+str(end[0])+', X='+str(end[1]))
        
    print("\nYou Win!")
    print("Score: ", score)

def main():
    os.system('cls')
    global maze, watch, start, end
    file_list = []

    print("List of mazes:")
    for file in os.listdir('./mazes'):
        if file.endswith('.bin'):
            file_list.append(file)
            print("\t"+str(len(file_list))+":", file)

    maze_num = 0
    while(maze_num > len(file_list) or maze_num < 1):
        maze_num = int(input("Enter number of the maze you want to play: "))
    
    maze = []

    with open('./mazes/'+file_list[maze_num-1], "rb") as f:
        start = (int(f.read(8), 2), int(f.read(8), 2))
        f.read(1)
        end = (int(f.read(8), 2), int(f.read(8), 2))
        f.read(1)
        for line in f.readlines():
            maze.append([int(line[i:i+2], 2) for i in range(0, len(line)-1, 2)])
    print_maze(maze)
    play()

if __name__ == "__main__":
    main()