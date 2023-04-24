from ctypes.wintypes import RGB
from math import *
import sys

import numpy
import pygame
import pygame_gui

import CurveDrawer

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
        print()
        if (len(sys.argv) > 1):
            self.background_image_path = sys.argv[1]

        self.background_image = None
        if self.background_image_path != None:
            self.background_image = pygame.image.load(self.background_image_path)
         
        self.is_background_image_rendered = True

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
            points.append((x_fun(t) * size + 200, y_fun(t) * size + 200))
        
    
        return points
   
    def update(self, mouse_position=None):
        if mouse_position != None:
            mouse_position = list(mouse_position)
            if mouse_position[1] < self.menu.height:
                return
            else:
                self.user_points.append(mouse_position)

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
        
        for point in self.user_points:
            pygame.draw.circle(self.window_surface, self.colorscheme["green"], point, 3.0)
            self.curveDrawers[0].draw(surface=self.window_surface, color=self.colorscheme["blue"])
            self.curveDrawers[1].draw(surface=self.window_surface, color=self.colorscheme["red"])
        
        self.menu.manager.draw_ui(self.window_surface)
        
        pygame.display.update()
    
    def move_points(self, direction):
        if len(self.user_points) < 1:
            return

        if direction == "left":
            for point in self.user_points:
                point[0] -= 10
        if direction == "right":
            for point in self.user_points:
                point[0] += 10
        if direction == "up":
            for point in self.user_points:
                point[1] -= 10
        if direction == "down":
            for point in self.user_points:
                point[1] += 10
        self.update()
    
    def toggle_background_image(self):
        self.is_background_image_rendered = not self.is_background_image_rendered

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
        self.curveDrawers.append(curveDrawerInterpol)
        self.curveDrawers.append(curveDrawerSpline)

        while self.is_running:
            time_delta = self.clock.tick(60)/1000.0
        
            for event in pygame.event.get():
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
                    self.update(pygame.mouse.get_pos())
                
            self.menu.manager.update(time_delta)
        
            self.render()

curvesEditor = CurvesEditor()
curvesEditor.start()

