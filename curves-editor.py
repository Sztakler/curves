from ctypes.wintypes import RGB
import pygame
import pygame_gui
from math import *
import numpy
import CurveDrawer
import NaturalCubicSplines

def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

colorscheme = {
        "bg": hex_to_rgb("#282828"),
        "red": hex_to_rgb("#cc241d"),
        "green": hex_to_rgb("#98971a"),
        "yellow": hex_to_rgb("#d79921"),
        "blue": hex_to_rgb("#458588"),
        "purple": hex_to_rgb("#b16286"),
        }

screen_res = (1368, 768)


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

def get_chebyshev_nodes(points):
    n = len(points)
    result = []
    for k in range(n + 1)[1:]:
        result.append( 
            cos( 
                ((2*k - 1) / (2*n)) * pi) )
    return result

background_image = pygame.image.load('./apple-small.png')

points = []
user_points = []


curveDrawerInterpol = CurveDrawer.CurveDrawer(user_points=user_points, interpolation_method="lagrange", nodes_method=get_chebyshev_nodes, ts_len=1000)
curveDrawerSpline = CurveDrawer.CurveDrawer(user_points=user_points, interpolation_method="spline", ts_len=1000)

while is_running:
    time_delta = clock.tick(60)/1000.0


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
        
        left_mouse_button_lock = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            left_mouse_button_lock = True
            user_points.append(pygame.mouse.get_pos())
            curveDrawerInterpol.update(user_points)
            curveDrawerSpline.update(user_points)
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

    # curveDrawer = CurveDrawer.CurveDrawer(user_points, numpy.linspace(0, 1, len(user_points)))

    # cubicSpline = NaturalCubicSplines.NaturalCubicSplines(user_points)
    # curveDrawer.print()
    if len(points) >= 2:
        parametric_curve = pygame.Surface(screen_res)
        pygame.draw.aalines(parametric_curve, 'white', closed=False, points=points);
        window_surface.blit(parametric_curve, (0, 0))

    points_surface = pygame.Surface(screen_res)
    points_surface.fill(colorscheme["bg"])
    points_surface.blit(background_image, (0,0))

    for point in user_points:
        pygame.draw.circle(points_surface, colorscheme["green"], point, 3.0)
    if len(user_points) >= 2:
        # spline = cubicSpline.interpolate()
        curveDrawerInterpol.draw(surface=points_surface, color=colorscheme["blue"])
        curveDrawerSpline.draw(surface=points_surface, color=colorscheme["red"])
    window_surface.blit(points_surface, (0, 0))
    
    manager.draw_ui(window_surface)
    
    
    pygame.display.update()

