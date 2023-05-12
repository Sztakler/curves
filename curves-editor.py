from ctypes.wintypes import RGB
from functools import reduce
from math import *
import sys

import numpy
import pygame
import pygame_gui

import CurveDrawer


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def getCoordinates(self):
        return [self.x, self.y]

class Menu:
    def __init__(self, manager, elements, margin, padding, height):
        self.manager = manager
        self.elements = elements
        self.margin = margin
        self.padding = padding
        self.height = height
       
    def set_layout(self):
        for i in range(len(self.elements)):
            self.elements[i].manager = self.manager

            

class CurvesEditor:
    def __init__(self):
        self.window_size = (1366, 768)
        self.curveDrawers = []
        self.clock = pygame.time.Clock()
        self.is_running = True
        self.user_points = []
        self.points = []
        self.colorscheme = {
            "bg": self.hex_to_rgb("#282828"),
            "red": self.hex_to_rgb("#cc241d"),
            "green": self.hex_to_rgb("#98971a"),
            "yellow": self.hex_to_rgb("#d79921"),
            "blue": self.hex_to_rgb("#458588"),
            "purple": self.hex_to_rgb("#b16286"),
            }

        self.window_size = (1368, 768)
        pygame.init() 
        pygame.display.set_caption('Curves Editor')
        self.window_surface = pygame.display.set_mode(self.window_size)
        self.menu = Menu(
                pygame_gui.UIManager(self.window_size),
            [
                pygame_gui.elements.UIButton(relative_rect=pygame.Rect(5,5,100, 30), text="Say Hello", manager=None, anchors={'top': 'top', 'left': 'left'}),
                pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect(110,5,300,30), manager=None, anchors={'top': 'top', 'left': 'left'}),
                pygame_gui.elements.UIButton(relative_rect=pygame.Rect(415,5,100,30), text="Clear", manager=None, anchors={'top': 'top', 'left': 'left'}),
                pygame_gui.elements.UIButton(relative_rect=pygame.Rect(520,5,100,30), text="MoveLeft", manager=None, anchors={'top': 'top', 'left': 'left'}),
                pygame_gui.elements.UIButton(relative_rect=pygame.Rect(625,5,100,30), text="MoveRight", manager=None, anchors={'top': 'top', 'left': 'left'}),
                pygame_gui.elements.UIButton(relative_rect=pygame.Rect(730,5,100,30), text="MoveUp", manager=None, anchors={'top': 'top', 'left': 'left'}),
                pygame_gui.elements.UIButton(relative_rect=pygame.Rect(835,5,100,30), text="MoveDown", manager=None, anchors={'top': 'top', 'left': 'left'}),
                pygame_gui.elements.UIButton(relative_rect=pygame.Rect(940,5,150,30), text="Toggle Image", manager=None, anchors={'top': 'top', 'left': 'left'}),
            ],
            margin=5,
            padding=5,
            height=30)
        self.menu.set_layout()

        self.background_image_path = None
        if (len(sys.argv) > 1):
            self.background_image_path = sys.argv[1]

        self.background_image = None
        if self.background_image_path != None:
            self.background_image = pygame.image.load(self.background_image_path)
         
        self.is_background_image_rendered = True
        self.isConvexHullRendered = False
        self.is_dragging = False
        self.moving = False
        self.direction = "left"
        self.rotation = False
        self.rotation_direction = "clockwise"
        self.pivot = None

    def hex_to_rgb(self, value):
        value = value.lstrip('#')
        lv = len(value)
        return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))
    
    
    def process_input(self, input):
        x_fun = sin
        y_fun = cos
        t_range = [0, pi, 1000]
        t = 0
    
        parts = input.split(';')
      
        n_args = len(parts)
        if n_args >= 1 and parts[0] != "":
            x_fun = eval(parts[0])
        if n_args >= 2:
            y_fun = eval(parts[1])
        if n_args >= 3:
            t_args = eval(parts[2])
            t_args_length = len(t_args)
            if t_args_length >= 1:
                t_range[0] = t_args[0]
            if t_args_length >= 2:
                t_range[1] = t_args[1]
            if t_args_length >= 3:
                t_range[2] = t_args[2]
    
    
        t_start = t_range[0]
        t_stop  = t_range[1]
        t_step  = t_range[2]
    
        ts = numpy.linspace(t_start, t_stop, t_step)
    
        points = []
        size = 100.0
        for t in ts:
            point = Point(x_fun(t) * size + 200, y_fun(t) * size + 200)
            points.append(point)
            
        return points
   
    def update(self, mouse_position=None):
        if mouse_position != None:
            point = Point(mouse_position[0], mouse_position[1])
            if point.x < self.menu.height:
                return
            else:
                self.user_points.append(point)
        for curveDrawer in self.curveDrawers:
            curveDrawer.update(self.user_points)

    def render(self):
        if len(self.points) >= 2:
            parametric_curve = pygame.Surface(self.window_size)
            pygame.draw.aalines(parametric_curve, 'white', closed=False, points=self.points);
            self.window_surface.blit(parametric_curve, (0, 0))
        
        self.window_surface.fill(self.colorscheme["bg"])
        if self.background_image != None and self.is_background_image_rendered == True:
            self.window_surface.blit(self.background_image, (200,200))
        
        # convex_hull = self.get_convex_hull()
        convex_hull = self.GrahamScan()
        if len(convex_hull) > 2 and self.isConvexHullRendered:
            pygame.draw.aalines(self.window_surface, self.colorscheme["purple"], closed=True, points=convex_hull);
        
        for point in self.user_points:
            pygame.draw.circle(self.window_surface, self.colorscheme["green"], point.getCoordinates(), 3.0)
            self.curveDrawers[0].draw(surface=self.window_surface, color=self.colorscheme["blue"])
            self.curveDrawers[1].draw(surface=self.window_surface, color=self.colorscheme["red"])
            self.curveDrawers[2].draw(surface=self.window_surface, color=self.colorscheme["green"])

        
        self.menu.manager.draw_ui(self.window_surface)
        
        pygame.display.update()
    
    def move_points(self, direction):
        if len(self.user_points) < 1:
            return

        if direction == "left":
            for point in self.user_points:
                point.x -= 10
        if direction == "right":
            for point in self.user_points:
                point.x += 10
        if direction == "up":
            for point in self.user_points:
                point.y -= 10
        if direction == "down":
            for point in self.user_points:
                point.y += 10
        self.update()
    
    def toggle_background_image(self):
        self.is_background_image_rendered = not self.is_background_image_rendered

    def get_point_under_cursor_index(self):
        mouse_position = pygame.mouse.get_pos()
        size = [10, 10]
        collider = pygame.Rect(mouse_position[0] - size[0]/2, mouse_position[1] - size[1]/2, size[0], size[1])
        pygame.draw.rect(self.window_surface, self.colorscheme["red"], collider) 
        collider_surface = pygame.Surface(self.window_size)
        pygame.draw.rect(collider_surface, 'red', collider);
        self.window_surface.blit(collider_surface, mouse_position)
        for point in self.user_points:
            if collider.collidepoint(point.x, point.y):
                return self.user_points.index(point)
        return None        


    def get_point_under_cursor(self):
        mouse_position = pygame.mouse.get_pos()
        size = [10, 10]
        collider = pygame.Rect(mouse_position[0] - size[0]/2, mouse_position[1] - size[1]/2, size[0], size[1])
        pygame.draw.rect(self.window_surface, self.colorscheme["red"], collider) 
        collider_surface = pygame.Surface(self.window_size)
        pygame.draw.rect(collider_surface, 'red', collider);
        self.window_surface.blit(collider_surface, mouse_position)
        for point in self.user_points:
            if collider.collidepoint(point.x, point.y):
                return point
        return None        

    def remove_point(self, point):
        if point != None:
            self.rotation_direction = "clockwise"
            self.user_points.remove(point)
            self.rotation_direction = "clockwise"

    def rotate_point(self, pivot, point, direction):
        point.x -= pivot[0]
        point.y -= pivot[1]

        angle = pi / 100

        new_point = Point(point.x, point.y)

        if direction == "clockwise":
            new_point.x = point.x * cos(angle) + point.y * sin(angle)
            new_point.y = -point.x * sin(angle) + point.y * cos(angle)
        else:        
            new_point.x = point.x * cos(angle) - point.y * sin(angle)
            new_point.y = point.x * sin(angle) + point.y * cos(angle)
        

        point.x = new_point.x + pivot[0] 
        point.y = new_point.y + pivot[1] 

    def toggleHull(self):
        self.isConvexHullRendered = not self.isConvexHullRendered
    
    def get_convex_hull(self):
        def findSide(p1, p2, p):
            val = (p.y - p1.y) * (p2.x - p1.x) - (p2.y - p1.y) * (p.x - p1.x)
     
            if val > 0:
                return 1
            if val < 0:
                return -1
            return 0

        def lineDist(p1, p2, p):
            return abs((p.y - p1.y) * (p2.x - p1.x) -
                (p2.y - p1.y) * (p.x - p1.x))

        hull = []

        def quickHull(a, n, p1, p2, side):
            ind = -1
            max_dist = 0
         
            # finding the point with maximum distance
            # from L and also on the specified side of L.
            for i in range(n):
                temp = lineDist(p1, p2, a[i])
                 
                if (findSide(p1, p2, a[i]) == side) and (temp > max_dist):
                    ind = i
                    max_dist = temp
         
            # If no point is found, add the end points
            # of L to the convex hull.
            if ind == -1:
                hull.append(p1)
                hull.append(p2)
                return
         
            # Recur for the two parts divided by a[ind]
            quickHull(a, n, a[ind], p1, -findSide(a[ind], p1, p2))
            quickHull(a, n, a[ind], p2, -findSide(a[ind], p2, p1))

        

        n = len(self.user_points)
        a = self.user_points[:]
        if (n < 3):
            print("Convex hull not possible")
            return
     
        # Finding the point with minimum and
        # maximum x-coordinate
        min_x = 0
        max_x = 0
        for i in range(1, n):
            if a[i].x < a[min_x].x:
                min_x = i
            if a[i].x > a[max_x].x:
                max_x = i
     
        # Recursively find convex hull points on
        # one side of line joining a[min_x] and
        # a[max_x]
        quickHull(a, n, a[min_x], a[max_x], 1)
     
        # Recursively find convex hull points on
        # other side of line joining a[min_x] and
        # a[max_x]
        quickHull(a, n, a[min_x], a[max_x], -1)

        hullPoints = [[point.x, point.y] for point in list(hull)]
     
        print(hullPoints)
        return hullPoints
            

    def GrahamScan(self):
        '''
        Returns points on convex hull in CCW order according to Graham's scan algorithm. 
        By Tom Switzer <thomas.switzer@gmail.com>.
        '''
        points = [[point.x, point.y] for point in self.user_points]
        TURN_LEFT, TURN_RIGHT, TURN_NONE = (1, -1, 0)

        def cmp(a, b):
            return (a > b) - (a < b)

        def turn(p, q, r):
            return cmp((q[0] - p[0])*(r[1] - p[1]) - (r[0] - p[0])*(q[1] - p[1]), 0)

        def _keep_left(hull, r):
            while len(hull) > 1 and turn(hull[-2], hull[-1], r) != TURN_LEFT:
                hull.pop()
            if not len(hull) or hull[-1] != r:
                hull.append(r)
            return hull

        points = sorted(points)
        l = reduce(_keep_left, points, [])
        u = reduce(_keep_left, reversed(points), [])
        return l.extend(u[i] for i in range(1, len(u) - 1)) or l        
            
    def start(self): 
        def get_chebyshev_nodes(points):
            n = len(points)
            result = []
            for k in range(n + 1)[1:]:
                result.append( 
                    cos( 
                        ((2*k - 1) / (2*n)) * pi) )
            return result
        
        curveDrawerInterpol = CurveDrawer.CurveDrawer(user_points=self.user_points, interpolation_method="lagrange", nodes_method=get_chebyshev_nodes, ts_len=1000)
        curveDrawerSpline = CurveDrawer.CurveDrawer(user_points=self.user_points, interpolation_method="spline", ts_len=1000)
        curveDrawerBezier = CurveDrawer.CurveDrawer(user_points=self.user_points, interpolation_method="bezier", ts_len=1000)
        self.curveDrawers.append(curveDrawerInterpol)
        self.curveDrawers.append(curveDrawerSpline)
        self.curveDrawers.append(curveDrawerBezier)

        MODSHIFT = False
        while self.is_running:
            time_delta = self.clock.tick(60)/1000.0
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LSHIFT:
                       MODSHIFT = True
                    if event.key == pygame.K_LEFT:
                        self.moving = True
                        self.direction = "left"
                    if event.key == pygame.K_RIGHT:
                        self.moving = True
                        self.direction = "right"
                    if event.key == pygame.K_UP:
                        self.moving = True
                        self.direction = "up"
                    if event.key == pygame.K_DOWN:
                        self.moving = True
                        self.direction = "down"
                    if event.key == pygame.K_h:
                        self.toggleHull()
                    if event.key == pygame.K_r:
                        self.rotation = True
                        self.rotation_direction = "clockwise"
                        if MODSHIFT:
                            self.rotation_direction = "counter-clockwise"
                        self.pivot = list(pygame.mouse.get_pos())
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LSHIFT:
                        self.is_dragging = False
                        MODSHIFT = False
                    if event.key in [pygame.K_RIGHT, pygame.K_LEFT, pygame.K_DOWN, pygame.K_UP]:
                        self.moving = False
                    if event.key == pygame.K_r:
                        self.rotation = False
                if event.type == pygame.QUIT:
                    self.is_running = False
                
                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.menu.elements[0]:
                        print("Hello!")
                    if event.ui_element == self.menu.elements[2]:
                        self.user_points = []
                    if event.ui_element == self.menu.elements[3]:
                        self.move_points("left")
                    if event.ui_element == self.menu.elements[4]:
                        self.move_points("right")
                    if event.ui_element == self.menu.elements[5]:
                        self.move_points("up")
                    if event.ui_element == self.menu.elements[6]:
                        self.move_points("down")
                    if event.ui_element == self.menu.elements[7]:
                        self.toggle_background_image()
                if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED:
                    if event.ui_element == self.menu.elements[1]:
                        self.points = self.process_input(self.menu.elements[1].get_text())
                self.menu.manager.process_events(event)
 
                if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            if MODSHIFT:
                                self.is_dragging = True
                                self.index = self.get_point_under_cursor_index()
                            else:
                                self.update(pygame.mouse.get_pos())
                        if event.button == 3:
                            if MODSHIFT:
                                # add new point
                                pass
                            else:
                                self.remove_point(self.get_point_under_cursor())
                                self.update()
                
            self.menu.manager.update(time_delta)
           
            if self.moving:
                self.move_points(self.direction)

            if self.is_dragging:
                if self.index != None:
                    mouse_position = pygame.mouse.get_pos()
                    point = Point(mouse_position[0], mouse_position[1])
                    self.user_points[self.index] = point
                    
                if len(self.user_points) >= 2:
                    self.update()

            if self.rotation:
                for point in self.user_points:
                    self.rotate_point(self.pivot, point, self.rotation_direction)
                self.update()
                    
            self.render()

curvesEditor = CurvesEditor()
curvesEditor.start()

