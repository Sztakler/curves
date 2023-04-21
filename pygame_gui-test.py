import pygame
import pygame_gui
from math import *
import numpy
import CurveDrawer

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

pygame.display.set_caption('Quick Start')
window_surface = pygame.display.set_mode((800, 600))

background = pygame.Surface((800, 600))
background.fill(pygame.Color('#000000'))

manager = pygame_gui.UIManager((800, 600))

button_layout_rect = pygame.Rect(5, 5, 100, 30)
hello_button = pygame_gui.elements.UIButton(relative_rect=button_layout_rect, text="Say Hello", manager=manager, anchors={'top': 'top', 'left': 'left'})

formula_input_layout_rect = pygame.Rect(110, 5, 300, 30)
formula_input = pygame_gui.elements.UITextEntryLine(relative_rect=formula_input_layout_rect, manager=manager, anchors={'top': 'top', 'left': 'left'})

clock = pygame.time.Clock()
is_running = True


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

    curveDrawer = CurveDrawer.CurveDrawer(nodes_points)
    curveDrawer.print()
    window_surface.blit(background, (0, 0))

    if len(points) >= 2:
        parametric_curve = pygame.Surface((800, 600))
        pygame.draw.aalines(parametric_curve, 'white', closed=False, points=points);
        window_surface.blit(parametric_curve, (0, 0))

    if len(nodes_points) > 2:
        points_surface = pygame.Surface((800, 600))
        for point in nodes_points:
            pygame.draw.circle(points_surface, "green", point, 2.0)
        # window_surface.blit(points_surface, (0, 0))

        line = curveDrawer.draw(window_surface)
        line_surface = pygame.Surface((800, 600))
        pygame.draw.aalines(points_surface, 'yellow', closed=False, points=line);
        window_surface.blit(points_surface, (0, 0))
        # pygame.draw.aalines(points_surface, "green", false, )
    
    manager.draw_ui(window_surface)
    
    
    pygame.display.update()

