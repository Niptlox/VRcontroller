import math

from pygame import Vector3

from Py3DEngine.Vectors import MatrixRotation3, mul_vector_matrix

AX, AY, AZ = 0, 1, 2
OX, XO = (1, 0, 0), (-1, 0, 0)
OY, YO = (0, 1, 0), (0, -1, 0)
OZ, ZO = (0, 0, 1), (0, 0, -1)
AXIS = [[OX, OY, OZ], [XO, YO, ZO]]


def findMaxAxis(vec: Vector3):
    maxAxis, maxV = AX, vec.x
    if abs(vec.y) >= abs(maxV):
        maxAxis, maxV = AY, vec.y
    if abs(vec.z) >= abs(maxV):
        maxAxis, maxV = AZ, vec.z

    return maxAxis, maxV, AXIS[int(maxV >= 0)][maxAxis]


def CalcAccel(acc):
    return Vector3(acc.x * acc.x * -0.0027 + acc.x * 0.00, acc.y * acc.y * 0.00 + acc.y * 0.0,
                   acc.z * acc.z * -0.0065 - acc.z * 0.010)


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

    def now(self):
        return self.lst[self.stack_i]

    def last(self):
        return self.lst[self.stack_i - 1]


class VrController:
    def __init__(self, position, on_new_angle, on_new_pos, on_new_accel, on_new_g, on_down_button=None):
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
        self.on_new_accel = on_new_accel
        self.on_down_button = on_down_button
        self.on_new_g = on_new_g

        self.AngleOfG = Vector3(0)

        self.vector_g = Vector3(0)
        self.vector_g_last = Vector3(0)
        self.vector_g_avg = StackAvg(5)

        # какая осб смотрит вверх
        self.AxisAccel = OZ

        self.Grav = Vector3(0)
        self.isCalibrate = False

    def resetGyro(self):
        self.gyroNow.xyz = (0, 0, 0)
        print("resetGyro ", self.gyroNow)

    def Calibrate(self):
        self.gyroOffset.xyz = (self.gyroData[self.iterV3].x, self.gyroData[self.iterV3].y, self.gyroData[self.iterV3].z)
        self.accelOffset.xyz = (
            self.accelData[self.iterV3].x, self.accelData[self.iterV3].y, self.accelData[self.iterV3].z)
        self.resetGyro()
        self.isCalibrate = True

    def VecToStr(self, vec):
        return "[" + vec.x + "; " + vec.y + "; " + vec.z + "]"

    def angleTan(self, x, y, to_degrees=True):
        if to_degrees:
            return math.degrees(math.atan2(x, y))
        return math.atan2(y, x)

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
        self.position += accelNow

        # self.on_new_pos(self.position)

    def NewMsg(self, st: str, elapsed_time):

        # oldIterV3 = self.iterV3
        splitAr = st.split(";")
        # print(splitAr)
        n = len(splitAr) - 1
        if (n < 6):
            return
        m = [float(el) for el in splitAr if el]
        # print(m)

        # смена итерации
        if self.iterV3 != -1:
            self.iterV3 ^= 1
        else:
            self.iterV3 = 0
        if self.on_down_button:
            self.on_down_button((m[7], m[6], m[8], m[9]))

        self.accelData[self.iterV3].xyz = (m[0], m[1], m[2]);
        self.gyroData[self.iterV3].xyz = (m[3], m[4], m[5]);
        self.accelAvgStack.push(self.accelData[self.iterV3]);
        self.on_new_accel(self.accelData[self.iterV3])

        if not self.isCalibrate:
            self.Calibrate()

        acc = self.accelData[self.iterV3]
        accL = acc.length_squared()

        gyro = self.gyroData[self.iterV3] - self.gyroOffset;

        dZero = Vector3(2.5, 0.13, -3.74)
        dZero = Vector3(0, 0, 0)
        if gyro.x == 0 and gyro.y == 0 and gyro.z == 0:
            self.Grav = acc
            # na = Vector3(acc.x * 0.03, acc.y*-0.015, acc.z * -0.09)
            # na = Vector3(acc.x * 0.03, acc.y * acc.y * 0.0055 + acc.y * 0.0, acc.z* acc.z * -0.0065 - acc.z * 0.010)
            # na = Vector3(acc.x * acc.x * -0.0027 + acc.x * 0.00, acc.y * acc.y * 0.00 + acc.y * 0.0,
            #              acc.z * acc.z * -0.0065 - acc.z * 0.010)
            na = CalcAccel(acc)
            self.Grav = vv = acc + na + dZero
            vvL = vv.length_squared()
            print("Zero", acc, vv, acc.length_squared(), vvL)
        else:
            self.gyroNow += gyro;
            accMove = acc - self.Grav
            gyroC = gyro / math.pi

            grav = self.Grav#.normalize() * 10.1

            mat = MatrixRotation3(-Vector3(gyroC)).get_matrix()

            gravM = Vector3(mul_vector_matrix(grav, mat))
            self.on_new_g(gravM)
            gravML = gravM.length_squared()
            # n_acc = CalcAccel(acc)
            n_acc = acc
            accSub = n_acc - gravM
            delta_pos = Vector3(accSub.y, accSub.z, accSub.x) * 0.1
            self.position += delta_pos
            self.on_new_pos(self.position)

            # print("l", self.Grav, acc, gyro, gravM, accL, gravML, accSub, )

        # StickButtons.Me.setButtons((int)m[7], (int)m[6], (int)m[8], (int)m[9]);

        # if (gyro.x == 0 and gyro.y == 0 and gyro.z == 0) or 1:
        #     self.resetAngleOfG();
        #
        # # gyroData[iterV3].magnitude
        # self.zDot = self.accelData[self.iterV3].dot(self.accelData[self.iterV3]);
        # # print(iterV3+") dot=" + zDot + "         " + VecToStr(gyroNow) + "          " + VecToStr(accelData[iterV3]));
        #
        # if (self.zDotSumI < self.zDotSumCnt):
        #     self.zDotSumI += 1;
        #
        # # accelAvg = self.accelAvgStack.avg()
        # # print("accel", accelAvg.length_squared())
        # # self.on_new_accel(accelAvg)
        # # # print(accelAvg)
        # # degAngle = Vector3(self.angleTan(accelAvg.x, accelAvg.z), -self.gyroNow.z * math.pi,
        # #                    self.angleTan(accelAvg.y, accelAvg.z))
        #
        # self.on_new_angle(self.resultAngle * (math.pi / 180));
        #
        # self.CalculatePosition(self.resultAngle, elapsed_time)
        #

    def resetAngleOfG(self):
        # контроллер не шевелится, сбрасываем угол исходя из G
        # TODO: доделать

        # accelAvg = self.accelAvgStack.avg()
        accelVal = self.accelData[self.iterV3]
        accNorm = accelVal.normalize()
        maxAxis, maxV, axisVec = findMaxAxis(accNorm)
        print("accel", int(accelVal.length_squared()), axisVec)

        # self.on_new_accel(accelVal)
        # print(accelAvg)
        if maxAxis == AZ:
            self.AngleOfG = Vector3(self.angleTan(accelVal.x, accelVal.z), -self.gyroNow.z * math.pi,
                                    self.angleTan(accelVal.y, accelVal.z))
        elif maxAxis == AX:
            self.AngleOfG = Vector3(self.angleTan(accelVal.z, accelVal.x), -self.gyroNow.x * math.pi,
                                    self.angleTan(accelVal.y, accelVal.x))
        elif maxAxis == AY:
            self.AngleOfG = Vector3(self.angleTan(accelVal.x, accelVal.y), -self.gyroNow.y * math.pi,
                                    self.angleTan(accelVal.z, accelVal.y))
        self.resultAngle = self.AngleOfG
        # self.on_new_angle(degAngle * (math.pi / 180));

        pass
