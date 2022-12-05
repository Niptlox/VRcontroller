import sys
import pygame
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

TO_UNKNOWN = -1
TO_N = 0
TO_NW = 1
TO_W = 2
TO_EW = 3
TO_E = 4
TO_ES = 5
TO_S = 6
TO_NS = 7
TO_OFFSET = [
             (0, -1),
             (1, -1),
             (1, 0),
             (1, 1),
             (0, 1),
             (-1, 1),
             (-1, 0),
             (-1, -1)
             ]

pygame.font.init()
FONT_arial = 'arial'
SIZE_TEXT_POINT = 14
FONT_TEXT_POINT = pygame.font.SysFont(FONT_arial, SIZE_TEXT_POINT)


class Brush(object):
    def __init__(self, color=BLACK):
        print("Brush")
        self.color = color


class Pg(object):
    def __init__(self, surface, def_color=BLACK):
        print("PG")
        self.surface = surface
        self.def_color = def_color

    def show(self):
        pass


class Point2(object):
    """docstring for ."""

    def __init__(self, xy):
        print("Point2")
        self.x, self.y = xy

class Point2d(Point2):
    """docstring for ."""

    def __init__(self, pg, xy, brush):
        #super(Pg, ).__init__(surface=surface, color=color)
        super(Point2d, self).__init__(xy)
        #super(Brush, self).__init__(color=color)
        self.pg = pg
        self.brush = brush

    def show(self):
        pygame.gfxdraw.pixel(self.pg.surface, self.x, self.y, self.brush.color)

class Point2d_text(Point2d):
    """docstring for ."""

    def __init__(self, pg, xy, brush, text="", orientation=TO_W):
        super(Point2d_text, self).__init__(pg, xy, brush)
        self.text = text
        self.orientation = TO_UNKNOWN
        #print(sys.getsizeof(self))
        self.text_surface = FONT_TEXT_POINT.render(text, True, brush.color)
        self.set_offset_text(orientation)

    def set_offset_text(self, orient):
        if self.orientation == orient:
            return None
        width, height = self.text_surface.get_size()
        hw, hh = width // 2 * TO_OFFSET[orient][0], height // 2 * TO_OFFSET[orient][1]
        self.offset_x, self.offset_y = hw, hh

        return True

    def show(self):
        #pygame.gfxdraw.pixel(self.surface, self.x, self.y, self.color)
        pygame.draw.circle(self.pg.surface, self.brush.color, (self.x, self.y), 2)
        self.pg.surface.blit(self.text_surface, (self.offset_x + self.x,
                                              self.offset_y + self.y))


class Figure2(object):
    def __init__(self, array_points):
        self.array_points = array_points


class Figure2d(Pg, Figure2, Brush):
    """docstring for ."""

    def __init__(self, surface, ar_p, color=BLACK):
        super(Figure2d, self).__init__(array_points=ar_p, surface=surface, color=color)
        #super(pg).__init__(surface)

    def show(self):
        pygame.gfxdraw.pixel(self.surface, self.x, self.y, self.color)


width, height = 310, 400
screen = pygame.display.set_mode((width, height), flags=pygame.RESIZABLE)
#print(sys.getsizeof(screen))
screen.fill(WHITE)

pg = Pg(screen)

brush = Brush(color=BLACK)

A = Point2d_text(pg, (1,1), brush, text="A")
B = Point2d_text(pg, (50,20), brush, text="B")
A.show()
B.show()
pygame.display.update()
while 1: pass
"""
p = Point2d(screen, (1,2))
f = Figure2(array_points=[
        Point2(xy=(0, 0)) ,
        Point2(xy=(0, 10)) ,
        Point2(xy=(10, 10)) ,
        Point2(xy=(10, 0)) ])
g = p
del g
print(p)


while 1:
    i ^= 1
    pygame.time.delay(30)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: exit()
        if event.type == pygame.ACTIVEEVENT: pass
        print(event)

    mx, my = pygame.mouse.get_pos()
    pressed = pygame.mouse.get_pressed()
    #screen.fill(BLACK)



    if pressed[0]:
        #pygame.display.toggle_fullscreen()
        #screen = pygame.display.set_mode((width, height), flags=pygame.RESIZABLE)
        #screen.blit(surf,(10,10))
        #surf.fill(RED)
        pass
    if pressed[2]:
        #screen = pygame.display.set_mode((width, height), flags=pygame.FULLSCREEN)
        pass#    surf.blit(surf2,(10,10))


    #print(mx, my, pressed)
    pygame.display.update()
"""
