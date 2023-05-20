import heapq
import os, time, copy
import keyboard
from binGenDFS import print_maze, maze_to_str, maze_to_arr

maze = [[]]
visited = [[]]
end = (0,0)
start = (0,0)
watch = False

# arrays are mutable, but not hashable
def array_to_tuple(arr):
    return tuple(tuple(row) for row in arr)

# tuples are hashable, but immutable
def tuple_to_array(tup):
    return [list(row) for row in tup]

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

def move_marker(curr,prev,state):
    new_state = copy.deepcopy(state)
    #move marker and underline if bottom wall
    space=new_state[curr[0]][curr[1]]
    if not can_go_down(curr[0], curr[1]):
        new_state[curr[0]][curr[1]] = space.replace("_","o\u0332")
    else:
        new_state[curr[0]][curr[1]] = space.replace(" ","o", 1)
    #clear prev space
    new_state[prev[0]][prev[1]] = new_state[prev[0]][prev[1]].replace("o\u0332","_").replace("o"," ")
    #print("new child")
    #print_str(new_state)
    return new_state

def heuristic(state):
    # heuristic returns optimistic guess of steps from goal
    # 0 for now, add something smarter later on
    return 0

def is_goal_state(state):
    # goal state if the end has been marked
    if state[end[0]][end[1]] in ["o\u0332 ", "o ", "o\u0332|", "o|"]:
        return True
    return False

def get_successors(state):
    # successors are next possible moves
    #print("new parent")
    successors = []
    
    # find the marker's position in parent node
    prev = (0,0)
    for i,row in enumerate(state):
        for j,val in enumerate(row):
            if val in ["o\u0332 ", "o ", "o\u0332|", "o|"]:
                prev = (i,j)
    
    #print("parent start: ",prev[0],prev[1])
    #print_str(state)
    
    # check every direction and construct nodes (state, action, cost)
    if can_go_up(prev[0],prev[1]):
        #print("can up")
        curr = (prev[0]-1, prev[1])
        s_node = (move_marker(curr,prev,state), "up", 1)
        successors.append(s_node)
        
    if can_go_down(prev[0],prev[1]):
        #print("can down")
        curr = (prev[0]+1, prev[1])
        s_node = (move_marker(curr,prev,state), "down", 1)
        successors.append(s_node)
        
    if can_go_left(prev[0],prev[1]):
        #print("can left")
        curr = (prev[0], prev[1]-1)
        s_node = (move_marker(curr,prev,state), "left", 1)
        successors.append(s_node)
        
    if can_go_right(prev[0],prev[1]):
        #print("can right")
        curr = (prev[0], prev[1]+1)
        s_node = (move_marker(curr,prev,state), "right", 1)
        successors.append(s_node)
    
    return successors   # list of child nodes
    
def a_star():
    global maze, start, end
    
    start_state = maze_to_arr(maze)   # start state for search alg
    visited = dict()    # key: state (as a tuple), data: cost
    
    #initialize start position in start_state
    curr = (start[0], start[1])
    start_state = move_marker(curr, (0,0), start_state)
    
    actions=[]  # log actions taken
    start_node = (start_state, actions, 0)  # (state, actions, cost)
    queue = []  # queue for deciding which state to investigate next
    ids = 0
    heapq.heapify(queue)
    # sort queue by heuristic value, then id (order of discovery)
    heapq.heappush(queue, (heuristic(start_state), ids, start_node))
    
    visited[array_to_tuple(start_state)] = 0    # add start_state to visited dict, cost of 0
    i=0
    while len(queue)>0:
        f, i, node = heapq.heappop(queue)   # use node from top of queue
        state, act_curr, cost_curr = node
        
        if is_goal_state(state):
            return act_curr
        
        for child in get_successors(state):
            
            c_state, c_act, c_cost = child
            
            c_state_tuple = array_to_tuple(c_state)
            if c_state_tuple not in visited or c_cost < visited[c_state_tuple]:
                visited[c_state_tuple] = c_cost
            
                act_next = act_curr+[c_act]
                c_next = cost_curr+c_cost
            
                f_next = heuristic(c_state) + c_next
                #print(f_next, end=" ")
                ids+=1
                next_node = (c_state, act_next, c_next)
                heapq.heappush(queue, (f_next, ids, next_node))
    return []

def cpu_play(maze, actions):
    state = maze_to_arr(maze)
    curr = (start[0], start[1])
    new_state = move_marker(curr,(0,0),state)
    print_str(new_state)
    time.sleep(0.1)
    for act in actions:
        prev = curr
        if act == 'up':
            curr = (prev[0]-1, prev[1])
        elif act == 'down':
            curr = (prev[0]+1, prev[1])
        elif act == 'left':
            curr = (prev[0], prev[1]-1)
        elif act == 'right':
            curr = (prev[0], prev[1]+1)
        new_state = move_marker(curr,prev,new_state)
        print_str(new_state)
        print(act)
        print('Current Pos: Y='+str(curr[0])+', X='+str(curr[1]))
        print('Start: Y='+str(start[0])+', X='+str(start[1]))
        print('End: Y='+str(end[0])+', X='+str(end[1]))
        time.sleep(0.1)
    print("Done!")
    time.sleep(2)

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
    actions = a_star()
    print('Start: '+str(start[0])+','+str(start[1]))
    print('End: '+str(end[0])+','+str(end[1]))
    print('\nActions found:\n',actions)
    print('\nBest Possible Score: ', len(actions))
    
    watch = input("\nWatch the solution? (y/n) ")
    if watch == 'y' or watch == 'Y':
        cpu_play(maze, actions)

if __name__ == "__main__":
    main()