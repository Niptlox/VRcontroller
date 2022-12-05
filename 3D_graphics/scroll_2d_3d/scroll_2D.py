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
    def __init__(self, **args):
        print("Brush")
        print(args)
        self.color = args["color"]
        print(1, self.color)

class Pg(object):
    def __init__(self, **args):
        print("PG")
        print(args)
        self.surface = args["surface"]
        self.def_color = args.get('color', BLACK)

    def show(self):
        pass
#endClass

class Point2(object):
    """docstring for ."""

    def __init__(self, **args):
        print("Point2")
        print(args)
        self.x, self.y = args["xy"]

class Point2d(Brush, Point2, Pg):
    """docstring for ."""

    def __init__(self, surface, xy, color=BLACK):
        print(color)
        #super(Brush, self).__init__(xy=xy, surface=surface, color=color)
        super(Pg, ).__init__(surface=surface, color=color)
        super(Point2, self).__init__(xy=xy)
        super(Brush, self).__init__(color=color)
        print("SUPER")
        print(self.color)
        #super(pg).__init__(surface)

    def show(self):
        pygame.gfxdraw.pixel(self.surface, self.x, self.y, self.color)

class Point2d_text(Point2d):
    """docstring for ."""

    def __init__(self, surface, xy, color=BLACK, text="", orientation=TO_W):
        super(Point2d_text, self).__init__(xy=xy, surface=surface, color=color)
        self.text = text
        self.orientation = TO_UNKNOWN
        #print(sys.getsizeof(self))
        self.text_surface = FONT_TEXT_POINT.render(text, True, color)
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
        pygame.draw.circle(self.surface, self.color, (self.x, self.y), 2)
        self.surface.blit(self.text_surface, (self.offset_x + self.x,
                                              self.offset_y + self.y))


class Figure2(object):
    def __init__(self, **args):
        self.array_points = args["array_points"]


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

A = Point2d_text(screen, (1,1), text="A")
B = Point2d_text(screen, (50,20), text="B")
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
