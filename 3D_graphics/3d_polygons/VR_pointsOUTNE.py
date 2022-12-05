# from Vectors import *
import random

#d debug = print
inputD = input
# from debuger import *

import math

# from debuger import *


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

Rotation_0 = 0
Rotation_X = 1
Rotation_Y = 2
Rotation_Z = 3


def mul_matrix(a, b, c=None):
    s = 3
    if c is None:
        c = [[0] * s for i in range(3)]
    for i in range(s):
        for j in range(s):
            c[i][j] = a[i][0] * b[0][j] + a[i][1] * b[1][j] + a[i][2] * b[2][j]
    return c


def crt_rotation_matrix(angle, rot_axis, c=None):
    s = 3
    if c is None:
        c = [[0] * s for i in range(3)]
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
    if c is None:
        c = [0] * s
    for j in range(s):
        c[j] = a[0] * b[0][j] + a[1] * b[1][j] + a[2] * b[2][j]
    return c


def scalar_mul_vectors(a, b):
    c = a[0] * b[0] + a[1] * b[1] + a[2] * b[2]
    return c


def sub_vectors(a, b, c=None):
    s = 3
    if c is None:
        c = [0] * s
    for j in range(s):
        c[j] = a[j] - b[j]
    return c


def sum_vectors(a, b, c=None):
    s = 3
    if c is None:
        c = [0] * s
    for j in range(s):
        c[j] = a[j] + b[j]
    return c


def vector_mul_vector(a, b, c=None):
    s = 3
    if c is None:
        c = [0] * 3
    a1, a2, a3 = a
    b1, b2, b3 = b
    # i = [(a2 * b3 - b2 * a3), 0, 0]
    # j = [0, (a1 * b3 - b1 * a3), 0]
    # k = [0, 0, (a1 * b2 - b1 * a2)]
    c[:] = [(a2 * b3 - b2 * a3), -(a1 * b3 - b1 * a3), (a1 * b2 - b1 * a2)]
    return c


class PointN:
    def __init__(self, coords):
        self.n = len(coords)
        self.__coords = list(coords)

    @property
    def coords(self):
        return self.__coords

    @coords.setter
    def coords(self, coords):
        self.__coords = coords

    def __getitem__(self, index):
        if index >= self.n:
            return 0
        return self.__coords[index]

    def __setitem__(self, index, value):
        self.__coords[index] = value

    def __str__(self):
        return self.__class__.__name__ + str(tuple(self.coords))

    def __repr__(self):
        return str(self)

    def copy(self):
        return self.__class__(self.coords)


class Point3(PointN):
    def __init__(self, xyz):
        super().__init__(xyz)

    @property
    def xyz(self):
        return self.coords

    @xyz.setter
    def xyz(self, xyz):
        self.coords = xyz

    @property
    def x(self):
        return self[0]

    @property
    def y(self):
        return self[1]

    @property
    def z(self):
        return self[2]

    @x.setter
    def x(self, x):
        self[0] = x

    @y.setter
    def y(self, y):
        self[1] = y

    @z.setter
    def z(self, z):
        self[2] = z


class VectorN(PointN):
    def __init__(self, vector):
        super().__init__(vector)
        self._class = VectorN

    # def vectorMul(self, vector):
    #     a1, a2, a3 = self.getXYZ()
    #     b1, b2, b3 = vector.getXYZ()
    #     ar = [(a2 * b3 - b2 * a3), -(a1 * b3 - b1 * a3), (a1 * b2 - b1 * a2)]
    #     return Vector3(ar)

    @property
    def vector(self):
        return self.coords

    @vector.setter
    def vector(self, vector):
        self.coords = vector

    def scalarMul(self, vector):
        return sum([self[i] * vector[i] for i in range(self.n)])

    def mul(self, cof):
        return self._class([self[i] * cof for i in range(self.n)])

    # /
    def __truediv__(self, d):
        return self.mul(1.0 / d)

    # /
    def __floordiv__(self, d):
        return self.mul(1.0 / d)

    # *
    def __mul__(self, other):
        if type(other) == self._class:
            return self.scalarMul(other)
        else:
            return self.mul(other)

    # +
    def __add__(self, vector):
        return self._class([self[j] + vector[j] for j in range(self.n)])

    # -
    def __sub__(self, vector):
        return self._class([self[j] - vector[j] for j in range(self.n)])

    # len
    @property
    def len(self):
        return math.sqrt(self * self)

    # Еденичный вектор
    @property
    def E(self):
        if self.len != 0:
            return self.copy() / self.len

    # ==
    def __eq__(self, other):
        return self._class == type(other) and self.coords == other.coords

    # !=
    def __ne__(self, other):
        return self._class == type(other) and self.coords != other.coords

    @classmethod
    def Zero(cls, n=3):
        return cls([0] * n)

class Vector3(VectorN, Point3):
    n = 3

    def __init__(self, xyz=(0, 0, 0)):
        super().__init__(xyz)
        self._class = self.__class__
        # debugO(self, vars=True)

    def vectorMul(self, vector):
        a1, a2, a3 = self.vector
        b1, b2, b3 = vector.vector
        ar = [(a2 * b3 - b2 * a3), -(a1 * b3 - b1 * a3), (a1 * b2 - b1 * a2)]
        return Vector3(ar)

    # **
    def __pow__(self, other):
        return self.vectorMul(other)

    @classmethod
    def Zero(cls):
        return cls([0] * cls.n)


TLISTS = (tuple, list)

class Matrix:
    def __init__(self, matrix):
        if type(matrix) in TLISTS:
            if type(matrix[0]) in TLISTS:
                matrix = Matrix.createMatrix(matrix)
        else:
            raise Exception("Is not tuple")
        self.n = len(matrix)
        self.M = matrix

    @property
    def matrix(self):
        return self.M

    def solve(self):
        #d debug("===MATRIX SOLVE===")
        M = self.M
        #d debug("Start M:", *M, sep="\n")
        n = self.n
        #d debug("M", M)
        i = 0
        while i < n:
            Mii = M[i][i]
            if Mii == 0:
                j = i + 1
                while j < n and M[j][i] == 0:
                    j += 1
                if j == n:
                    return 0
                    # #d debug("Exception", M)
                    # raise Exception("j == n")
                M[i], M[j] = M[j], M[i]
                Mii = M[i][i]
            if i > 0:
                for j in range(i):
                    Mij = M[i][j]
                    if Mij != 0:
                        M[i] = M[i] - M[j] * Mij
                Mii = M[i][i]
            if Mii == 0:
                continue
            if Mii != 1:
                M[i] = M[i] / Mii
            i += 1
        #d debug("1 M:", *M, sep="\n")
        res = [0] * n
        for i in range(n-1, -1, -1):
            res[i] = M[i][n]
            for j in range(i + 1, n):
                Mij = M[i][j]
                if Mij != 0:
                    M[i][n] -= M[j][n] * Mij
            res[i] = M[i][n]
        #d debug("RES", res)
        # for i in range(n-1, -1, -1):
        #     for j in range(i + 1, n):
        #         Mij = M[i][j]
        #         if Mij != 0:
        #             M[i] = M[i] - M[j] * Mij
        #     res[i] = M[i][n]

        return res

    @classmethod
    def createMatrix(cls, vecs):
        n = len(vecs)
        M = [None] * n
        for i in range(n):
            p, vec = vecs[i]
            M[i] = VectorN((vec[0], vec[1], vec[2], vec * p))
        return M


# if __name__ == '__main__':
#     p = PointN([1, 2, 3])
#     p3 = Point3((5, 59, 3))
#     p3.x = 1
#     print(p3.x)
#     vn1 = VectorN((1, 1, 2, 10))
#     vn2 = VectorN((1, 5, 2, 10))



def inOneLine(V, Ai, Bi, Ci):
    AB = V[Ai] - V[Bi]
    AC = V[Ai] - V[Ci]
    return AB.E == AC.E


def OnePlateFor4(V, Ai, Bi, Ci, i, n):
    AB = V[Ai] - V[Bi]
    AC = V[Ai] - V[Ci]
    AB_AC = AB ** AC
    # eAB = AB.E
    for j in range(i, n):
        AD = V[Ai] - V[j]
        if AB_AC * AD == 0:
            return j
    return False


def OneLineFor3(V, Ai, Bi, i, n):
    AB = V[Ai] - V[Bi]
    eAB = AB.E
    for j in range(i, n):
        AC = V[Ai] - V[j]
        if eAB != AC.E:
            return j - 1
    return n - 1


def posPoint2(V, D, i, j):
    AB = V[j] - V[i]
    lAB = AB.len
    if lAB == D[i] + D[j]:
        return V[i] + AB * (D[i] / lAB)
    if lAB == D[i] - D[j]:
        return V[i] + AB * (D[i] / lAB)
    if lAB == D[j] - D[i]:
        return V[i] - AB * (D[i] / lAB)
    return 0


def getXAB(V, D, Ai, Bi):
    AB = V[Bi] - V[Ai]
    lAB = AB.len
    eAB = AB / lAB
    x = (D[Ai] * D[Ai] - D[Bi] * D[Bi] + lAB * lAB) / (2 * lAB)
    N = V[Ai] + eAB * x
    return x, N


def posPoint3(V, D, Ai, Bi, Ci):
    AB = V[Bi] - V[Ai]
    lAB = AB.len
    for ABi in ((Ai, Bi), (Bi, Ci), (Ai, Ci)):
        outL = posPoint2(V, D, *ABi)
        if outL != 0:
            return outL
    AC = V[Ci] - V[Ai]
    lAC = AC.len
    EAB = AB / lAB
    EAC = AC / lAC
    if EAB == EAC:
        return 0
    # еденичный перпендикуляр AC AB
    PABC = EAB ** EAC
    # еденичный перпендикуляр AB до AC
    PAB_C = PABC ** AB
    ePAB = PAB_C.E
    x, N = getXAB(V, D, Ai, Bi)
    hAMB = math.sqrt(D[Ai] ** 2 - x ** 2)

    #d debug("X N", x, N)
    NM = ePAB * hAMB
    M = N + NM
    Cd = D[Ci]
    lCM = round((M - V[Ci]).len, 10)
    #d debug("Cd, lCM", Cd, lCM)
    if Cd == lCM:
        return M.xyz
    M = N - NM
    lCM = round((M - V[Ci]).len, 10)
    #d debug("Cd, lCM", Cd, lCM)
    if Cd == lCM:
        return M.xyz
    return 0


def posPoint4(V, D, Ai, Bi, Ci, Di):
    AB = V[Bi] - V[Ai]
    AC = V[Ci] - V[Ai]
    AD = V[Di] - V[Ai]
    eAB = AB.E
    eAC = AC.E
    AB_AC = eAB ** eAC
    EABC = AB_AC.E

    xAB, NAB = getXAB(V, D, Ai, Bi)
    xAC, NAC = getXAB(V, D, Ai, Ci)
    matrix = [[NAB, AB], [NAC, AC], [V[Ai], EABC]]
    Mat = Matrix(matrix)
    F = Vector3(Mat.solve())
    if F == 0:
        return 0
    AF = F - V[Ai]
    lAF = AF.len
    h = math.sqrt(D[Ai] * D[Ai] - lAF * lAF)
    M = F + EABC * h
    MD = M - V[Di]
    distDmy = round((MD).len, 5)
    distD = round(D[Di], 5)
    if distDmy == distD:
        return M.xyz
    M = F - EABC * h
    MD = M - V[Di]
    distDmy = round((MD).len, 5)
    if distDmy == distD:
        return M.xyz
    return 0


def getPosition(pArP):
    global faza
    # towers = Towers(arTowers)
    # если дистанция == 0
    V, D, arP = [], [], []
    n = 0
    for i in range(len(pArP)):
        xyzd = pArP[i]
        *xyz, d = xyzd
        if d == 0:
            return xyz
        if xyz not in arP:
            arP.append(xyz)
            V.append(Vector3(xyz))
            D.append(d)
            n += 1
    if n == 1:
        return 0
    # V = [Vector3(xyzd[:3]) for xyzd in arP]
    # D = [xyzd[3] for xyzd in arP]
    #d debug(V, D, sep="\n")
    # Vi = 0
    sAB_AC = 0
    Ai = 0
    Bi = 1
    i = 1
    faza = 0
    while i < n:
        if faza == 0:
            posL = posPoint2(V, D, Ai, Bi)
            if posL:
                return posL.xyz
            i += 1
            faza += 1
            continue
        if faza == 1:
            AB = V[Bi] - V[Ai]
            lAB = AB.len
            eAB = AB / lAB
            while i < n:
                Ci = i
                AC = V[Ci] - V[Ai]
                lAC = AC.len
                sAB_AC = eAB * AC
                i += 1
                if round(abs(sAB_AC), 10) == round(lAC, 10):
                    if sAB_AC < 0:
                        Ai = Ci
                        break
                    else:
                        if lAC > lAB:
                            Bi = Ci
                            break
                else:
                    faza += 1
                    break
        if faza == 2:
            eAC = AC / lAC
            # еденичный перпендикуляр AC AB
            PABC = eAB ** eAC
            # еденичный перпендикуляр AB до AC
            PAB_C = PABC ** AB
            ePAB_C = PAB_C.E
            x, N = getXAB(V, D, Ai, Bi)
            hAMB = math.sqrt(D[Ai] * D[Ai] - x * x)

            NM = ePAB_C * hAMB
            Cd = round(D[Ci], 10)
            M = N + NM
            CM = M - V[Ci]
            lCM = round(CM.len, 10)
            if Cd == lCM:
                return M.xyz
            M = N - NM
            CM = M - V[Ci]
            lCM = round(CM.len, 10)
            if Cd == lCM:
                return M.xyz
            faza += 1
            sAB_AC = eAB * AC

        if faza == 3:
            nABC = AB ** AC
            while i < n:
                Di = i
                i += 1
                AD = V[Di] - V[Ai]
                snABC_AD = nABC * AD
                if round(snABC_AD, 10) == 0:
                    # continue
                    sAB_AD = eAB * AD
                    if D[Ci] < D[Di] and sAB_AC > sAB_AD:
                        Ci = Di
                        AC = AD
                        sAB_AC = sAB_AD
                        break
                else:
                    faza += 1
                    break
        if faza == 4:
            enABC = nABC.E
            xAB = (D[Ai] ** 2 - D[Bi] ** 2 + lAB ** 2) / (2 * lAB)
            NAB = V[Ai] + eAB * xAB

            eAC = AC / lAC
            xAC = (D[Ai] ** 2 - D[Ci] ** 2 + lAC ** 2) / (2 * lAC)
            NAC = V[Ai] + eAC * xAC

            matrix = [[NAB, AB], [NAC, AC], [V[Ai], enABC]]
            Mat = Matrix(matrix)
            outMat = Mat.solve()
            if outMat == 0:
                return 0
            F = Vector3(outMat)
            AF = F - V[Ai]
            lAF = AF.len
            h = math.sqrt(D[Ai] * D[Ai] - lAF * lAF)
            M = F + enABC * h
            MD = M - V[Di]
            distDmy = round((MD).len, 5)
            distD = round(D[Di], 5)
            if distDmy == distD:
                return M.xyz
            M = F - enABC * h
            MD = M - V[Di]
            distDmy = round((MD).len, 5)
            if distDmy == distD:
                return M.xyz
            return 0
    return 0


def test(n):
    arP = [0] * n
    Mres = Vector3((random.randint(-10, 10), random.randint(-10, 10), random.randint(-10, 10)))
    for i in range(n):
        Dl = Vector3((random.randint(-10, 10), random.randint(-10, 10), random.randint(-10, 10)))
        p = Mres + Dl
        arP[i] = (p.x, p.y, p.z, Dl.len)
    return arP, Mres


def main():
    n = int(inputD())
    arP = [list(map(float, inputD().split())) for _ in range(n)]
    for n in range(2, 3):
        # n = 10 ** 5
        # arP, Mres = test(n)
        # print(1)
        # print(arP)
        out = getPosition(arP)
        if type(out) == Vector3:
            out = out.xyz
        if type(out) == int and out == 0:
            print(0)
        else:
            print(1, *[round(num, 5) for num in out])
            # input()
        # print("faza", faza)
        # if faza != 4:
        #     print("=" * 31)
        # print(Mres)

    #d debug("TRUE:", trueOutput)


# if __name__ == '__main__':
main()
