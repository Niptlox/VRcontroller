import sys
import pygame
import math
delta_angle = math.pi / 18
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
    def __init__(self, color=BLACK, bg_color=None):
        print("Brush")
        self.color = color
        self.bg_color = bg_color


class Pg(object):
    def __init__(self, surface, def_color=BLACK):
        print("PG")
        self._update = True
        self.width, self.height = surface.get_size()
        self.offset_x, self.offset_y = self.width // 2, self.height // 2
        self.scale = 1
        self.surface = surface
        self.def_color = def_color
        self.array_obj_show = []
        self.angle = 0
        self.delta_TO = 0

    def show(self):
        if self._update:
            self.surface.fill(WHITE)
            for obj in self.array_obj_show:
                obj.show()
            self._update = False

    def set_offset(self, offset_xy):
        self.offset_x, self.offset_y = offset_xy

    def get_cordinate(self, xy):
        x, y = xy
        x, y = (x * math.cos(self.angle) + y * math.sin(self.angle),
                y * math.cos(self.angle) - x * math.sin(self.angle))
        # oxy = (int(x * self.scale) + self.offset_x, int(y * self.scale) + self.offset_y)

        oxy = (int(x * self.scale) + self.offset_x, self.height-int(y * self.scale + self.offset_y))

        return oxy

    def add_obj_show(self, obj):
        self.array_obj_show.append(obj)
        self.set_update = True

    def add_offset(self, offset_x=0, offset_y=0):
        self.offset_x += offset_x
        self.offset_y += offset_y
        self._update = True

    def add_scale(self, add_scale):
        self.scale += add_scale * 0.01
        self._update = True

    def add_angle(self, add_angle):
        self.angle += add_angle
        pi2 = math.pi * 2
        if self.angle > pi2:
            self.angle -= pi2
        if self.angle < 0:
            self.angle += pi2
        self.delta_TO = int(((self.angle) * 4) // math.pi)
        self._update = True

    def set_update(self):
        self._update = True

class Point2(object):
    """docstring for ."""

    def __init__(self, xy):
        #print("Point2")
        self.x, self.y = xy

    def get_xy(self):
        return (self.x, self.y)

class Point2d(Point2):
    """docstring for ."""

    def __init__(self, pg, brush, xy):
        pg.add_obj_show(self)
        #super(Pg, ).__init__(surface=surface, color=color)
        super(Point2d, self).__init__(xy)
        #super(Brush, self).__init__(color=color)
        self.pg = pg
        self.brush = brush

    def show(self):
        pygame.draw.circle(self.pg.surface, self.brush.color, self.get_xy2d(), 2)

    def get_xy2d(self):
        return self.pg.get_cordinate((self.x, self.y))


class Point2d_text(Point2d):
    """docstring for ."""

    def __init__(self, pg, brush, xy, text="", orientation=TO_W):
        super(Point2d_text, self).__init__(pg, brush, xy)
        self.text = text
        self.orientation = TO_UNKNOWN
        #print(sys.getsizeof(self))
        self.text_surface = FONT_TEXT_POINT.render(text, True, brush.color)
        self.set_offset_text(orientation)

    def set_offset_text(self, orient):
        o_orient = orient
        orient = (orient + pg.delta_TO) % 8
        #print(self.text, orient)
        if self.orientation == orient:
            return None
        width, height = self.text_surface.get_size()
        sx, sy = width // 2, height // 2
        hw, hh = sx * 1.5 * TO_OFFSET[orient][0] - sx, sy * 1.1 * TO_OFFSET[orient][1] - sy
        self.offset_x, self.offset_y = hw, hh
        self.orientation = o_orient

        return True

    def show(self):
        #print(self.orientation)
        self.set_offset_text(self.orientation)
        #pygame.gfxdraw.pixel(self.surface, self.x, self.y, self.color)
        x, y = self.pg.get_cordinate((self.x, self.y))
        pygame.draw.circle(self.pg.surface, self.brush.color, (x, y), 2)
        self.pg.surface.blit(self.text_surface, (self.offset_x + x,
                                              self.offset_y + y))



class Figure2(object):
    def __init__(self, array_points):
        self.array_points = array_points


class Figure2d(object):
    """
    ar_inter_points # внутрение точки  - локальные
    ar_ext_points   # внешние точки
    """

    def __init__(self, pg, brush, ar_p, closed=True):
        self.pg = pg
        pg.add_obj_show(self)
        self.brush = brush
        self.closed = closed
        self.ar_points = []
        self.ar_inter_points = [] #внутрение точки  - локальные
        self.ar_ext_points = [] # внешние точки
        for point in ar_p:
            if type(point) == tuple or type(point) == list:
                self.add_inter_point2d(point)
            else:
                self.add_ext_point2d(point)

        #self.c_inter_points = len(self.ar_inter_points)
        #self.c_ext_points = len(self.ar_ext_points)
        #self.c_points = len(self.ar_points)

    def add_ext_point2d(self, point):
        self.ar_ext_points.append(point)
        self.ar_points.append(point)

    def add_inter_point2d(self, xy):
        point = Point2d(self.pg, xy, self.brush)
        self.ar_inter_points.append(point)
        self.ar_points.append(point)

    def show(self):

        old_point = None
        ar_points = [point.get_xy2d() for point in self.ar_points]
        if self.brush.bg_color != None:
            pygame.draw.polygon(self.pg.surface, self.brush.bg_color, ar_points)
        #print((self.pg.surface, self.brush.color, self.closed, ar_points, 1))
        pygame.draw.aalines(self.pg.surface, self.brush.color, self.closed, ar_points)


def create_system_cordinate(pg):
    brush = Brush(color=BLACK)
    cx_ar = []
    for x in range(-4000, 4000, 100):
        if x == 0:
            continue
        cx_ar.append(Point2d_text(pg, brush, (x, 0), text=str(x), orientation=TO_E))
    Point2d_text(pg, brush, (0, 0), text="O", orientation=TO_ES)
    cy_ar = []
    for y in range(-4000, 4000, 100):
        if y == 0:
            continue
        cy_ar.append(Point2d_text(pg, brush, (0, y), text=str(y), orientation=TO_S))
    x_system_cordinate = Figure2d(pg, brush, cx_ar, closed=False)
    y_system_cordinate = Figure2d(pg, brush, cy_ar, closed=False)


width, height = 400, 400
h_width, h_height = width // 2, height // 2
#print(sys.getsizeof(screen))
screen = pygame.display.set_mode((width, height), flags=pygame.RESIZABLE)
screen.fill(WHITE)

pg = Pg(screen)
tank = Pg(screen)
create_system_cordinate(pg)
brush = Brush(color=(10, 10, 10))

if 1:
    brush_1 = Brush(color=BLACK, bg_color=(225, 225, 0))
    A = Point2d_text(pg, brush, (-20,20), text="A", orientation=TO_N)
    B = Point2d_text(pg, brush, (50,20), text="B", orientation=TO_W)
    C = Point2d_text(pg, brush, (50,100), text="C", orientation=TO_S)
    ABC = Figure2d(pg, brush_1, [A, B, C])


pg.show()
#A.show()
#B.show()
#C.show()
#ABC.show()

pygame.display.update()
down_Ctrl = False
down_Alt = False
down_Up = False
while 1:

    pygame.time.delay(30)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: exit()
        if event.type == pygame.ACTIVEEVENT: pass
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                pg.add_offset(offset_x=-5)
            elif event.key == pygame.K_RIGHT:
                pg.add_offset(offset_x=5)
            elif event.key == pygame.K_UP:
                down_Up = True
                pg.add_offset(offset_y=-5)
            elif event.key == pygame.K_DOWN:
                pg.add_offset(offset_y=5)
            elif event.key == pygame.K_LCTRL:
                down_Ctrl = True
            elif event.key == pygame.K_LALT:
                down_Alt = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LCTRL:
                down_Ctrl = False
            elif event.key == pygame.K_LALT:
                down_Alt = False
            elif event.key == pygame.K_UP:
                down_Up = False
        if down_Ctrl:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 5:
                    pg.add_scale(1)
                if event.button == 4:
                    pg.add_scale(-1)
        elif down_Alt:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 5:
                    pg.add_angle(delta_angle)
                if event.button == 4:
                    pg.add_angle(-delta_angle)

        #print(event)

    if down_Up:
        pg.add_offset(offset_y=-5)

    print(down_Up)
    pg.show()
    pygame.display.update()
