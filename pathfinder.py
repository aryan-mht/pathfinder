import pygame
import math
from queue import PriorityQueue


WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Pathfinder Visualizer")

# colors 
RED = (255, 0, 0 )
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0 )
WHITE = (255, 255, 255)
BLACK = (0, 0 , 0)
PURPLE = (128, 0, 128)
ORANGE = (225, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)


class Spot:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width # row number 8 the width of each spot 
        self.y = col * width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

    
    def get_pos(self):
        return self.row, self.col

    # already looked at ? 
    def is_closed(self): 
        return self.color == RED
    
    def is_open(self):
        return self.color == GREEN
    
    def is_barrier(self):
        return self.color == BLACK
    
    def is_start(self):
        return self.color == ORANGE
    
    def is_end(self):
        return self.color == TURQUOISE
    
    def reset(self):
        self.color = WHITE

    def make_start(self):
        self.color = ORANGE

    def make_closed(self):
        self.color = RED
    
    def make_open(self):
        self.color = GREEN
    
    def make_barrier(self):
        self.color = BLACK

    def make_end(self):
        self.color = TURQUOISE
    
    def make_path(self):
        self.color = PURPLE
    
    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))
    
    def update_neighbors(self, grid):
        self.neighbors = []
        if self.row < self.total_rows -1 and not grid[self.row + 1][self.col].is_barrier(): # DOWN
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.row > 0  and not grid[self.row - 1][self.col].is_barrier(): # UP
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.col < self.total_rows -1 and not grid[self.row][self.col + 1].is_barrier(): # RIGHT
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): # LEFT
            self.neighbors.append(grid[self.row][self.col - 1])

    def __lt__(self,other):
        return False
    

# heuiristic function 
def h(p1, p2):
    x1, y1 = p1 # deconstruct p1
    x2, y2 = p2 # deconstruct p2
    return abs(x1-x2) + abs(y1-y2)

def reconstruct_path(came_from, current, draw):
    # current starts from the end node and we'll traverse to the start node 
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()


def a_star(draw, grid, start, end):
    draw() # Lamda is a anonym function so can call like this 
    count = 0
    open_set = PriorityQueue() # always gets the smallest element everytime out of it
    open_set.put((0, count, start))
    came_from = {}
    g_score = {spot: float("inf") for row in grid for spot in row} # for row in grid, for spot in row => g_score[spot] = float("inf")
    g_score[start] = 0

    f_score = {spot: float("inf") for row in grid for spot in row} # for row in grid, for spot in row => f_score[spot] = float("inf")
    f_score[start] = h(start.get_pos(), end.get_pos()) # 0 + h

    open_set_hash = {start}

    while not open_set.empty():
        # make sure we're not quitting the game, if we are then quit 
        for event in pygame.event.get():
             if event.type == pygame.QUIT: 
                 pygame.quit()
        
        
        current = open_set.get()[2] # gets the min fscore related node from the priority queue 
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            return True
        
        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash: 
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()
        draw()
        if current != start: 
            current.make_closed()
    return False



def dfs(draw, grid, start, end, ROWS):
    draw() # Lamda is a anonym function so can call like this 
    stack = [(start, None)] # node of node and its parent 
    visited = set() # to  avoid duplicacy 
    parents = {} # dict to store parent information
    
    
    # while set is not empty 
    while stack:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        current, parent = stack.pop()
        visited.add(current)


        # check if we reached the goal 
        if current == end:
            reconstruct_path_dfs_bfs(start, end, parents, draw)  # Pass the required arguments directly
            end.make_end()
            return True
        
        for neighbor in current.neighbors:
            if neighbor not in visited and not neighbor.is_barrier():
                stack.append((neighbor, current))
                neighbor.make_open()
                parents[neighbor] = current
                draw()
        if current != start:
            current.make_closed()
    return False


def reconstruct_path_dfs_bfs(start, end, parents, draw,):  # Pass the required arguments directly
    current = end
    while current != start:
        current.make_path()
        draw()
        current = parents[current]



def bfs(draw, grid, start, end, ROWS):
    draw()
    queue = [start]
    visited = set()
    parents = {}

    while queue: 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        current = queue.pop(0)

        if current == end:
            reconstruct_path_dfs_bfs(start, end, parents, draw)
            end.make_end()
            return True        
        
        for neighbor in current.neighbors:
            if neighbor not in visited and not neighbor.is_barrier():
                queue.append(neighbor)
                visited.add(neighbor)
                neighbor.make_open()
                parents[neighbor] = current
                draw()
        if current != start:
            current.make_closed()

    return False

def make_grid(rows, width):
    grid = []
    gap = width // rows # the width of each cube 
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Spot(i, j, gap, rows) # i and j are current row, col for that spot and gap is the width of each Spot
            grid[i].append(spot)
    return grid

def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i*gap), (width, i * gap)) # horizontal lines 
    
    for j in range(rows):
        pygame.draw.line(win, GREY, (j*gap, 0), (j * gap, width)) # vertical lines 

def draw(win, grid, rows, width):
    win.fill(WHITE)
    for row in grid:
        for spot in row:
            spot.draw(win)
    draw_grid(win, rows, width)
    pygame.display.update()

def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y,x = pos
    row = y // gap
    col = x // gap
    return row,col

def main(win, width):
    ROWS = 50

    grid = make_grid(ROWS, width)
    start = None
    end = None
    algorithm = None
    run = True
    while run:
        draw(win, grid, ROWS, width)
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:
                run = False
           

            if pygame.mouse.get_pressed()[0]: # left click 
                pos = pygame.mouse.get_pos() # x, y coord of the click 
                row, col = get_clicked_pos(pos, ROWS, width)
                spot = grid[row][col]
                if not start and spot!=end:
                    start = spot
                    start.make_start() 
                elif not end and spot!=start:
                    end = spot
                    end.make_end()
                
                elif spot != end and spot != start: 
                    spot.make_barrier()
            elif pygame.mouse.get_pressed()[2]: # right click 
                pos = pygame.mouse.get_pos() # x, y coord of the click 
                row, col = get_clicked_pos(pos, ROWS, width)
                spot = grid[row][col]            
                spot.reset()    
                if spot == start:
                    start = None
                elif spot == end: 
                    end = None
            
            if event.type == pygame.KEYDOWN:
                for row in grid:
                    for spot in row:
                        spot.update_neighbors(grid)                
                if event.key == pygame.K_d and start and end:
                    # Execute DFS when the "D" key is pressed
                    dfs(lambda: draw(win, grid, ROWS, width), grid, start, end, ROWS)

                if event.key == pygame.K_a and start and end:
                    # Execute A* when the "A" key is pressed
                    a_star(lambda: draw(win, grid, ROWS, width), grid, start, end)
                
                if event.key == pygame.K_b and start and end:
                    bfs(lambda: draw(win, grid, ROWS, width), grid, start, end, ROWS)

                    
                if event.key == pygame.K_ESCAPE:
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)    

    pygame.quit()

main(WIN, WIDTH)