from VrController import VrController
import VR_points
from websocket_async import WebSocketClient
import math
import pygame as pg
from Py3DEngine.app import SkeletonRotate, Angle3, World, SystemCoord, Vector3, Player, Camera, WallCube, Power1Vector, \
    Power3Vectors

from Py3DEngine.settings import WINDOW_SIZE, FPS
from Py3DEngine.ObjReader import open_file_obj
from multiprocessing import Process, Queue
import threading

data_queue = Queue()

MAIN_MODEL_IS_RECT = True


class ModelController:
    def __init__(self, world: World, position: Vector3):
        self.world = world

        if MAIN_MODEL_IS_RECT:
            self.model = SkeletonRotate(*open_file_obj("rect.obj", (5, 5, 5), _convert_faces_to_lines=True),
                                        rotation=Angle3(math.pi / 2, 0, 0))
        else:
            self.model = SkeletonRotate(*open_file_obj("controllerVR.obj", (5, 5, 5), _convert_faces_to_lines=True),
                                        rotation=Angle3(math.pi / 2, 0, 0))
        self.model.position = position
        self.accel1v = Power1Vector(position, 5, color=(255, 0, 255))
        self.accel3v = Power3Vectors(position, 5)
        world.add_object(self.model)
        world.add_object(self.accel1v)
        world.add_object(self.accel3v)

    def fix_state(self):
        model = self.model.copy()
        self.world.add_object(model)

    @property
    def position(self):
        return self.model.position

    @position.setter
    def position(self, position):
        self.model.position = position
        self.accel1v.position = position
        self.accel3v.position = position

    def set_rotation(self, rotation):
        self.model.rotation = rotation

    def set_accel(self, accel):
        self.accel1v.power = accel
        self.accel3v.power = accel


class App:
    def __init__(self, run=True):
        pg.init()
        pg.mouse.set_visible(False)
        self.screen = pg.display.set_mode(WINDOW_SIZE)
        self.clock = pg.time.Clock()
        self.font = pg.font.SysFont("", 20)
        # if MAIN_MODEL_IS_RECT:
        #     self.model = SkeletonRotate(*open_file_obj("rect.obj", (5, 5, 5), _convert_faces_to_lines=True),
        #                                 rotation=Angle3(math.pi / 2, 0, 0))
        # else:
        #     self.model = SkeletonRotate(*open_file_obj("controllerVR.obj", (5, 5, 5), _convert_faces_to_lines=True),
        #                                 rotation=Angle3(math.pi / 2, 0, 0))
        self.player = SkeletonRotate(*open_file_obj("man.obj", (1, 1, 1), _convert_faces_to_lines=True),
                                     rotation=Angle3(math.pi / 2, 0, 0))

        cubes = []
        cube_size = 10
        for i in range(10):
            cubes.append(WallCube(Vector3(-30 + 30 * i, -140, 0), cube_size, cube_size), )
        #[SystemCoord(Vector3(0, 0, 0), 100), ] + ]
        self.world = World(cubes)
        self.model = ModelController(self.world, position=Vector3(0, 0, 0))

        self.player = Player(Vector3(-00, 132, 14), rotation=Angle3(0.0, 0, math.pi), mouse_control=0)
        self.player.set_world(self.world)
        self.camera = Camera(self.player, WINDOW_SIZE)
        self.vr_controller = VrController(Vector3(self.model.position), self.set_angle, self.set_pos, self.set_accel,
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
            elapsed_time = self.clock.tick(FPS)
            while data_queue.qsize():
                data = data_queue.get()
                self.vr_controller.NewMsg(data, elapsed_time)

            self.screen.fill("#000000")
            for event in pg.event.get():
                if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                    self.exit()
                if event.type == pg.KEYDOWN and event.key == pg.K_1:
                    self.model.position = self.model.position + Vector3(1, 0, 0)
                if event.type == pg.KEYDOWN and event.key == pg.K_2:
                    self.model.position = self.model.position + Vector3(-1, 0, 0)

            self.camera.render(self.screen)
            self.player.update(elapsed_time)
            # mini_map.draw(screen)
            self.screen.blit(self.font.render(f"{int(self.clock.get_fps())}fps", False, "#00FF00"), (5, 5))
            self.screen.blit(self.font.render(str(self.player.position), False, "#00FF00"), (5, 25))
            self.screen.blit(self.font.render(str(self.player.rotation), False, "#00FF00"), (5, 45))
            self.screen.blit(self.font.render(str(self.model.model.rotation), False, "#00FF00"), (5, 65))
            pg.display.flip()

    def exit(self):
        self.running = False

    def set_accel(self, accel):
        self.model.set_accel(accel)

    def set_angle(self, angle):
        # print(angle)
        angle += Angle3(math.pi / 2, 0, 0)
        self.model.set_rotation(Angle3(angle.x, angle.z, -angle.y))
        # self.model.rotation = Angle3(angle.x, angle.z, -angle.y)

    def set_pos(self, pos):
        # print(angle)
        pass
        self.model.position = Vector3(pos.x, pos.z, pos.y)

    def new_accel(self, accel):
        accel


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
