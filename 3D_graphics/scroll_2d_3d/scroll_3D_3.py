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

Rotation_0 = 0
Rotation_X = 1
Rotation_Y = 2
Rotation_Z = 3

def mul_matrix(a, b, c=None):
    s = 3
    if c == None:
        c = [[0]*s for i in range(3)]
    for i in range(s):
        for j in range(s):
            c[i][j] = a[i][0] * b[0][j] + a[i][1] * b[1][j] + a[i][2] * b[2][j]
    return c

def crt_rotation_matrix(angle, rot_axis, c=None):
    s = 3
    if c == None:
        c = [[0]*s for i in range(3)]
    else:
        for i in range(s):
            for j in range(s):
                c[i][j] = 0
    c[0][0] = c[1][1] = c[2][2] = 1
    if rot_axis == Rotation_0:
        return c
    cos_a = math.cos(angle)
    sin_a = math.sin(angle)
    if rot_axis == Rotation_X:
        c[1][1] = cos_a
        c[1][2] = sin_a
        c[2][1] = -sin_a
        c[2][2] = cos_a
    elif rot_axis == Rotation_Y:
        c[0][0] = cos_a
        c[0][2] = sin_a
        c[2][0] = -sin_a
        c[2][2] = cos_a
    elif rot_axis == Rotation_Z:
        c[0][0] = cos_a
        c[0][1] = sin_a
        c[1][0] = -sin_a
        c[1][1] = cos_a
    return c

def mul_vector_matrix(a, b, c=None):
    s = 3
    if c == None:
        c = [0]*s
    for j in range(s):
        c[j] = a[0] * b[0][j] + a[1] * b[1][j] + a[2] * b[2][j]
    return c

def scalar_mul_vectors(a, b):
    c = a[0] * b[0] + a[1] * b[1] + a[2] * b[2]
    return c

def sub_vectors(a, b, c=None):
    s = 3
    if c == None:
        c = [0]*s
    for j in range(s):
        c[j] = a[j] - b[j]
    return c

def sum_vectors(a, b, c=None):
    s = 3
    if c == None:
        c = [0]*s
    for j in range(s):
        c[j] = a[j] + b[j]
    return c




class Brush(object):
    def __init__(self, color=BLACK, bg_color=None):
        #print("Brush")
        self.color = color
        self.bg_color = bg_color


class Pg(object):
    def __init__(self, surface, def_color=BLACK):
        #print("PG")
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

    def get_cordinate(self, xy, add_offset=True):
        x, y = xy
        x, y = (x * math.cos(self.angle) + y * math.sin(self.angle),
                y * math.cos(self.angle) - x * math.sin(self.angle))
        # oxy = (int(x * self.scale) + self.offset_x, int(y * self.scale) + self.offset_y)
        if add_offset:
            oxy = (int(x * self.scale) + self.offset_x, self.height-int(y * self.scale + self.offset_y))
        else:
            oxy = (int(x * self.scale), int(y * self.scale))
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


class Point3(object):
    """docstring for ."""

    def __init__(self, xyz):
        #print("Point2")
        self.x, self.y, self.z = xyz

    def get_xyz(self):
        return (self.x, self.y, self.z)


class Pg3d(object):
    def __init__(self, surface, focus):
        self.surface = surface
        self._update = True
        self.width, self.height = surface.get_size()
        self.offset_x, self.offset_y = self.width // 2, self.height // 2
        self.focus = focus
        self.array_obj_show = []

    def add_obj_show(self, obj, xyz=(0,0,0)):
        self_3d = self
        gc = obj.get_cordinate
        obj.get_cordinate = lambda xy, z=0: self_3d.get_cordinate_3d(gc(xy, add_offset=False), obj, z)
        r_matrix = crt_rotation_matrix(0, Rotation_0)
        obj.struct_3d = {"O": xyz, "rm": r_matrix}
        self.array_obj_show.append(obj)
        self._update = True

    def get_cordinate_3d(self, xy, pg, z=0):
        #print("3d", self, pg)
        r_matrix = pg.struct_3d["rm"]
        o_xyz = pg.struct_3d["O"]
        x, y = xy
        v_xyz = sum_vectors(mul_vector_matrix((x, y, z), r_matrix), o_xyz)
        x, y, z = v_xyz
        K =  self.focus / (self.focus + z)
        return (int(x * K)+self.offset_x, int(y * K)+self.offset_x)

    def show(self):
        for obj in self.array_obj_show:
            obj.show()

    def add_angle(self, angle, rot_axis):
        r_m = crt_rotation_matrix(angle, rot_axis)
        #print(self.array_obj_show[0])
        or_m = self.array_obj_show[0].struct_3d["rm"]
        m = mul_matrix(r_m, or_m)
        self.array_obj_show[0].struct_3d["rm"] = m
        self.array_obj_show[0]._update = True
        self._update = True

    def add_offset(self, offset_x=0, offset_y=0):
        self.offset_x += offset_x
        self.offset_y += offset_y
        self._update = True
        for obj in self.array_obj_show:
            obj._update = True

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

class Point3d(Point2d):
    def __init__(self, pg, brush, xy, z):
        self.z = z
        super(Point3d, self).__init__(pg, brush, xy)

    def get_xy2d(self):
        return self.pg.get_cordinate((self.x, self.y), z=self.z)


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

def create_grid(pg, width, height, step=1):
    step = step
    wp, hp = width // step, height // step
    brush = Brush(color=BLACK)
    ar = [[None] * wp for i in range(hp)]
    bx, by = -width // 2, -height // 2

    for y in range(hp):
        nx = bx
        for x in range(wp):
            r = (nx * nx + by * by) / (width ** 2) * math.pi * 5
            z = 30 * math.cos(r)
            print(r,(nx * nx + by * by), (nx , by))
            point = Point3d(pg, brush, (nx, by), z)
            nx += step
            ar[y][x] = point
        by += step
        #print(ar[y])
        Figure2d(pg, brush, ar[y], closed=False)
    for x in range(wp):
        vert_ar = [ar[y][x] for y in range(hp)]
        #print(None in vert_ar)
        Figure2d(pg, brush, vert_ar, closed=False)



def create_system_cordinate(pg):
    brush = Brush(color=BLACK)
    cx_ar = []
    len_xy = 150
    sep = 100
    for x in range(-len_xy, len_xy + 1, sep):
        if x == 0:
            continue
        cx_ar.append(Point2d_text(pg, brush, (x, 0), text=str(x), orientation=TO_E))
    cx_ar.append(Point2d_text(pg, brush, (x, 0), text="X", orientation=TO_W))
    Point2d_text(pg, brush, (0, 0), text="O", orientation=TO_ES)
    cy_ar = []
    for y in range(-len_xy, len_xy + 1, sep):
        if y == 0:
            continue
        cy_ar.append(Point2d_text(pg, brush, (0, y), text=str(y), orientation=TO_S))
    cy_ar.append(Point2d_text(pg, brush, (0, y), text="Y", orientation=TO_N))
    x_system_cordinate = Figure2d(pg, brush, cx_ar, closed=False)
    y_system_cordinate = Figure2d(pg, brush, cy_ar, closed=False)


width, height = 400, 400
h_width, h_height = width // 2, height // 2
#print(sys.getsizeof(screen))
screen = pygame.display.set_mode((width, height), flags=pygame.RESIZABLE)
screen.fill(WHITE)

pg = Pg(screen)
tank = Pg(screen)
#create_system_cordinate(pg)
create_grid(pg, 300, 300, step=5)
brush = Brush(color=(10, 10, 10))

if 0:
    brush_1 = Brush(color=BLACK, bg_color=(225, 225, 0))
    A = Point2d_text(pg, brush, (-20,20), text="A", orientation=TO_N)
    B = Point2d_text(pg, brush, (50,20), text="B", orientation=TO_W)
    C = Point2d_text(pg, brush, (50,100), text="C", orientation=TO_S)
    ABC = Figure2d(pg, brush_1, [A, B, C])


#pg.show()

pg_3d = Pg3d(screen, 250)
pg_3d.add_obj_show(pg, xyz=(0,0,50))
pg_3d.show()
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
            if down_Ctrl:
                if event.key == pygame.K_LEFT:
                    pg_3d.add_angle(delta_angle, Rotation_Y)
                elif event.key == pygame.K_RIGHT:
                    pg_3d.add_angle(-delta_angle, Rotation_Y)
                elif event.key == pygame.K_UP:
                    pg_3d.add_angle(delta_angle, Rotation_X)
                elif event.key == pygame.K_DOWN:
                    pg_3d.add_angle(-delta_angle, Rotation_X)
            else:
                if event.key == pygame.K_LEFT:
                    pg_3d.add_offset(offset_x=-5)
                elif event.key == pygame.K_RIGHT:
                    pg_3d.add_offset(offset_x=5)
                elif event.key == pygame.K_UP:
                    down_Up = True
                    pg_3d.add_offset(offset_y=-5)
                elif event.key == pygame.K_DOWN:
                    pg_3d.add_offset(offset_y=5)
            if event.key == pygame.K_LCTRL:
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

    #print(down_Up)
    pg_3d.show()
    pygame.display.update()
