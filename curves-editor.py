from copy import deepcopy
from math import *
import sys
from random import randint

import pygame
import pygame_gui

from Curve import Curve
from Point import Point
from Image import Image
from InputManager import InputManager


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
            "selected": self.hex_to_rgb("#d65d0e"),
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
                pygame_gui.elements.UIButton(relative_rect=pygame.Rect(
                    5, 5, 100, 30), text="Colour", manager=None, anchors={'top': 'top', 'left': 'left'}),
                pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect(
                    110, 5, 300, 30), manager=None, anchors={'top': 'top', 'left': 'left'}),
                pygame_gui.elements.UIButton(relative_rect=pygame.Rect(
                    415, 5, 100, 30), text="Clear", manager=None, anchors={'top': 'top', 'left': 'left'}),
                pygame_gui.elements.UIButton(relative_rect=pygame.Rect(520,5,100,30), text="Load", manager=None, anchors={'top': 'top', 'left': 'left'}),
                pygame_gui.elements.UIButton(relative_rect=pygame.Rect(
                    625, 5, 100, 30), text="MoveRight", manager=None, anchors={'top': 'top', 'left': 'left'}),
                pygame_gui.elements.UIButton(relative_rect=pygame.Rect(
                    730, 5, 100, 30), text="MoveUp", manager=None, anchors={'top': 'top', 'left': 'left'}),
                pygame_gui.elements.UIButton(relative_rect=pygame.Rect(
                    835, 5, 100, 30), text="MoveDown", manager=None, anchors={'top': 'top', 'left': 'left'}),
                pygame_gui.elements.UIButton(relative_rect=pygame.Rect(
                    940, 5, 150, 30), text="Toggle Image", manager=None, anchors={'top': 'top', 'left': 'left'}),
                pygame_gui.elements.UIDropDownMenu(relative_rect=pygame.Rect(1100, 5, 200, 30), options_list=[
                                                   "Lagrange", "Spline", "Bezier", "Rational Bezier", "BSpline"], starting_option="Bezier", manager=None, anchors={'top': 'top', 'left': 'left'}),
                pygame_gui.windows.UIColourPickerDialog(
                    rect=pygame.Rect(5, 5, 200, 200), visible=0),
                pygame_gui.windows.UIFileDialog(rect=pygame.Rect(
                    5, 5, 200, 200), manager=None, visible=0),
            ],
            margin=5,
            padding=5,
            height=30)
        self.menu.set_layout()
        self.menu.elements[9].on_close_window_button_pressed = lambda: self.menu.elements[9].hide(
        )
        self.menu.elements[9].kill = lambda: self.menu.elements[9].hide()
        self.menu.elements[10].kill = lambda: self.menu.elements[10].hide()

        self.background_image_path = None
        if (len(sys.argv) > 1):
            self.background_image_path = sys.argv[1]

        self.background_image = None
        if self.background_image_path != None:
            self.background_image = pygame.image.load(
                self.background_image_path)

        self.is_background_image_rendered = True
        self.isConvexHullRendered = False
        self.is_dragging = False
        self.move_curve = False
        self.moving = False
        self.direction = "left"
        self.rotation = False
        self.rotation_direction = "clockwise"
        self.pivot = None
        self.curves = []
        self.selected_curve: Curve | None = None
        self.block_mouse = False
        self.block_keyboard = False
        self.configFilePath = "./input-config.json"
        self.inputManager = InputManager(self.configFilePath)
        self.image = Image()
        self.move_image = False

    def hex_to_rgb(self, value):
        value = value.lstrip('#')
        lv = len(value)
        return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

    def process_input(self, input):
        color = input
        return color
        # x_fun = sin
        # y_fun = cos
        # t_range = [0, pi, 1000]
        # t = 0

        # parts = input.split(';')

        # n_args = len(parts)
        # if n_args >= 1 and parts[0] != "":
        #     x_fun = eval(parts[0])
        # if n_args >= 2:
        #     y_fun = eval(parts[1])
        # if n_args >= 3:
        #     t_args = eval(parts[2])
        #     t_args_length = len(t_args)
        #     if t_args_length >= 1:
        #         t_range[0] = t_args[0]
        #     if t_args_length >= 2:
        #         t_range[1] = t_args[1]
        #     if t_args_length >= 3:
        #         t_range[2] = t_args[2]

        # t_start = t_range[0]
        # t_stop  = t_range[1]
        # t_step  = t_range[2]

        # ts = numpy.linspace(t_start, t_stop, t_step)

        # points = []
        # size = 100.0
        # for t in ts:
        #     point = Point(x_fun(t) * size + 200, y_fun(t) * size + 200)
        #     points.append(point)

        # return points

    def update(self, mouse_position=None):
        if mouse_position != None:
            point = Point(mouse_position[0], mouse_position[1])
            if point.y < self.menu.height:
                return

            if self.selected_curve != None:
                self.selected_curve.append(point)

        if self.selected_curve != None:
            self.selected_curve.update(self.selected_curve.points)

    def render(self):
        if len(self.points) >= 2:
            parametric_curve = pygame.Surface(self.window_size)
            pygame.draw.aalines(parametric_curve, 'white',
                                closed=False, points=self.points)
            self.window_surface.blit(parametric_curve, (0, 0))

        self.window_surface.fill(self.colorscheme["bg"])
        # if self.background_image != None and self.is_background_image_rendered == True:
        #     self.window_surface.blit(self.background_image, (200, 200))

        self.image.draw(surface=self.window_surface)

        for curve in self.curves:
            curve.draw(surface=self.window_surface, draw_points=True)

        self.menu.manager.draw_ui(self.window_surface)

        pygame.display.update()

    def move_points(self, direction):
        if len(self.selected_curve.points) < 1:
            return

        if direction == "left":
            for point in self.selected_curve.points:
                point.x -= 10
        if direction == "right":
            for point in self.selected_curve.points:
                point.x += 10
        if direction == "up":
            for point in self.selected_curve.points:
                point.y -= 10
        if direction == "down":
            for point in self.selected_curve.points:
                point.y += 10
        self.update()

    def toggle_background_image(self):
        self.is_background_image_rendered = not self.is_background_image_rendered

    def get_point_under_cursor_index(self):
        if self.selected_curve == None:
            return None
        mouse_position = pygame.mouse.get_pos()
        size = [10, 10]
        collider = pygame.Rect(
            mouse_position[0] - size[0]/2, mouse_position[1] - size[1]/2, size[0], size[1])
        pygame.draw.rect(self.window_surface,
                         self.colorscheme["red"], collider)
        collider_surface = pygame.Surface(self.window_size)
        pygame.draw.rect(collider_surface, 'red', collider)
        self.window_surface.blit(collider_surface, mouse_position)
        for point in self.selected_curve.points:
            if collider.collidepoint(point.x, point.y):
                return self.selected_curve.points.index(point)
        return None

    def get_point_under_cursor(self, curve=None):
        mouse_position = pygame.mouse.get_pos()
        size = [10, 10]
        collider = pygame.Rect(
            mouse_position[0] - size[0]/2, mouse_position[1] - size[1]/2, size[0], size[1])
        pygame.draw.rect(self.window_surface,
                         self.colorscheme["red"], collider)
        collider_surface = pygame.Surface(self.window_size)
        pygame.draw.rect(collider_surface, 'red', collider)
        self.window_surface.blit(collider_surface, mouse_position)

        if curve == None:
            for curve in self.curves:
                for point in curve.points:
                    if collider.collidepoint(point.x, point.y):
                        return point
        else:
            for point in self.selected_curve.points:
                if collider.collidepoint(point.x, point.y):
                    return point
        return None

    def select_curve_under_cursor(self):
        mouse_position = pygame.mouse.get_pos()
        epsilon = 10
        for curve in self.curves:
            point = self.get_point_under_cursor()
            if curve.check_if_lies_on(mouse_position, epsilon) or point in curve.points:
                return curve

    def remove_point(self, point):
        if point != None:
            self.rotation_direction = "clockwise"
            self.selected_curve.remove(point)

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
        self.selected_curve.convexHull.toggleRendering()

    def clear(self):
        self.user_points = []
        if self.selected_curve is not None:
            self.selected_curve.clear()
        self.update()

    def get_chebyshev_nodes(self, points):
        n = len(points)
        result = []
        for k in range(n + 1)[1:]:
            result.append(
                cos(((2*k - 1) / (2*n)) * pi))
        return result

    def copySelectedCurve(self):
        newCurve = deepcopy(self.selected_curve)
        self.curves.append(newCurve)
        self.selectCurve(newCurve)

    def selectCurve(self, curve):
        if curve == None:
            return

        if self.selected_curve != None:
            self.selected_curve.deselect()
        self.selected_curve = curve
        self.user_points = self.selected_curve.points
        self.selected_curve.update(self.selected_curve.points)
        self.selected_curve.select(self.colorscheme["selected"])

    def addCurve(self, points):
        self.user_points = []
        color = (randint(0, 255), randint(0, 255), randint(0, 255), 255)
        method = "-".join(
            self.menu.elements[8].selected_option.split(" ")).lower()

        curve = Curve(points, color, method)
        if method == "lagrange":
            curve = Curve(points, color, method, self.get_chebyshev_nodes)

        self.curves.append(curve)
        self.selectCurve(curve)

    def watchInputBlocks(self):
        self.block_mouse = False
        self.block_keyboard = False
        if self.menu.elements[8].current_state == self.menu.elements[8].menu_states['expanded']:
            self.block_mouse = True
        if self.menu.elements[9]._get_visible() or self.menu.elements[10]._get_visible():
            self.block_mouse = True
            self.block_keyboard = True

    def start(self):
        MODSHIFT = False
        SELECTING_CURVE = False
        while self.is_running:
            self.block_mouse = False
            self.block_keyboard = False
            self.watchInputBlocks()
            time_delta = self.clock.tick(60)/1000.0
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and self.block_keyboard != True:
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
                    if event.key == pygame.K_n:
                        self.addCurve([])
                    if event.key == pygame.K_e:
                        if self.selected_curve is None:
                            continue
                        newCurvesPoints = self.selected_curve.raiseDegree()
                        if newCurvesPoints == None:
                            continue
                        self.selected_curve.update(newCurvesPoints)
                    if event.key == pygame.K_l:
                        if self.selected_curve is None:
                            continue
                        newCurvesPoints = self.selected_curve.lowerDegree()
                        if newCurvesPoints != None:
                            self.selected_curve.update(newCurvesPoints)
                    if event.key == pygame.K_j:
                        SELECTING_CURVE = True
                    if event.key == pygame.K_i:
                        if self.selected_curve is None:
                                continue
                        if MODSHIFT:
                            self.selected_curve.modifyPointThickness(-1)
                        else:
                            self.selected_curve.modifyPointThickness(1)
                    if event.key == pygame.K_s:
                        if self.selected_curve is None:
                                continue
                        newCurvesPoints = self.selected_curve.split(0.5)
                        if newCurvesPoints == None:
                            continue
                        self.curves.remove(self.selected_curve)
                        self.addCurve(newCurvesPoints[0])
                        self.addCurve(newCurvesPoints[1])
                    if event.key == pygame.K_c:
                        self.copySelectedCurve()
                    if event.key == pygame.K_q:
                        self.clear()

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
                        self.menu.elements[9].show()
                    if event.ui_element == self.menu.elements[2]:
                        self.clear()
                    if event.ui_element == self.menu.elements[3]:
                        # self.move_points("left")
                        self.menu.elements[10].show()
                    if event.ui_element == self.menu.elements[4]:
                        self.move_points("right")
                    if event.ui_element == self.menu.elements[5]:
                        self.move_points("up")
                    if event.ui_element == self.menu.elements[6]:
                        self.move_points("down")
                    if event.ui_element == self.menu.elements[7]:
                        self.image.toggle()
                if event.type == pygame_gui.UI_COLOUR_PICKER_COLOUR_PICKED:
                    if self.selected_curve is not None:
                        self.selected_curve.changeColor(event.colour)
                if event.type == pygame_gui.UI_FILE_DIALOG_PATH_PICKED:
                    self.image.load(event.text)
                if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED:
                    if event.ui_element == self.menu.elements[1]:
                        print(self.process_input(
                            self.menu.elements[1].get_text()))
                self.menu.manager.process_events(event)

                if event.type == pygame.MOUSEWHEEL and not self.block_mouse:
                    if self.selected_curve is None:
                                continue
                    weightDelta = event.y
                    pointIndex = self.get_point_under_cursor_index()
                    if pointIndex:
                        if MODSHIFT:
                            self.selected_curve.changeSelectedPointWeight(
                                weightDelta, pointIndex)
                        else:
                            self.selected_curve.modifyPointThickness(event.y)
                    else:
                        self.selected_curve.modifyLineThickness(event.y)

                if event.type == pygame.MOUSEBUTTONDOWN and self.block_mouse == False:
                    if event.button == 2:
                        self.is_dragging = True
                        self.index = self.get_point_under_cursor_index()
                        image_collision = self.image.collidepoint(pygame.mouse.get_pos())
                        if MODSHIFT:
                            if self.index is not None:
                                self.move_curve = True
                            elif image_collision:
                                self.move_image = True
                    if event.button == 1:
                        if SELECTING_CURVE:
                            if self.selected_curve is None:
                                continue
                            other_curve = self.select_curve_under_cursor()
                            newCurvesPoints = self.selected_curve.join(
                                other_curve)
                            self.selected_curve.update(newCurvesPoints)
                            other_curve.update([])
                            SELECTING_CURVE = False
                        elif MODSHIFT:
                            self.selectCurve(self.select_curve_under_cursor())
                        else:
                            self.update(pygame.mouse.get_pos())
                    if event.button == 3:
                        if MODSHIFT:
                            # add new point
                            pass
                        else:
                            self.remove_point(self.get_point_under_cursor())
                            self.update()
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 2:
                        self.is_dragging = False
                        self.move_curve = False
                        self.move_image = False
                if event.type == pygame.MOUSEMOTION:
                    if self.is_dragging and self.move_image:
                        self.image.drag()
                        self.render()

            self.menu.manager.update(time_delta)

            if self.moving:
                self.move_points(self.direction)

            if self.is_dragging:
                # if self.move_image:
                #     self.image.drag()

                if self.selected_curve is None:
                    continue

                if self.index != None:
                    mouse_position = pygame.mouse.get_pos()
                    point = Point(mouse_position[0], mouse_position[1])
                    selectedPoint = self.selected_curve.points[self.index]
                    if self.move_curve == True:
                        offset = [mouse_position[0] - selectedPoint.x,
                                  mouse_position[1] - selectedPoint.y]
                        self.selected_curve.move_curve(offset)
                    else:
                        self.selected_curve.points[self.index] = point

                if len(self.selected_curve.points) >= 2:
                    self.update()

            if self.rotation:
                for point in self.selected_curve.points:
                    self.rotate_point(self.pivot, point,
                                      self.rotation_direction)
                self.update()
            self.render()


curvesEditor = CurvesEditor()
curvesEditor.start()
