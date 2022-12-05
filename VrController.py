import math

from pygame import Vector3


class StackAvg:

    def __init__(self, size):

        self.size = size
        self.cnt = 0
        self.lst = [Vector3()] * size
        self.summ = Vector3()
        self.stack_i = 0

    def push(self, vec):
        # print("==========", vec, self.summ, self.lst)
        self.summ += vec
        if self.cnt < self.size:
            self.stack_i = self.cnt
            self.cnt += 1
        else:
            self.stack_i += 1
            if self.stack_i >= self.size:
                self.stack_i = 0
            self.summ -= self.lst[self.stack_i]

        self.lst[self.stack_i] = vec

    def avg(self):
        return sum(self.lst, Vector3()) / self.cnt
        # return self.summ / self.cnt


class VrController:
    def __init__(self, position, on_new_angle, on_new_pos, on_down_button=None):
        self.accel_center = [Vector3(), Vector3()]
        self.position = position
        self.gyroNow = Vector3()
        self.gyroOffset = Vector3()
        self.accelOffset = Vector3()
        self.accelAngle = Vector3()
        self.gyroData = [Vector3(), Vector3()]
        self.accelData = [Vector3(), Vector3()]
        self.accelAvgStack = StackAvg(4)
        self.iterV3 = -1
        self.zDot = 0
        self.zDotSum = 0
        self.zDotSumCnt = 16
        self.zDotSumI = 0
        self.on_new_angle = on_new_angle
        self.on_new_pos = on_new_pos
        self.on_down_button = on_down_button

    def resetGyro(self):
        self.gyroNow.xyz = (0, 0, 0)
        print("resetGyro ", self.gyroNow)

    def Calibrate(self):
        self.gyroOffset.xyz = (self.gyroData[self.iterV3].x, self.gyroData[self.iterV3].y, self.gyroData[self.iterV3].z)
        self.accelOffset.xyz = (self.accelData[self.iterV3].x, self.accelData[self.iterV3].y, self.accelData[self.iterV3].z)
        self.resetGyro()

    def VecToStr(self, vec):
        return "[" + vec.x + "; " + vec.y + "; " + vec.z + "]"

    def angleTan(self, x, y):
        if y == 0:
            if x > 0:
                return 90
            else:
                return -90
        else:
            if x == 0:
                print("zero x", x, y)
            # print(math.atan(y / x), y / x, y, x)
            return math.atan((y / x) if x != 0 else 0) * 180 / math.pi - 90 + (
                (-180 if x < 0 else 90) if y < 0 else (-180 if x < 0 else 0))

    def CalculatePosition(self, degAngle, elapsed_time):
        # TODO: Надо пересчитать скорость
        # ускорение self.accelData[self.iterV3]
        # уголовая скорость self.gyroData[self.iterV3]
        vecNG = Vector3(0, -self.accelOffset.z, 0)

        vecNG.rotate_x_ip(-degAngle.x)
        vecNG.rotate_y_ip(-degAngle.y)
        vecNG.rotate_z_ip(-degAngle.z)
        accelNow = self.accelAvgStack.avg() - vecNG
        self.position += accelNow * elapsed_time

        # self.on_new_pos(self.position)




    def NewMsg(self, st: str, elapsed_time):

        oldIterV3 = self.iterV3
        splitAr = st.split(";")
        n = len(splitAr) - 1
        if (n < 6):
            return
        m = [float(el) for el in splitAr if el]
        # print(m)

        if (self.iterV3 != -1):
            self.iterV3 ^= 1
        else:
            self.iterV3 = 0

        self.accelData[self.iterV3].xyz = (m[0], m[1], m[2]);
        self.accelAvgStack.push(self.accelData[self.iterV3]);

        self.gyroData[self.iterV3].xyz = (m[3], m[4], m[5]);
        v = self.gyroData[self.iterV3] - self.gyroOffset;
        self.gyroNow += v;

        if self.on_down_button:
            self.on_down_button((m[7], m[6], m[8], m[9]))
        # StickButtons.Me.setButtons((int)m[7], (int)m[6], (int)m[8], (int)m[9]);

        if (v.x == 0 and v.y == 0 and v.z == 0):
            self.reset();

        # gyroData[iterV3].magnitude
        self.zDot = self.accelData[self.iterV3].dot(self.accelData[self.iterV3]);
        # print(iterV3+") dot=" + zDot + "         " + VecToStr(gyroNow) + "          " + VecToStr(accelData[iterV3]));

        if (self.zDotSumI < self.zDotSumCnt):
            self.zDotSumI += 1;

        accelAvg = self.accelAvgStack.avg()
        # print(accelAvg)
        degAngle = Vector3(self.angleTan(accelAvg.x, accelAvg.z), -self.gyroNow.z * math.pi,
                           self.angleTan(accelAvg.y, accelAvg.z))
        self.on_new_angle(degAngle / 180 * math.pi);
        self.CalculatePosition(degAngle, elapsed_time)

        return degAngle

    def reset(self):
        pass
