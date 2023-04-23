from ctypes.wintypes import RGB
import pygame
import pygame_gui
from math import *
import numpy
import CurveDrawer

colorscheme = {
        "bg": "#282828",
        "red": "#cc241d",
        "green": "#98971a",
        "yellow": "#d79921",
        "blue": "458588",
        "purple": "b16286",
        }

screen_res = (1368, 768)

def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

def process_input(input):
    # x_fun = numpy.identity
    # y_fun = numpy.identity
    # t_range = [0, 1, 1000]
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

pygame.init()

pygame.display.set_caption('Curve Editor')
window_surface = pygame.display.set_mode(screen_res)

background = pygame.Surface(screen_res)
background.fill((255, 255, 255))

manager = pygame_gui.UIManager(screen_res)

button_layout_rect = pygame.Rect(5, 5, 100, 30)
hello_button = pygame_gui.elements.UIButton(relative_rect=button_layout_rect, text="Say Hello", manager=manager, anchors={'top': 'top', 'left': 'left'})

formula_input_layout_rect = pygame.Rect(110, 5, 300, 30)
formula_input = pygame_gui.elements.UITextEntryLine(relative_rect=formula_input_layout_rect, manager=manager, anchors={'top': 'top', 'left': 'left'})

clock = pygame.time.Clock()
is_running = True

def chebyshev_nodes(n, interval):
    nodes = []
    for k in range(0, n + 1):
        nodes.append(cos((2 * k + 1) * pi / (2 * n + 2)))
        # nodes.append( (0.5 * (interval[0] + interval[1]) + (interval[1] - interval[0]) * cos((2*k + 1) * pi / (2 * (n+2))) ) )
    return nodes

points = []
nodes_points = []
while is_running:
    time_delta = clock.tick(60)/1000.0


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
        
        left_mouse_button_lock = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            left_mouse_button_lock = True
            nodes_points.append(pygame.mouse.get_pos())
        if event.type == pygame.MOUSEBUTTONUP:
            left_mouse_button_lock = False
        
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == hello_button:
                print("Hello!")
        if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED:
            if event.ui_element == formula_input:
                points = process_input(formula_input.get_text())
        manager.process_events(event)

    manager.update(time_delta)

    # curveDrawer = CurveDrawer.CurveDrawer(nodes_points, numpy.linspace(0, 1, len(nodes_points)))
    curveDrawer = CurveDrawer.CurveDrawer(nodes_points,chebyshev_nodes(len(nodes_points) - 1, (0,0,11))) 
    # curveDrawer.print()
    window_surface.blit(background, (0, 0))

    if len(points) >= 2:
        parametric_curve = pygame.Surface(screen_res)
        pygame.draw.aalines(parametric_curve, 'white', closed=False, points=points);
        window_surface.blit(parametric_curve, (0, 0))

    points_surface = pygame.Surface(screen_res)
    points_surface.fill(hex_to_rgb(colorscheme["bg"]))
    for point in nodes_points:
        pygame.draw.circle(points_surface, hex_to_rgb(colorscheme["green"]), point, 2.0)
    if len(nodes_points) >= 2:
        line = curveDrawer.draw(numpy.linspace(-1, 1, 5000))
        line_surface = pygame.Surface(screen_res)
        pygame.draw.aalines(points_surface, hex_to_rgb(colorscheme["yellow"]), closed=False, points=line);
    window_surface.blit(points_surface, (0, 0))
    
    manager.draw_ui(window_surface)
    
    
    pygame.display.update()

