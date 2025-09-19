import math, pygame, random
from collections import defaultdict
from pygame.locals import *
from collections import deque

def init():
  global clock, display
  display = Display(10, 10)
  pygame.init()
  clock = pygame.time.Clock()
  pygame.display.set_caption("DEMO PROGRAM 1")
  keys=pygame.key.get_pressed()

class Display:
    def __init__(self, board_height = 8, board_width = 8):
        self.board_height = board_height
        self.board_width = board_width
        self.width = 200
        self.height = 200
        self.screen = pygame.display.set_mode((self.width*2, self.height*2))

class Model:
    def __init__(self, board_height, board_width):
        self.dt = 0
        # (x, y):wall
        # 0 is up, everything else goes clockwise in order
        self.walls = defaultdict(set)
        self.selected = None
        self.board_height= board_height
        self.board_width = board_width
        self.queue = deque()
        #list of (x, y)
        self.visited = set()
        self.start = None
        self.running = True

def main():
  init()
  model = Model(display.board_height, display.board_width)
  randomize(model)
  inputs={'mouse_down':False, 'last_mouse_down':False, 'mouse_x':0, 'mouse_y':0, 'W':False, 'A':False, 'S':False, 'D':False, 'SPACE':False,
  'UP':False,'DOWN':False, 'RIGHT':False, 'LEFT':False}
  g = None
  step = 0
  while model.running:
    if pygame_running()==False:
      model.running = False
      break
    model.dt = clock.tick(30)
    inputs = update_inputs(inputs)
    model = input_handler(inputs, model, g)
    if model.start is not None and g is None:
        g = Graph()
        model.queue.append(model.start)
    if g is not None and step%3 == 0:
        (g, model) = update_bfs(g, model)
    model = draw_handler(model)
    update_screen()
    step += 1
def randomize(model):
    chance = 0.5
    # columns:
    for row in range(model.board_height):
        for wall in range(model.board_width-1):
            if random.random() > chance:
                continue
            model.walls[(wall, row)].add(1)
            model.walls[(wall+1, row)].add(3)
    # rows:
    for column in range(model.board_width):
        for wall in range(model.board_height-1):
            if random.random() > chance:
                continue
            model.walls[(column, wall)].add(2)
            model.walls[(column, wall+1)].add(0)
            
def update_bfs(g, model):
    if not model.queue:
        return (g, model)
    current = model.queue.popleft()
    if current in model.visited:
        return (g, model)
    neighbors = check_edges(model, current)
    g.add_v(current, neighbors)
    for v in neighbors:
        if v in model.visited:
            continue
        model.queue.append(v)
    model.visited.add(current)
    return (g, model)

def check_edges(model, v1):
    walls = model.walls[v1]
    (x, y) = v1
    neighbors = []
    if 0 not in walls:
        if y > 0:
            neighbors.append((x, y-1))
    if 1 not in walls:
        if x < model.board_width-1:
            neighbors.append((x+1, y))
    if 2 not in walls:
        if y < model.board_height-1:
            neighbors.append((x, y+1))
    if 3 not in walls:
        if x > 0:
            neighbors.append((x-1, y))
    return neighbors
    
def draw_handler(model):
  screen = display.screen
  bgcolor = pygame.color.Color("orange")
  screen.fill(bgcolor)
  draw_walls(model)
  return model
  
def draw_walls(model):
    board_width = int(display.width*2/display.board_width)
    board_height = int(display.width*2/display.board_height)
    screen = display.screen
    black = pygame.color.Color("black")
    blue = pygame.color.Color("aqua")
    
    for (index, square) in model.walls.items():
        (i, j) = index
        (y, x) = (board_width*(j+1/2)+1/2, board_height * (i+1/2)+1/2)
        if 0 in square:
            pygame.draw.line(screen, black, (x-board_width/2, y-board_height/2), (x+board_width/2, y-board_height/2), 3)
        if 1 in square:
            pygame.draw.line(screen, black, (x+board_width/2, y-board_height/2), (x+board_width/2, y+board_height/2), 3)
        if 2 in square:
            pygame.draw.line(screen, black, (x+board_width/2, y+board_height/2), (x-board_width/2, y+board_height/2), 3)
        if 3 in square:
            pygame.draw.line(screen, black, (x-board_width/2, y+board_height/2), (x-board_width/2, y-board_height/2), 3)
    
    #red = pygame.color.Color("red")
    for square in model.visited:
        (i, j) = square
        (y, x) = (board_width*(j+1/2), board_height * (i+1/2))
        s = pygame.Rect(0, 0, board_width-3, board_height-3)
        s.center = (x, y)
        pygame.draw.rect(screen, blue, s)
    
    #for i in range(board_size2+1):
    #    pygame.draw.line(screen, black, (board_width*i, 0), (board_width*i, display.height*2))
    # for i in range(board_size1+1):
    #     pygame.draw.line(screen, black, (0, board_height*i), (display.width*2, board_height*i))

def pygame_running():
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            return False
            pygame.quit()
        else:
            return True

def update_inputs(inputs):
  keys=pygame.key.get_pressed()
  inputs['last_mouse_down'] = inputs['mouse_down']
  inputs['mouse_down'] = pygame.mouse.get_pressed()[0]
  (inputs['mouse_x'], inputs['mouse_y']) = pygame.mouse.get_pos()
  inputs['W']=keys[K_w]
  inputs['A']=keys[K_a]
  inputs['S']=keys[K_s]
  inputs['D']=keys[K_d]
  inputs['SPACE']=keys[K_SPACE]
  inputs['UP']=keys[K_UP]
  inputs['DOWN']=keys[K_DOWN]
  inputs['RIGHT']=keys[K_RIGHT]
  inputs['LEFT']=keys[K_LEFT]
  #screen.fill("White")
  return inputs
  
def input_handler(inputs, model, g):
    x = int(inputs['mouse_x']/(display.width*2/display.board_width))
    y = int(inputs['mouse_y']/(display.height*2/display.board_height))
    if inputs['mouse_down'] and not inputs['last_mouse_down']:
        if model.start is None:
            model.start = (x, y)
        else:
            model.queue.append((x, y))
            
    if inputs['W']:
        print(g)
        print(f"first bfs: {bfs(g, model.start)}")
    return model
  
def update_screen():
    pygame.display.flip()

#undirected graph
class Graph():
    #edges are a default dict adjency list
    #weights is a default dict mapping (v1, v2) to a weight
    def __init__(self, nvertices=0, edges = defaultdict(set), directed=False, weights = {}):
        self.edges = edges
        if nvertices == 0:
            self.update_nvertices()
        else:
            self.v = nvertices
        if directed == False:
            self.update_undirected_edges()
        self.weights = weights
    
    def add_v(self, name, edge_list):
        self.v += 1
        self.edges[name] = set(edge_list)
    
    def add_edge(self, v1, v2):
        self.edges[v1].add(v2)
        
    def cleanup(edges, weights, all_v):
        all_v = list(all_v)
        all_v.sort()
        index = {v : i for i,v in enumerate(all_v)}
        edges2 = defaultdict(list)
        for v, neighbors in edges.items():
            edges2[index[v]] = [index[v2] for v2 in neighbors]
        weights2 = defaultdict(int)
        for (v1, v2), weight in weights.items():
            weights2[index[v1], index[v2]] = weight
        return (edges2, weights2)

    def update_nvertices(self):
        self.v = len(self.edges)
    def update_undirected_edges(self):
        for v, neighbors in self.edges.items():
            for v2 in neighbors:
                if v not in self.edges[v2]:
                    self.edges[v2].append(v)
    
    def print_edges(self, edges):
        ans = ""
        for v, neighbors in edges.items():
            ans += f"\n{v}: {neighbors}"
        return ans
    
    def print_weights(self, weights):
        ans = ""
        for (v1, v2), w in weights.items():
            ans += f"\n({v1}, {v2}): {w}"
        return ans
    
    def __repr__(self):
        return f"[Graph, V={self.v}, E={self.print_edges(self.edges)}, W={self.print_weights(self.weights)}]"

def bfs(graph, start):
    queue = deque()
    visited = []
    queue.append(start)
    while queue:
        current  = queue.popleft()
        if current in visited:
            continue
        visited.append(current)
        neighbors = graph.edges[current]
        for n in neighbors:
            if n in visited:
                continue
            queue.extend(neighbors)
    return visited

if __name__ == '__main__':
  main()