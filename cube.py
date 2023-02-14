import pygame

class Cube(object):
    rows = 20
    w = 500

    def __init__(self, start, dirnx=1, dirny=0, color=(0, 179, 89)):
        self.pos = start
        self.dirnx = 1
        self.dirny = 0
        self.color = color

    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)

    def draw(self, surface, eyes=False):
        distance = self.w // self.rows  # distance between grid lines
        r = self.pos[0]  # current row
        c = self.pos[1]  # current column

        pygame.draw.rect(surface, self.color, (r * distance + 1, c * distance + 1, distance - 2,
                                               distance - 2))  # draw a cube that is, on each side, just one pixel width smaller than the grid, so we can still see the grid

        # Eyes drawing - small black dots only on the head
        if eyes:
            center = distance // 2  # center of our cube
            radius = 3
            middle = (r * distance + center - radius, c * distance + 8)  # center of first eye
            middle2 = (r * distance + distance - radius * 2, c * distance + 8)  # center of first eye

            pygame.draw.circle(surface, (0, 0, 0), middle, radius)
            pygame.draw.circle(surface, (0, 0, 0), middle2, radius)
