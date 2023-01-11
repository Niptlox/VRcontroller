import pygame as pg
from Py3DEngine.Engine3D import Scene3D, load_object_from_fileobj, create_cube, Camera, Producer, Vector3, Object3d, create_box
import math

from Py3DEngine.constants import BLACK, GREEN, WHITE, RED
from src import App


def load_data(path="SensorsData3"
                   ".csv"):
    with open(path, "r") as f:
        data = f.readlines()
    data = [list(map(float, line.replace(";\n", "").split(";"))) for line in data if len(line) > 15]
    return data


def create_sphere_sensor(scene3d, length=-1):
    owner = create_sphere(scene3d, (100, 100, 100), radius=9.8, step=6)

    dataSrc = load_data()
    # data = [[Vector3(line[0] / 180 * math.pi, 0, line[1] / 180 * math.pi), Vector3(line[2], line[3], line[4]).length(), Vector3(line[2], line[3], line[4])]
    data = [[Vector3(line[0] / 18 * math.pi, 0, line[1] / 180 * math.pi), Vector3(line[2], line[3], line[4]).length(), Vector3(line[2], line[4], line[3])]
            for line in dataSrc]

    points = [Vector3(0, 0, 0)]
    points = []
    lines = []
    pointsSrc = [Vector3(0, 0, 0)]
    i = 0
    first = True
    for angle, l, p in data[:length]:
        print(angle, l)
        # vec = Vector3(0, l, 0)
        vec = Vector3(0, 9.8, 0)
        point = (vec).rotate_x_rad(-angle.x).rotate_z_rad(-angle.z)
        if not first:
            lines.append((i-1, i))
        else:
            first = False

        points.append(p)
        # points.append(point)

        # pointsSrc.append(point)
        i += 1
        # obj = Object3d(scene3d, (0, 0, 0), [], [], [], rotation=angle)
        # cube = create_cube(None, (0, l, 0), 0.5)
        # scene3d.add_static(obj)
        # scene3d.add_static(cube)
    obj = Object3d(None, (0, 0, 0), points, lines, [], color=GREEN)
    scene3d.add_static(obj)
    objSrc = Object3d(None, (0, 0, 0), pointsSrc, [], [], color=RED)
    boxO = Object3d(None, (0, 0, 0), [], [], [])
    box = create_box(boxO, (0, -15, 0), (10, 0.1, 10))
    scene3d.add_static(boxO)
    scene3d.add_static(box)
    # scene3d.add_static(objSrc)
    return obj, owner, objSrc, box


def create_sphere(scene3d, color, radius=1.0, step=3):
    points = [Vector3(0, 0, 0)]
    for x in range(0, 360, step):
        for z in range(0, 360, step):
            vec = Vector3(0, radius, 0)
            point = (vec).rotate_x(-x).rotate_z(-z)
            points.append(point)
            # obj = Object3d(scene3d, (0, 0, 0), [], [], [], rotation=angle)
            # cube = create_cube(None, (0, l, 0), 0.5)
            # scene3d.add_static(obj)
            # scene3d.add_static(cube)
    obj = Object3d(scene3d, (0, 0, 0), points, [], [], color=color)
    scene3d.add_static(obj)
    return obj


class AppScene3D(App.Scene):
    def __init__(self, app) -> None:
        super().__init__(app)
        self.tact = 0

        self.screen.fill(BLACK)
        self.scene3d = Scene3D()

        self.objs = create_sphere_sensor(self.scene3d)

        self.camera = Camera(self.scene3d, self.scene3d, self.screen, (0, 0, -50), (0, 0, 0), background=(10, 10, 10))
        self.producer = Producer()
        self.producer.add_camera(self.camera)
        self.rot_flag = 0

    def pg_event(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_f:
                self.rot_flag ^= 1
            if event.key == pg.K_c:
                obj = self.obj.__copy__()
                self.scene3d.add_static(obj)

    def update_keys(self):
        keys = pg.key.get_pressed()
        speed = 0.01 * self.elapsed_time
        rot_speed = 0.001 * self.elapsed_time
        # camera = self.obj
        for camera in self.objs:
            # поворот объекта
            rx, ry, rz = 0, 0, 0
            if keys[pg.K_LEFT]:
                ry = -1
            elif keys[pg.K_RIGHT]:
                ry = 1
            if keys[pg.K_UP]:
                rx = -1
            elif keys[pg.K_DOWN]:
                rx = 1
            camera.set_rotation(camera.rotation + Vector3(rx, ry, rz) * rot_speed)
        # camera.owner.set_rotation(camera.rotation + Vector3(rx, ry, rz) * rot_speed)
        vec_speed = Vector3(0, 0, 0)
        # смещение
        camera = self.camera
        ry = camera.rotation.y
        if keys[pg.K_w]:
            vec_speed = Vector3(math.sin(ry), 0, math.cos(ry))
        elif keys[pg.K_s]:
            vec_speed = Vector3(-math.sin(ry), 0, -math.cos(ry))
        if keys[pg.K_a]:
            vec_speed += Vector3(-math.cos(ry), 0, math.sin(ry))
        elif keys[pg.K_d]:
            vec_speed += Vector3(math.cos(ry), 0, -math.sin(ry))
        if keys[pg.K_q]:
            vec_speed += Vector3(0, -1, 0)
        if keys[pg.K_e]:
            vec_speed += Vector3(0, 1, 0)
        camera.position = camera.position + vec_speed * speed

    def update(self):
        pg.display.set_caption(f"Cnt: {len(self.scene3d.static)};fps: {int(self.clock.get_fps())}")
        rot_speed = 0.001 * self.elapsed_time
        if self.rot_flag:
            self.obj2.set_rotation(self.obj2.rotation + Vector3(rot_speed, 0, rot_speed))
            self.obj.set_rotation(self.obj.rotation + Vector3(rot_speed, 0, 0))
            # point = Object3d(self.scene3d, self.obj.points[1].position, [(0, 0, 0)], [], [])
            # self.scene3d.add_static(point)
            # for pos in self.obj2.points:
            #     point = Object3d(self.scene3d, pos.position, [(0, 0, 0)], [], [])
            #     self.scene3d.add_static(point)

        self.producer.show()
        pg.display.flip()
        self.update_keys()


def main():
    FPS = 600
    width, height = 800, 800
    pg.init()
    screen = pg.display.set_mode((width, height), flags=pg.RESIZABLE)
    app = App.App(screen, fps=FPS)
    app.set_scene(AppScene3D(app))
    app.main()


if __name__ == '__main__':
    main()
