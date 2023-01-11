from Py3DEngine.Engine3D import Scene3D, Vector3, load_object_from_fileobj, create_cube, Camera, Producer, create_box, \
    create_line, create_pyramid
from VrController import VrController
import VR_points
from websocket_async import WebSocketClient
import math
import pygame as pg
# from Py3DEngine_.app import SkeletonRotate, Angle3, World, SystemCoord, Vector3, Player, Camera, WallCube, Power1Vector, \
#     Power3Vectors
#
# from Py3DEngine_.settings import WINDOW_SIZE, FPS
# from Py3DEngine_.ObjReader import open_file_obj
from multiprocessing import Process, Queue
from src.App import DESKTOP_SIZE
import threading

FPS = 60
FULLSIZE = False
if FULLSIZE:
    WINDOW_SIZE = DESKTOP_SIZE
else:
    WINDOW_SIZE  = (1420, 780)
data_queue = Queue()

MAIN_MODEL_IS_RECT = True

def add_line(scene3d, pos, color=(130, 250, 0)):
    obj = create_cube(None, pos, 0.5, color=(30, 200, 0))
    line = create_line(obj, (0, 0, 0), (0, -10, 0), color=color)
    scene3d.add_static(obj)
    scene3d.add_static(line)
    return line

class ModelController:
    def __init__(self, scene3d, position: Vector3):
        self.scene3d = scene3d

        if MAIN_MODEL_IS_RECT:
            self.model= load_object_from_fileobj(self.scene3d, position, "rect.obj", scale=5)
            # self.model = (*open_file_obj("rect.obj", (5, 5, 5), _convert_faces_to_lines=True),
            #                             rotation=Angle3(math.pi / 2, 0, 0))
        else:
            self.model = load_object_from_fileobj(self.scene3d, position , "controllerVR.obj", scale=5)
            # self.model = SkeletonRotate(*open_file_obj("controllerVR.obj", (5, 5, 5), _convert_faces_to_lines=True),
            #                             rotation=Angle3(math.pi / 2, 0, 0))
        scene3d.add_static(self.model)
        # self.accelM = create_pyramid(obj, (0, 0, 0), 1, (0, -10, 0), color=(230, 100, 0))
        self.accelM = add_line(scene3d, (30, 0, 0), (230, 10, 0))
        self.lineG = add_line(scene3d, (30, 0, 0), (30, 210, 0))
        add_line(scene3d, (30, 0, 0), (210, 210, 210))

        # self.accel1v = Power1Vector(position, 5, color=(255, 0, 255))
        # self.accel3v = Power3Vectors(position, 5)
        # world.add_object(self.accel1v)
        # world.add_object(self.accel3v)

    def fix_state(self):
        model = self.model.copy()
        self.scene3d.add_static(model)

    @property
    def position(self):
        return self.model.position

    @position.setter
    def position(self, position):
        self.model.position = position
        # self.accel1v.position = position
        # self.accel3v.position = position

    def set_rotation(self, rotation):
        self.model.set_rotation(rotation)

    def set_accel(self, accel):
        x,y,z = (Vector3(accel)*3).xyz
        self.accelM.points[2].local_position = Vector3(-y, -z, -x)
        pass
        # self.accel1v.power = accel
        # self.accel3v.power = accel

    def set_G(self, val):
        x,y,z = (Vector3(val)*3).xyz
        self.lineG.points[2].local_position = Vector3(-y, -z, -x)



class App:
    def __init__(self, run=True):
        pg.init()
        pg.mouse.set_visible(False)
        self.elapsed_time = 0
        self.screen = pg.display.set_mode(WINDOW_SIZE)
        self.clock = pg.time.Clock()
        self.font = pg.font.SysFont("", 20)
        # if MAIN_MODEL_IS_RECT:
        #     self.model = SkeletonRotate(*open_file_obj("rect.obj", (5, 5, 5), _convert_faces_to_lines=True),
        #                                 rotation=Angle3(math.pi / 2, 0, 0))
        # else:
        #     self.model = SkeletonRotate(*open_file_obj("controllerVR.obj", (5, 5, 5), _convert_faces_to_lines=True),
        #                                 rotation=Angle3(math.pi / 2, 0, 0))
        self.scene3d = Scene3D()
        self.player = load_object_from_fileobj(self.scene3d, (0,0,0), "man.obj", scale=0.3)
        # self.scene3d.add_static(self.player)
        # self.player = SkeletonRotate(*open_file_obj("man.obj", (1, 1, 1), _convert_faces_to_lines=True),
        #                              rotation=Angle3(math.pi / 2, 0, 0))

        cubes = []
        cube_size = 10
        for i in range(10):
            # create_cube(None, Vector3(-30 + 30 * i, -140, 0), cube_size)
            cubes.append(create_cube(None, Vector3(-80 + 30 * i,-40, 140), cube_size))
            self.scene3d.add_static(cubes[-1])
        #[SystemCoord(Vector3(0, 0, 0), 100), ] + ]

        self.model = ModelController(self.scene3d, position=Vector3(0, 0, 0))

        # self.player = Player(Vector3(-00, 132, 14), rotation=Angle3(0.0, 0, math.pi), mouse_control=0)
        # self.player.set_world(self.world)

        self.camera = Camera(self.scene3d, self.scene3d, self.screen, (0, 0, -150), (0, 0, 0), background=(10, 10, 10),
                             focus=-1)
        self.producer = Producer()
        self.producer.add_camera(self.camera)

        self.vr_controller = VrController(Vector3(self.model.position), self.set_angle, self.set_pos, self.set_accel, self.set_G,
                                          on_down_button=self.down_button)
        self.running = True
        if run:
            self.run()

    def down_button(self, buttons):

        if buttons[1]:
            self.vr_controller.Calibrate()

    def run(self):
        self.render_loop()

    def render_loop(self):
        while self.running:
            self.elapsed_time = self.clock.tick(FPS)
            while data_queue.qsize():
                data = data_queue.get()
                self.vr_controller.NewMsg(data, self.elapsed_time)

            self.screen.fill("#000000")
            for event in pg.event.get():
                if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                    self.exit()
                if event.type == pg.KEYDOWN and event.key == pg.K_1:
                    self.model.position = self.model.position + Vector3(1, 0, 0)
                if event.type == pg.KEYDOWN and event.key == pg.K_2:
                    self.model.position = self.model.position + Vector3(-1, 0, 0)

            # self.camera.render(self.screen)
            # self.player.update(elapsed_time)
            # mini_map.draw(screen)
            self.update_keys()
            self.producer.show()
            self.screen.blit(self.font.render(f"{int(self.clock.get_fps())}fps", False, "#00FF00"), (5, 5))
            self.screen.blit(self.font.render(str(self.camera.position), False, "#00FF00"), (5, 25))
            self.screen.blit(self.font.render(str(self.camera.rotation), False, "#00FF00"), (5, 45))
            self.screen.blit(self.font.render(str(self.model.model.rotation), False, "#00FF00"), (5, 65))
            pg.display.flip()

    def exit(self):
        self.running = False

    def set_accel(self, accel):
        self.model.set_accel(accel)

    def set_G(self, val):
        self.model.set_G(val)

    def set_angle(self, angle):
        # print(angle)
        angle += Vector3(math.pi / 2, 0, 0)
        self.model.set_rotation(Vector3(angle.x, angle.z, -angle.y))
        # self.model.rotation = Angle3(angle.x, angle.z, -angle.y)

    def set_pos(self, pos):
        # print(angle)
        pass
        self.model.position = Vector3(pos.x, pos.y, pos.z)

    def new_accel(self, accel):
        accel

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


async def new_msg(msg):
    data_queue.put(msg)


if __name__ == '__main__':
    host = '192.168.4.1'
    port = '80'
    websocket_resource_url = f"ws://{host}:{port}/ws"
    # app = App()
    ws_client = WebSocketClient(websocket_resource_url,
                                on_message=lambda ws, msg: new_msg(msg))
    process_app = threading.Thread(target=App)
    process_ws = threading.Thread(target=ws_client.run)
    process_app.start()
    process_ws.start()
    process_app.join()
    process_ws.join()
