
import math, pygame, random
from collections import defaultdict
from pygame.locals import *
from collections import deque
import colorsys

def init():
  global clock, display
  size = 15
  display = Display(size, size)
  pygame.init()
  clock = pygame.time.Clock()
  pygame.display.set_caption("DEMO PROGRAM 1")
  keys=pygame.key.get_pressed()

class Display:
    def __init__(self, board_height = 8, board_width = 8):
        self.board_height = board_height
        self.board_width = board_width
        self.width = 210
        self.height = 210
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
        self.visited2 = set()
        self.processing = set()
        self.processed = set()
        self.start = None
        self.running = True
        self.timer = 0
        self.times = defaultdict(lambda: None)
        self.drawmode = 1

def main():
  init()
  model = Model(display.board_height, display.board_width)
  global input
  (model, g) = loadmaze(model, input)
  inputs={'mouse_down':False, 'last_mouse_down':False, 'mouse_x':0, 'mouse_y':0, 'W':False, 'A':False, 'S':False, 'D':False, 'SPACE':False,
  'UP':False,'DOWN':False, 'RIGHT':False, 'LEFT':False, '1':False, '2':False, '3':False}
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
        g.add_v(model.start, [])
        model.queue.append(model.start)
    if g is not None and step%1 == 0:
        #change between bfs and dfs
        (g, model) = update_dfs(g, model)
    model = draw_handler(model)
    update_screen()
    step += 1

def update_bfs(g, model):
    if not model.queue:
        return (g, model)
    current = model.queue.popleft()
    if current in model.processed:
        return (g, model)
    x, y = current
    if x<0:
        current = (-1-x, -1-y)
        start, end = model.times[current]
        model.times[current] = (start, model.timer)
        model.timer += 1
        return (g, model)
    if current not in model.processing:
        model.times[current] = (model.timer, -1)
        model.timer += 1
    model.processing.add(current)
    neighbors = check_edges(model, current)
    g.add_v(current, neighbors)
    for v in neighbors:
        if v in model.visited:
            continue
        model.visited.add(v)
        model.queue.append(v)
    model.processed.add(current)
    model.queue.append((-1-x, -1-y))
    return (g, model)

def update_dfs(g, model):
    if not model.queue:
        return (g, model)
    current = model.queue.pop()
    if current in model.processed:
        return (g, model)
    x, y = current
    if x<0:
        current = (-1-x, -1-y)
        start, end = model.times[current]
        model.times[current] = (start, model.timer)
        model.timer += 1
        return (g, model)
    if current not in model.processing:
        model.times[current] = (model.timer, -1)
        model.timer += 1
    model.processing.add(current)
    neighbors = check_edges(model, current)
    g.add_v(current, neighbors)
    model.queue.append((-1-x, -1-y))
    for v in neighbors:
        if v in model.visited:
            continue
        model.visited.add(v)
        model.queue.append(v)
    model.processed.add(current)
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
    
def make_walls(model):
    # columns:
    for row in range(model.board_height):
        for wall in range(model.board_width-1):
            model.walls[(wall, row)].add(1)
            model.walls[(wall+1, row)].add(3)
    # rows:
    for column in range(model.board_width):
        for wall in range(model.board_height-1):
            model.walls[(column, wall)].add(2)
            model.walls[(column, wall+1)].add(0)
            
def loadmaze(model, input):
    make_walls(model)
    g = Graph.from_string(input)
    for v1, neighbors in g.edges.items():
        x1, y1 = v1
        for v2 in neighbors:
            x2, y2 = v2
            if x2 == x1 and y2 == y1-1:
                if 0 in model.walls[v1]:
                    model.walls[v1].remove(0)
                if 2 in model.walls[v2]:
                    model.walls[v2].remove(2)
            if x2 == x1+1 and y2 == y1:
                if 1 in model.walls[v1]:
                    model.walls[v1].remove(1)
                if 3 in model.walls[v2]:
                    model.walls[v2].remove(3)
            if x2 == x1 and y2 == y1+1:
                if 2 in model.walls[v1]:
                    model.walls[v1].remove(2)
                if 0 in model.walls[v2]:
                    model.walls[v2].remove(0)
            if x2 == x1-1 and y2 == y1:
                if 3 in model.walls[v1]:
                    model.walls[v1].remove(3)
                if 1 in model.walls[v2]:
                    model.walls[v2].remove(1)
    return (model, g)
    
def draw_handler(model):
  screen = display.screen
  if model.drawmode == 1:
    bgcolor = pygame.color.Color("orange")
  else:
    bgcolor = pygame.color.Color("white")
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
    
    
    if model.drawmode == 1:
        red = pygame.color.Color("red") 
        for square in model.visited:
            if square in model.processed:
                continue
            (i, j) = square
            (y, x) = (board_width*(j+1/2), board_height * (i+1/2))
            s = pygame.Rect(0, 0, board_width-3, board_height-3)
            s.center = (x, y)
            pygame.draw.rect(screen, blue, s)
            
        for square in model.processed:
            (i, j) = square
            (y, x) = (board_width*(j+1/2), board_height * (i+1/2))
            s = pygame.Rect(0, 0, board_width-3, board_height-3)
            s.center = (x, y)
            pygame.draw.rect(screen, red, s)
    elif model.drawmode == 2:
        for square in model.visited:
            if model.times[square] is None:
                continue
            start, end = model.times[square]
            hue = start/(display.board_height*display.board_width*2.3)
            r, g, b = colorsys.hsv_to_rgb(hue, 1, 1)
            color = (int(r * 255), int(g * 255), int(b * 255))
            (i, j) = square
            (y, x) = (board_width*(j+1/2), board_height * (i+1/2))
            s = pygame.Rect(0, 0, board_width-3, board_height-3)
            s.center = (x, y)
            pygame.draw.rect(screen, color, s)
    elif model.drawmode == 3:
        for square in model.processed:
            if model.times[square] is None:
                continue
            start, end = model.times[square]
            if end == -1:
                continue
            hue = end/(display.board_height*display.board_width*2.3)
            r, g, b = colorsys.hsv_to_rgb(hue, 1, 1)
            color = (int(r * 255), int(g * 255), int(b * 255))
            (i, j) = square
            (y, x) = (board_width*(j+1/2), board_height * (i+1/2))
            s = pygame.Rect(0, 0, board_width-3, board_height-3)
            s.center = (x, y)
            pygame.draw.rect(screen, color, s)
        

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
  inputs['1']=keys[K_1]
  inputs['2']=keys[K_2]
  inputs['3']=keys[K_3]
  #screen.fill("White")
  return inputs
  
def input_handler(inputs, model, g):
    x = int(inputs['mouse_x']/(display.width*2/display.board_width))
    y = int(inputs['mouse_y']/(display.height*2/display.board_height))
    if inputs['mouse_down'] and not inputs['last_mouse_down']:
        if model.start is None:
            model.start = (x, y)
            model.visited.add((x, y))
        
    if inputs['W']:
        print(f"graph: {g}")
    if inputs['1']:
        model.drawmode = 1
    if inputs['2']:
        model.drawmode = 2
    if inputs['3']:
        model.drawmode = 3
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
        
    def process_edge_line(line, edges, all_v, directed):
        vertices =  list(map(eval, line))
        for v in vertices:
            all_v.add(v)
        edges[vertices[0]] = set(vertices)
        if not directed:
            for v in vertices[1:]:
                edges[v].add(vertices[0])

    def process_weight_line(line, weights, directed):
        input = list(map(eval, line))
        v1 = input[0]
        v2 = input[1]
        weight = input[2]
        weights[(v1, v2)] = weight
        if not directed:
            weights[(v2, v1)] = weight

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
        
    # cls, the class, which is going to be Graph
    # openfile, a TextIO object, which acts just like an open file
    @classmethod
    def from_string(cls, string, directed=False):
        lines = string.split('\n')
        edges = defaultdict(set)
        weights = defaultdict(int)
        all_v = set()
        is_weight = False
        for row in lines:
            row = row[:-1]
            line = row.strip()
            if str(row) == '# WEIGHTS':
                is_weight = True
                continue
            if not line:
                continue
            if line[0] == '#':
                continue
            line = line.split()
            if is_weight:
                cls.process_weight_line(line, weights, directed)
            else:
                cls.process_edge_line(line, edges, all_v, directed)

        #edges, weights = cls.cleanup(edges, weights, all_v)
        return Graph(len(all_v), edges, directed, weights)

    def update_nvertices(self):
        self.v = len(self.edges)
    def update_undirected_edges(self):
        for v, neighbors in self.edges.items():
            for v2 in neighbors:
                if v not in self.edges[v2]:
                    self.edges[v2].add(v)
    
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
        
    def repr2(self):
        ans = "String repersentation: \n"
        for v1, edges in self.edges.items():
            ans += str(v1) + " "
            for v2 in edges:
                ans += str(v2) + " "
            ans += "\n"
        return ans

input = '''(0,0) (1,0) 
(0,1) (0,2) (0,0) 
(0,2) (0,1) (1,2) 
(1,2) (0,2) (1,3) 
(1,3) (1,2) (1,4) 
(1,4) (1,3) (1,5) 
(1,5) (1,4) (0,5) 
(0,5) (0,4) (0,6) (1,5) 
(0,6) (0,7) (0,5) 
(0,7) (1,7) (0,6) 
(1,7) (0,7) (1,8) 
(1,8) (1,7) (0,8) 
(0,8) (1,8) (0,9) 
(0,9) (0,8) (1,9) 
(1,9) (0,9) (1,10) 
(1,10) (2,10) (1,9) 
(2,10) (2,9) (1,10) 
(2,9) (2,10) (3,9) 
(3,9) (4,9) (2,9) 
(4,9) (4,10) (3,9) 
(4,10) (4,9) (5,10) 
(5,10) (4,10) (5,11) 
(5,11) (5,10) (5,12) 
(5,12) (4,12) (5,11) 
(4,12) (4,13) (5,12) 
(4,13) (3,13) (4,12) 
(3,13) (3,14) (4,13) 
(3,14) (2,14) (3,13) (4,14) 
(4,14) (5,14) (3,14) 
(5,14) (6,14) (4,14) 
(6,14) (5,14) (7,14) 
(7,14) (8,14) (6,14) 
(8,14) (9,14) (7,14) 
(9,14) (8,14) (9,13) 
(9,13) (10,13) (9,14) 
(10,13) (11,13) (9,13) 
(11,13) (11,12) (10,13) 
(11,12) (11,13) (12,12) 
(12,12) (11,12) (12,13) 
(12,13) (12,12) (13,13) 
(13,13) (14,13) (12,13) 
(14,13) (14,12) (14,14) (13,13) 
(14,12) (14,13) (13,12) 
(13,12) (14,12) (13,11) 
(13,11) (12,11) (13,12) 
(12,11) (12,10) (13,11) 
(12,10) (12,11) (13,10) 
(13,10) (12,10) (13,9) 
(13,9) (13,10) (12,9) 
(12,9) (13,9) (12,8) 
(12,8) (13,8) (12,9) 
(13,8) (12,8) (13,7) 
(13,7) (13,8) (13,6) 
(13,6) (13,5) (13,7) 
(13,5) (13,6) (14,5) 
(14,5) (14,6) (13,5) (14,4) 
(14,6) (14,7) (14,5) 
(14,7) (14,6) (14,8) 
(14,8) (14,7) (14,9) 
(14,9) (14,8) (14,10) 
(14,10) (14,9) (14,11) 
(14,11) (14,10) 
(14,4) (13,4) (14,5) 
(13,4) (12,4) (14,4) 
(12,4) (13,4) (12,3) 
(12,3) (12,4) (13,3) 
(13,3) (14,3) (12,3) 
(14,3) (13,3) (14,2) 
(14,2) (14,1) (14,3) 
(14,1) (14,2) (14,0) 
(14,0) (14,1) (13,0) 
(13,0) (12,0) (14,0) 
(12,0) (13,0) (11,0) 
(11,0) (12,0) (10,0) 
(10,0) (10,1) (11,0) 
(10,1) (10,0) (10,2) 
(10,2) (10,1) (10,3) 
(10,3) (9,3) (10,2) 
(9,3) (8,3) (10,3) 
(8,3) (8,2) (9,3) 
(8,2) (8,3) (7,2) 
(7,2) (8,2) (6,2) 
(6,2) (6,1) (7,2) 
(6,1) (6,2) (7,1) 
(7,1) (6,1) (8,1) 
(8,1) (9,1) (7,1) 
(9,1) (9,0) (9,2) (8,1) 
(9,2) (9,1) 
(9,0) (9,1) (8,0) 
(8,0) (9,0) (7,0) 
(7,0) (8,0) (6,0) 
(6,0) (7,0) (5,0) 
(5,0) (5,1) (6,0) 
(5,1) (5,0) (4,1) 
(4,1) (3,1) (5,1) 
(3,1) (4,1) (3,0) 
(3,0) (3,1) (4,0) (2,0) 
(4,0) (3,0) 
(2,0) (2,1) (3,0) 
(2,1) (1,1) (2,0) (2,2) 
(2,2) (2,3) (2,1) 
(2,3) (3,3) (2,2) 
(3,3) (2,3) (4,3) 
(4,3) (3,3) (4,2) 
(4,2) (5,2) (3,2) (4,3) 
(5,2) (5,3) (4,2) 
(5,3) (5,4) (5,2) 
(5,4) (5,3) (4,4) 
(4,4) (4,5) (5,4) 
(4,5) (4,4) (4,6) 
(4,6) (4,5) (3,6) 
(3,6) (4,6) (3,5) 
(3,5) (3,4) (3,6) 
(3,4) (2,4) (3,5) 
(2,4) (2,5) (3,4) 
(2,5) (2,4) (2,6) 
(2,6) (1,6) (2,5) (2,7) 
(1,6) (2,6) 
(2,7) (2,6) (2,8) 
(2,8) (3,8) (2,7) 
(3,8) (4,8) (2,8) 
(4,8) (3,8) (4,7) 
(4,7) (3,7) (5,7) (4,8) 
(3,7) (4,7) 
(5,7) (6,7) (4,7) 
(6,7) (6,6) (5,7) 
(6,6) (6,7) (7,6) 
(7,6) (6,6) (7,5) 
(7,5) (7,6) (8,5) 
(8,5) (9,5) (7,5) 
(9,5) (8,5) (9,4) 
(9,4) (9,5) (8,4) (10,4) 
(10,4) (10,5) (9,4) 
(10,5) (10,4) (10,6) 
(10,6) (10,5) (9,6) 
(9,6) (9,7) (10,6) 
(9,7) (9,6) (9,8) 
(9,8) (9,7) (10,8) 
(10,8) (10,7) (9,8) 
(10,7) (11,7) (10,8) 
(11,7) (11,8) (10,7) (11,6) 
(11,6) (11,7) (12,6) 
(12,6) (12,5) (12,7) (11,6) 
(12,5) (12,6) (11,5) 
(11,5) (12,5) (11,4) 
(11,4) (11,3) (11,5) 
(11,3) (11,2) (11,4) 
(11,2) (11,1) (11,3) 
(11,1) (11,2) (12,1) 
(12,1) (11,1) (13,1) 
(13,1) (13,2) (12,1) 
(13,2) (12,2) (13,1) 
(12,2) (13,2) 
(12,7) (12,6) 
(11,8) (11,7) (11,9) 
(11,9) (10,9) (11,8) 
(10,9) (11,9) (9,9) 
(9,9) (10,9) (8,9) 
(8,9) (8,8) (9,9) 
(8,8) (8,7) (8,9) 
(8,7) (8,8) (7,7) (8,6) 
(8,6) (8,7) 
(7,7) (8,7) (7,8) 
(7,8) (6,8) (7,7) 
(6,8) (6,9) (7,8) 
(6,9) (7,9) (5,9) (6,8) 
(7,9) (7,10) (6,9) 
(7,10) (7,9) (7,11) 
(7,11) (7,10) (8,11) 
(8,11) (7,11) (8,12) 
(8,12) (8,13) (9,12) (8,11) 
(8,13) (7,13) (8,12) 
(7,13) (8,13) (6,13) 
(6,13) (6,12) (7,13) (5,13) 
(5,13) (6,13) 
(6,12) (6,13) (7,12) (6,11) 
(6,11) (6,12) (6,10) 
(6,10) (6,11) 
(7,12) (6,12) 
(9,12) (9,11) (8,12) 
(9,11) (9,10) (9,12) 
(9,10) (9,11) (8,10) (10,10) 
(10,10) (9,10) (11,10) 
(11,10) (10,10) (11,11) 
(11,11) (10,11) (11,10) 
(10,11) (10,12) (11,11) 
(10,12) (10,11) 
(8,10) (9,10) 
(5,9) (6,9) (5,8) 
(5,8) (5,9) 
(8,4) (7,4) (9,4) 
(7,4) (8,4) (7,3) 
(7,3) (7,4) (6,3) 
(6,3) (6,4) (7,3) 
(6,4) (6,3) (6,5) 
(6,5) (5,5) (6,4) 
(5,5) (5,6) (6,5) 
(5,6) (5,5) 
(3,2) (4,2) 
(1,1) (1,0) (2,1) 
(1,0) (1,1) (0,0) 
(14,14) (14,13) (13,14) 
(13,14) (14,14) (12,14) 
(12,14) (13,14) (11,14) 
(11,14) (12,14) (10,14) 
(10,14) (11,14) 
(2,14) (3,14) (2,13) 
(2,13) (2,14) (1,13) 
(1,13) (0,13) (2,13) 
(0,13) (0,14) (1,13) (0,12) 
(0,14) (0,13) (1,14) 
(1,14) (0,14) 
(0,12) (0,13) (0,11) 
(0,11) (0,12) (1,11) (0,10) 
(0,10) (0,11) 
(1,11) (1,12) (0,11) 
(1,12) (1,11) (2,12) 
(2,12) (3,12) (1,12) 
(3,12) (2,12) (3,11) 
(3,11) (3,12) (4,11) (2,11) (3,10) 
(4,11) (3,11) 
(2,11) (3,11) 
(3,10) (3,11) 
(0,4) (0,3) (0,5) 
(0,3) (0,4) 

'''

if __name__ == '__main__':
  main()