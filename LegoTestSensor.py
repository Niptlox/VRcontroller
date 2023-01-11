import threading
import time
from multiprocessing import Queue

import ev3_dc as ev3
from thread_task import Sleep

from websocket_async import WebSocketClient

data_queue = Queue()

MOTOR_ONE_DEGREE = 56
STEP = 3
# STEP_DEGREE = MOTOR_ONE_DEGREE * STEP
LOOP_COUNT = 360 // STEP


class MotorsEV3:
    def __init__(self):
        print("START init EV3")
        self.bluetooth_host = '00:16:53:47:03:3A'
        self.my_ev3 = ev3.EV3(protocol=ev3.BLUETOOTH, host=self.bluetooth_host)
        print(self.my_ev3.battery)
        self.degree_1 = 0
        self.degree_2 = 0
        self.motor_1 = ev3.Motor(ev3.PORT_B, ev3_obj=self.my_ev3)
        self.motor_1.speed = 100
        self.motor_2 = ev3.Motor(ev3.PORT_C, ev3_obj=self.my_ev3)
        self.motor_2.speed = 100
        self.motor_2.move_to(0, speed=100, brake=True).start(thread=False)
        self.motors = [self.motor_1, self.motor_2]
        print("FIN init EV3")

    def move_by(self, degree, motor_idx):
        if motor_idx == 0:
            self.degree_1 += degree
        elif motor_idx == 1:
            self.degree_2 += degree
        self.motors[motor_idx].move_by(degree * MOTOR_ONE_DEGREE, brake=True).start(thread=False)


async def new_msg(msg):
    data_queue.put(msg)


def get_data_sensors():
    data = ""
    while data_queue.qsize():
        data = data_queue.get()
    return data


def main():
    print("Sleep 10")
    time.sleep(1)
    while not get_data_sensors():
        pass
    print("Get Offset Gyro")
    time.sleep(10)
    m = [float(el) for el in get_data_sensors().split(";") if el]
    gyro_offset = (m[3], m[4], m[5])
    print("gyro_offset", gyro_offset)


    print("START write")
    cof = 1
    motors = MotorsEV3()
    for i in range(LOOP_COUNT):

        for j in range(LOOP_COUNT):
            with open("SensorsData.csv", "a") as file:
                time.sleep(1)
                while True:
                    data = get_data_sensors()
                    while not data:
                        data = get_data_sensors()
                    m = [float(el) for el in data.split(";") if el]
                    gyro = (m[3], m[4], m[5])
                    if (gyro[0] - gyro_offset[0]) == 0 and (gyro[1] - gyro_offset[1]) == 0 and (gyro[2] - gyro_offset[2]) == 0:
                        break
                file.write(f"{motors.degree_1};{motors.degree_2};{data}\n")
            motors.move_by(-STEP*cof, 1)
        # motors.move_by(STEP*LOOP_COUNT, 1)
        cof *= -1
        motors.move_by(STEP, 0)

    print("FIN write")


if __name__ == '__main__':
    host = '192.168.4.1'
    port = '80'
    websocket_resource_url = f"ws://{host}:{port}/ws"
    # app = App()
    ws_client = WebSocketClient(websocket_resource_url,
                                on_message=lambda ws, msg: new_msg(msg))
    process_app = threading.Thread(target=main)
    process_ws = threading.Thread(target=ws_client.run)
    process_app.start()
    process_ws.start()
    process_app.join()
    process_ws.join()
