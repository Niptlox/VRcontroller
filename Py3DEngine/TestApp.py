import pygame as pg
from Engine3D import Scene3D, load_object_from_fileobj, create_cube, Camera, Producer, Vector3
import math

from constants import BLACK
from src import App


class AppScene3D(App.Scene):
    def __init__(self, app) -> None:
        super().__init__(app)
        self.tact = 0

        self.screen.fill(BLACK)
        self.scene3d = Scene3D()
        # self.obj = load_object_from_fileobj(self.scene3d, (0, 0, 0), "models/GAMUNCUL1.obj", scale=8)
        # self.obj = load_object_from_fileobj(self.scene3d, (0, 0, 0), "models/controllerVR.obj", scale=5)
        self.obj = load_object_from_fileobj(self.scene3d, (0, 10, 0), "models/monkey1.obj", scale=8)
        # self.obj = Object3d(self.scene3d, (0, 0, 0), [], [], [])

        # self.obj2 = Object3d(self.scene3d, (0, 0, 0), [(0, 0, 0), (0, 10, 0)], [], [])
        # self.obj2 = load_object_from_fileobj(self.scene3d, (0, 0, 0), "models/monkey1.obj", scale=8)
        self.obj2 = create_cube(None, (0, 1, 0), 10)
        # self.scene3d.add_static(self.obj2)
        # self.scene3d.add_static(obj)
        self.scene3d.add_static(self.obj)
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
        speed = 0.1 * self.elapsed_time
        rot_speed = 0.001 * self.elapsed_time
        camera = self.camera
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
        vec_speed = Vector3(0, 0, 0)
        # смещение
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
