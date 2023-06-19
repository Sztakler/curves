from Curve import Curve
import pygame
from copy import deepcopy
from utils import STATE


class Animator:
    def __init__(self, duration=2000):
        self.alpha = 0
        self.duration = duration
        self.elapsed_time = 0
        self.curve = None
        self.sourceCurve = None
        self.originalCurve = None
        self.destinationCurve = None
        self.clock = pygame.time.Clock()
        self.state = STATE.DEFAULT
        self.substitute = False

    def transformCurve(self, surface: pygame.SurfaceType, source: Curve, destination: Curve, substitute=False):
        if source is None or destination is None:
            return
        self.reset()
        self.substitute = substitute
        if self.substitute and ("bezier" in source.curveDrawer.interpolation_method) and ("bezier" in source.curveDrawer.interpolation_method):
            self.curve = source
            self.state = STATE.TRANSFORMING
        else:
            self.curve = deepcopy(source)
            self.state = STATE.ANIMATING
        self.sourceCurve = deepcopy(source)
        self.destinationCurve = deepcopy(destination)

    def reset(self):
        self.elapsed_time = 0
        self.alpha = 0
        self.destinationCurve = None
        self.sourceCurve = None
        self.curve = None
        self.state = STATE.DEFAULT
        self.substitute = False

    def draw(self, surface: pygame.SurfaceType):
        if self.curve is None:
            return
        self.curve.draw(surface=surface, draw_points=False)
        self.update()

    def animate(self):
        for i in range(len(self.curve.curveDrawer.interpolated_curve)):
            self.curve.curveDrawer.interpolated_curve[i][0] = (
                1.0 - self.alpha) * self.sourceCurve.curveDrawer.interpolated_curve[i][0] + self.alpha * self.destinationCurve.curveDrawer.interpolated_curve[i][0]
            self.curve.curveDrawer.interpolated_curve[i][1] = (
                1.0 - self.alpha) * self.sourceCurve.curveDrawer.interpolated_curve[i][1] + self.alpha * self.destinationCurve.curveDrawer.interpolated_curve[i][1]

        if self.state == STATE.TRANSFORMING:
            for i in range(len(self.curve.points)):
                self.curve.points[i].x = (
                    1.0 - self.alpha) * self.sourceCurve.points[i].x + self.alpha * self.destinationCurve.points[i].x
                self.curve.points[i].y = (
                    1.0 - self.alpha) * self.sourceCurve.points[i].y + self.alpha * self.destinationCurve.points[i].y
                self.curve.points[i].weight = (
                    1.0 - self.alpha) * self.sourceCurve.points[i].weight + self.alpha * self.destinationCurve.points[i].weight

        newColor = (
            (1 - self.alpha) *
            self.sourceCurve.color[0] + self.alpha *
            self.destinationCurve.color[0],
            (1 - self.alpha) *
            self.sourceCurve.color[1] + self.alpha *
            self.destinationCurve.color[1],
            (1 - self.alpha) *
            self.sourceCurve.color[2] + self.alpha *
            self.destinationCurve.color[2],
            255
        )
        self.curve.changeColor(newColor)

        self.alpha = min(self.elapsed_time / self.duration, 1)

        if self.elapsed_time > self.duration:
            self.reset()

    def equalizeDegrees(self):
        curveToElevate = self.curve
        curveHigher = self.destinationCurve
        if len(curveHigher.points) < len(curveToElevate.points):
            curveToElevate = self.destinationCurve
            curveHigher = self.curve

        while len(curveToElevate.points) != len(curveHigher.points):
            curveToElevate.update(curveToElevate.raiseDegree())

        if len(self.curve.points) != len(self.sourceCurve.points):
            self.sourceCurve = deepcopy(self.curve)

    def transform(self):
        if len(self.curve.points) != len(self.destinationCurve.points):
            self.equalizeDegrees()

        self.animate()

    def update(self):
        self.elapsed_time += self.clock.tick(60)
        if self.state == STATE.ANIMATING:
            self.animate()
        if self.state == STATE.TRANSFORMING:
            self.transform()
