from VrController import VrController
from websocket_async import WebSocketClient
import math
import pygame as pg
from Py3DEngine.app import SkeletonRotate, Angle3, World, SystemCoord, Vector3, Player, Camera

from Py3DEngine.settings import WINDOW_SIZE, FPS
from Py3DEngine.ObjReader import open_file_obj
from multiprocessing import Process, Queue
import threading

data_queue = Queue()


class App:
    def __init__(self):
        pg.init()
        pg.mouse.set_visible(False)
        self.screen = pg.display.set_mode(WINDOW_SIZE)
        self.clock = pg.time.Clock()
        self.font = pg.font.SysFont("", 20)

        self.model = SkeletonRotate(*open_file_obj("controllerVR.obj", (7, 7, 7), _convert_faces_to_lines=True),
                                    rotation=Angle3(math.pi / 2, 0, 0))
        self.world = World([SystemCoord(Vector3(0, 0, 0), 0), self.model])
        self.player = Player(Vector3(-00, 132, 14), rotation=Angle3(0.0, 0, math.pi), mouse_control=0)
        self.player.set_world(self.world)
        self.camera = Camera(self.player, WINDOW_SIZE)
        self.vr_controller = VrController(self.set_angle, on_down_button=self.down_button)
        self.running = True
        self.run()

    def down_button(self, buttons):

        if buttons[1]:
            self.vr_controller.Calibrate()

    def run(self):
        self.render_loop()

    def render_loop(self):
        while self.running:
            while data_queue.qsize():
                data = data_queue.get()
                self.vr_controller.NewMsg(data)
            elapsed_time = self.clock.tick(FPS)

            self.screen.fill("#000000")
            for event in pg.event.get():
                if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                    self.exit()

            self.camera.render(self.screen)
            self.player.update(elapsed_time)
            # mini_map.draw(screen)
            self.screen.blit(self.font.render(f"{int(self.clock.get_fps())}fps", False, "#00FF00"), (5, 5))
            self.screen.blit(self.font.render(str(self.player.position), False, "#00FF00"), (5, 25))
            self.screen.blit(self.font.render(str(self.player.rotation), False, "#00FF00"), (5, 45))
            self.screen.blit(self.font.render(str(self.model.rotation), False, "#00FF00"), (5, 65))
            pg.display.flip()

    def exit(self):
        self.running = False

    def set_angle(self, angle):
        # print(angle)
        angle += Angle3(math.pi/2, 0, 0)
        self.model.rotation = Angle3(angle.x, angle.z, -angle.y)


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
