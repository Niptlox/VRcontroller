import sys
import pygame
import math
delta_angle = math.pi / 18
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

DEFAULT_COLOR_POINT = BLACK

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


PHASE_OBJECT = 1
PHASE_MAP = 2
PHASE_CAMERA = 3
PHASE_SCREEN = 4

tact_3d = 0
phase_3d = 0
camera_3d = 0
count_camera = 1


POINT_FLAG_MAP = 1
POINT_FLAG_NORMAL = 2
OBJECT_FLAG_MAP = 1
OBJECT_FLAG_STATIC = 2
OBJECT_FLAG_MOVING = 4
OBJECT_FLAG_DEPENDENT = 8
POLGON_FLAG_HAVENT_NORMAL = 0
POLGON_FLAG_HAVE_NORMAL = 1
POLGON_FLAG_COMMON_NORMAL = 2
# FLAG & NAME_FLAG


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


def vector_mul_vector(a, b, c=None):
    s = 3
    if c == None:
        c = [0] * 3
    a1, a2, a3 = a
    b1, b2, b3 = b
    #i = [(a2 * b3 - b2 * a3), 0, 0]
    #j = [0, (a1 * b3 - b1 * a3), 0]
    #k = [0, 0, (a1 * b2 - b1 * a2)]
    c[:] = [(a2 * b3 - b2 * a3), -(a1 * b3 - b1 * a3), (a1 * b2 - b1 * a2)]
    return c


class Brush(object):
    def __init__(self, color=BLACK, bg_color=None):
        # print("Brush")
        self.color = color
        self.bg_color = bg_color


class Pg(object):
    def __init__(self, surface, def_color=BLACK):
        # print("PG")
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
            oxy = (int(x * self.scale) + self.offset_x,
                   self.height-int(y * self.scale + self.offset_y))
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


class Pg3d(object):
    def __init__(self, surface, focus):
        self.surface = surface
        self._update = True
        self.width, self.height = surface.get_size()
        self.offset_x, self.offset_y = self.width // 2, self.height // 2
        self.focus = focus
        self.array_obj_show = []

    def add_obj_show(self, obj, xyz=(0, 0, 0)):
        self_3d = self
        gc = obj.get_cordinate
        obj.get_cordinate = lambda xy, z=0: self_3d.get_cordinate_3d(
            gc(xy, add_offset=False), obj, z)
        r_matrix = crt_rotation_matrix(0, Rotation_0)
        obj.struct_3d = {"O": xyz, "rm": r_matrix}
        self.array_obj_show.append(obj)
        self._update = True

    def get_cordinate_3d(self, xy, pg, z=0):
        #print("3d", self, pg)
        r_matrix = pg.struct_3d["rm"]
        o_xyz = pg.struct_3d["O"]
        x, y = xy
        z *= pg.scale
        v_xyz = sum_vectors(mul_vector_matrix((x, y, z), r_matrix), o_xyz)
        x, y, z = v_xyz
        K = self.focus / (self.focus + z)
        x, y = (int(x * K)+self.offset_x, int(y * K)+self.offset_x)
        if 0 <= x <= self.width and 0 <= y <= self.height:
            return (x, y)
        return None

    def show(self):
        for obj in self.array_obj_show:
            obj.show()

    def add_angle(self, angle, rot_axis):
        r_m = crt_rotation_matrix(angle, rot_axis)
        # print(self.array_obj_show[0])
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
        # print("Point2")
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
        xy = self.get_xy2d()
        if xy != None:
            pygame.draw.circle(self.pg.surface, self.brush.color, xy, 2)

    def get_xy2d(self):
        return self.pg.get_cordinate((self.x, self.y))


class Point2d_text(Point2d):
    """docstring for ."""

    def __init__(self, pg, brush, xy, text="", orientation=TO_W):
        super(Point2d_text, self).__init__(pg, brush, xy)
        self.text = text
        self.orientation = TO_UNKNOWN
        # print(sys.getsizeof(self))
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
        # print(self.orientation)
        self.set_offset_text(self.orientation)
        #pygame.gfxdraw.pixel(self.surface, self.x, self.y, self.color)
        xy = self.pg.get_cordinate((self.x, self.y))
        if xy != None:
            x, y = xy
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
        self.ar_inter_points = []  # внутрение точки  - локальные
        self.ar_ext_points = []  # внешние точки
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
        ar_points = list(filter(lambda xy: xy != None, ar_points))
        if len(ar_points) >= 2:
            if self.brush.bg_color != None:
                pygame.draw.polygon(self.pg.surface, self.brush.bg_color, ar_points)
            #print((self.pg.surface, self.brush.color, self.closed, ar_points, 1))
            pygame.draw.aalines(self.pg.surface, self.brush.color, self.closed, ar_points)


class Point3d_screen(object):
    def __init__(self, flag, xy, color=DEFAULT_COLOR_POINT, radius=2):
        self.x, self.y = xy
        self.flag = flag
        self.color = color
        self.radius = radius

    def show(self, surface):
        pygame.draw.circle(surface, self.color, (self.x, self.y), self.radius)


class Point3d_static(object):
    def __init__(self, FLAG, xyz):
        self.xyz = xyz
        self.tact = TACT_RESTART
        self.FLAG = FLAG
        #self.FLAG = owner.ismap()

    def calc(self, phase):
        if tact < self.tact:
            pass

        if phase == 0:
            pass
        elif phase == 1:
            pass

    def get_map_xyz(self):

        return xyz

    def get_screen_xy(self):

        r_matrix = pg.struct_3d["rm"]
        o_xyz = pg.struct_3d["O"]
        x, y = xy
        z *= pg.scale
        v_xyz = sum_vectors(mul_vector_matrix((x, y, z), r_matrix), o_xyz)
        x, y, z = v_xyz
        K = self.focus / (self.focus + z)
        x, y = (int(x * K)+self.offset_x, int(y * K)+self.offset_x)
        if 0 <= x <= self.width and 0 <= y <= self.height:
            return (x, y)
        return None


class Point3d(object):
    def __init__(self, owner, FLAG, xyz):
        self.xyz = xyz
        self.owner = owner
        self.tact = TACT_RESTART
        self.FLAG = FLAG
        #self.FLAG = owner.ismap()

    def calc(self, phase):
        if tact < self.tact:
            pass

        if phase == 0:
            pass
        elif phase == 1:
            pass

    def get_map_xyz(self):

        return xyz

    def get_screen_xy(self):

        r_matrix = pg.struct_3d["rm"]
        o_xyz = pg.struct_3d["O"]
        x, y = xy
        z *= pg.scale
        v_xyz = sum_vectors(mul_vector_matrix((x, y, z), r_matrix), o_xyz)
        x, y, z = v_xyz
        K = self.focus / (self.focus + z)
        x, y = (int(x * K)+self.offset_x, int(y * K)+self.offset_x)
        if 0 <= x <= self.width and 0 <= y <= self.height:
            return (x, y)
        return None


class Polygon(object):
    def __init__(self, array_points=[], FLAG=POLGON_FLAG_HAVENT_NORMAL, normal=None):
        self.FLAG = FLAG
        self.array_points = array_points
        if normal != None:
            self.normal = normal
        else:
            if FLAG == POLGON_FLAG_HAVE_NORMAL:
                self.normal = create_normal

    def create_normal(self):
        v1 = sub_vectors(self.array_points[1].xyz, self.array_points[0].xyz)
        v2 = sub_vectors(self.array_points[1].xyz, self.array_points[2].xyz)
        v3 = vector_mul_vector(v1, v2)
        normal = Point3d(self.array_points[1].owner, POINT_FLAG_NORMAL, v3)
        return normal


class Surface3d(object):
    def __init__(self, owner, array_polygons=[]):
        self.owner = owner
        self.array_polygons = array_polygons
        self.tact = TACT_RESTART


class Surface3d_monocolor(Surface3d):
    def __init__(self, owner, array_polygons=[], rgb=WHITE, alpha=255):
        super(Surface3d_monocolor, self).__init__(owner, array_polygons)
        self.rgb = rgb
        self.alpha = alpha


class Flat_surface3d(Surface3d):
    def __init__(self, owner, array_polygons=[], normal=None):
        super(Flat_surface3d, self).__init__(owner, array_polygons)
        if normal == None:
            normal = array_polygons[0].create_normal()
        self.normal = normal

    def is_show(self):
        # point =
        return


class Object3d(object):
    def __init__(self, xyz, array_points=[], array_surface3d=[]):
        self.xyz = xyz
        self.array_points = array_points
        self.array_ext_points = []
        self.array_surface3d = array_surface3d
        # TODO: разобрать точки на внешние и внутрение
        # TODO: Сделать колайдер для определения поподает ли на экран ввиде Surface

    def add_point(self, point):
        self.array_points.append(point)

    def add_ext_point(self, point):
        self.array_ext_points.append(point)

    def show(self, camera, array_lamps):
        pass


class Cube_static(Object3d):
    def __init__(self, xyz, size):
        self.size = size
        hs = size // 2
        x, y, z = xyz
        p = [
            Point3d(self, POINT_FLAG_MAP, (x - hs, y - hs, z - hs)),
            Point3d(self, POINT_FLAG_MAP, (x - hs, y + hs, z - hs)),

            Point3d(self, POINT_FLAG_MAP, (x + hs, y + hs, z - hs)),
            Point3d(self, POINT_FLAG_MAP, (x + hs, y - hs, z - hs)),

            Point3d(self, POINT_FLAG_MAP, (x - hs, y - hs, z + hs)),
            Point3d(self, POINT_FLAG_MAP, (x - hs, y + hs, z + hs)),

            Point3d(self, POINT_FLAG_MAP, (x + hs, y + hs, z + hs)),
            Point3d(self, POINT_FLAG_MAP, (x + hs, y - hs, z + hs))
        ]
        sur3d = [
            Flat_surface3d(self, [Polygon([p[0], p[1], p[2], p[3]])]),
            Flat_surface3d(self, [Polygon([p[7], p[6], p[5], p[4]])]),
            Flat_surface3d(self, [Polygon([p[0], p[4], p[5], p[1]])]),
            Flat_surface3d(self, [Polygon([p[1], p[2], p[6], p[5]])]),
            Flat_surface3d(self, [Polygon([p[3], p[2], p[6], p[7]])]),
            Flat_surface3d(self, [Polygon([p[0], p[3], p[7], p[4]])])
        ]
        super(Cube_static, self).__init__(xyz, p, sur3d)


class Map(Object3d):
    def __init__(self):
        pass

    def create_grid(self, width, height, step=1,  array_height=None):
        if array_height == None:
            step = step
        else:
            step = height / len(array_height)
        wp, hp = int(width // step), int(height // step)
        brush = Brush(color=BLACK)
        ar = [[None] * wp for i in range(hp)]
        bx, by = -width // 2, -height // 2

        for y in range(hp):
            nx = bx
            for x in range(wp):
                if array_height == None:
                    r = (nx * nx + by * by) / (width ** 2) * math.pi * 2
                    z = 30 * math.cos(r * 1) * r
                else:
                    z = array_height[y][x]
                #print(r,(nx * nx + by * by), (nx , by))
                point = Point3d(pg, brush, (nx, by), z)
                nx += step
                ar[y][x] = point
            by += step
            # print(ar[y])
            Figure2d(pg, brush, ar[y], closed=False)
        for x in range(wp):
            vert_ar = [ar[y][x] for y in range(hp)]
            #print(None in vert_ar)
            Figure2d(pg, brush, vert_ar, closed=False)


class Scene(object):
    def __init__(self):
        self.array_static = []
        self.array_lamps = []

    def add_static(self, obj):
        self.array_static.append(obj)

    def show(self, camera):
        for obj in self.array_static:
            obj.show(camera, self.array_lamps)


class Camera(object):
    def __init__(self, surface, xyz, focus, scene):
        self.xyz = xyz
        self.surface = surface
        self._update = True
        self.width, self.height = surface.get_size()
        self.offset_x, self.offset_y = self.width // 2, self.height // 2
        self.focus = focus
        self.scene = scene
        self.trans_m = crt_rotation_matrix(0, Rotation_0)

    def show(self):
        global phase_3d
        phase_3d += 2
        self.scene.show(self)


class Producer(object):
    """
    PHASE_OBJECT = 1
    PHASE_MAP = 2
    PHASE_CAMERA = 3
    PHASE_SCREEN = 4

    tact_3d = 0
    phase_3d = 0
    camera_3d = 0
    count_camera = 1
    """

    def __init__(self):
        self.cameras = []
        self.count_camera = 0

    def add_camera(self, camera):
        self.cameras.append(camera)
        self.count_camera += 1

    def new_tact():
        global tact_3d, phase_3d
        tact += (PHASE_MAP + self.count_camera * 2)
        phase_3d = 0

    def show(self):
        global phase_3d
        phase_3d = PHASE_MAP
        for cam in self.cameras:
            cam.show()
        self.new_tact()


width, height = 400, 400
h_width, h_height = width // 2, height // 2
# print(sys.getsizeof(screen))
screen = pygame.display.set_mode((width, height), flags=pygame.RESIZABLE)
window = screen.subsurface((10, 10, width-20, height-20))
screen.fill(WHITE)

cube = Cube_static((0, 0, 0), 10)
scene = Scene()
scene.add_static(cube)
camera = Camera(window, (0, 0, -100), 100, scene)
produser = Producer()
produser.add_camera(camera)

produser.show()
