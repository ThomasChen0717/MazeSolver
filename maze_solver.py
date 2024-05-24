from pylab import *
import matplotlib.colors as mcolors
ion()

def laplaceTransform(maze, start, end, omega=1.5, iterations = 1000,tol = 1e-5):
    potential = full(maze.shape, nan)
    potential[start] = 0
    potential[end] = 1
    
    n = len(maze)
    m = len(maze[0])

    for i in range(n):
        for j in range(m):
            if maze[i, j] == 0 and (i, j) not in [start, end]:
                potential[i, j] = (potential[start] + potential[end]) / 2

    
    for _ in range(iterations): #Iteration limit
        old_potential = potential.copy()
        for i in range(n):
            for j in range(m):
                if maze[i,j] == 0 and (i, j) not in [start, end]:
                    neighbors = [
                        potential[i-1, j] if i > 0 else nan,
                        potential[i+1, j] if i < n - 1 else nan,
                        potential[i, j-1] if j > 0 else nan,
                        potential[i, j+1] if j < m - 1 else nan
                    ]
                    valid_neighbors = [n for n in neighbors if not isnan(n)]
                    if valid_neighbors:
                        new_value = mean(valid_neighbors)
                        potential[i, j] = old_potential[i, j] + omega * (new_value - old_potential[i, j])

        if allclose(potential, old_potential, atol = tol):
            break

    return potential

def mazeSolver(potential_field, start, end):
    path = [start]
    current = start

    n = len(potential_field)
    m = len(potential_field[0])
    
    while current != end:
        i, j = current
        neighbors = [
            (i-1, j), (i+1, j),
            (i, j-1), (i, j+1)
        ]

        neighbors = [p for p in neighbors if 0 <= p[0] < n 
                    and 0 <= p[1] < m
                    and not isnan(potential_field[p])]

        current = max(neighbors, key = lambda p: potential_field[p])
        if current in path:
            print("Unsolvable Maze!")
            return None
        path.append(current)

    return path

def plot_maze(maze,path,start,end):
    START_COLOR = 2
    END_COLOR = 3

    maze[start] = START_COLOR
    maze[end] = END_COLOR
    
    cmap = mcolors.ListedColormap(['white', 'black', 'red', 'green'])
    
    imshow(maze, cmap=cmap)
    if not path:
        print("Unsolvable Maze!")
        return 
    path_y, path_x = zip(*path)
    scale = max(len(path_y), len(path_x))
    for i in range(1,len(path_y)+1):
           imshow(maze, cmap=cmap)
           plot(path_x[0:i], path_y[0:i], color='blue')
           pause(0.1*(1/scale))     


maze1 = array([
    [0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 1, 0, 1, 0, 1, 1, 0],
    [0, 0, 0, 1, 0, 1, 0, 1, 1, 0],
    [0, 1, 1, 1, 0, 1, 0, 0, 1, 0],
    [0, 0, 0, 0, 1, 1, 1, 1, 1, 0],
    [0, 1, 1, 1, 0, 1, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 1, 0, 1, 1, 0],
    [0, 1, 0, 1, 0, 1, 0, 1, 1, 0],
    [0, 0, 0, 1, 0, 1, 0, 0, 1, 0],
    [1, 1, 0, 1, 0, 0, 0, 1, 1, 0]
])

start1 = (0,0)
end1 = (9,9)

maze2 = array([
    [0, 1, 0],
    [0, 1, 0],
    [0, 1, 0]
])
start2 = (0, 0)
end2 = (2, 2)

maze3 = array([
    [0, 0, 0, 0, 0],
    [1, 0, 1, 0, 0],
    [0, 0, 1, 0, 0],
    [0, 1, 0, 0, 0],
    [0, 1, 1, 0, 0],
    [0, 0, 0, 0, 1]
])
start3 = (0, 2)
end3 = (5, 2)



maze4 = array([
    [1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1],
    [1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 1, 0],
    [1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0],
    [0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 1],
    [1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 0],
    [1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0],
    [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1],
    [1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1],
    [0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1],
    [1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 1],
    [0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1],
    [1, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 1, 1, 1],
    [1, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0],
    [1, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0],
    [0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0, 0, 1],
    [1, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1],
    [1, 0, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 0, 1],
    [0, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1],
    [1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
    [1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1],
    [1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1, 1, 1],
    [1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1, 0, 0],
    [1, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 1],
    [1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 0, 0, 0, 1],
    [1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 0, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1],
    [0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1],
    [1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
])

start4 = (0,1)
end4 = (29,28)

#After adding more mazes, update here
maze_list = [maze1, maze2, maze3, maze4]
start_end_list = [
   {'start': start1, 'end': end1},
    {'start': start2, 'end': end2},
    {'start': start3, 'end': end3},
    {'start': start4, 'end': end4}
]

#This is the maze number to run
index = 0
maze = maze_list[index]
start = start_end_list[index].get('start')
end = start_end_list[index].get('end')

potential_field = laplaceTransform(maze,start,end)
path = mazeSolver(potential_field, start, end)
plot_maze(maze,path,start, end)
