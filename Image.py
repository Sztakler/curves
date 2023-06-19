import pygame


class Image:
    def __init__(self, path=None, position=[0, 0], visible=True):
        self.path = path
        self.visible = visible
        self.image = None
        self.position = position

    def draw(self, surface):
        if not self.visible or self.image is None:
            return

        surface.blit(self.image, self.position)

    def toggle(self):
        self.visible = not self.visible

    def load(self, path):
        self.path = path
        self.image = pygame.image.load(self.path)
        self.image.set_alpha(255)

    def drag(self):
        if self.image is None:
            return

        mouse_position = pygame.mouse.get_pos()
        offset = [mouse_position[0] - self.position[0],
                  mouse_position[1] - self.position[1]]
        self.move(offset)

    def move(self, offset):
        self.position[0] += offset[0]
        self.position[1] += offset[1]

    def collidepoint(self, point):
        if self.image is None:
            return False
        rect = self.image.get_rect()
        return point[0] > self.position[0] and point[0] < self.position[0] + rect.width and point[1] > self.position[1] and point[1] < self.position[1] + rect.height
