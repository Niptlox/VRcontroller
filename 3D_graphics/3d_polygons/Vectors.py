import math

from debuger import *


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
        self._class = self.__class__

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

    def __round__(self, n):
        return self.__class__([round(x, n) for x in self.coords])

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

    # ?????????????????? ????????????
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
        self.M = matrix
        self.n = len(matrix)

    def copy(self):
        M = [v.copy() for v in self.M]
        return Matrix(M)

    @property
    def matrix(self):
        return self.M

    def det(self):
        m = self.M
        return m[0][0]*(m[1][1]*m[2][2]-m[1][2]*m[2][1])-\
               m[0][1]*(m[1][0]*m[2][2]-m[1][2]*m[2][0])+\
               m[0][2]*(m[1][0]*m[2][1]-m[1][1]*m[2][0])

    def detCol(self, xc):
        M = [v.copy() for v in self.M]
        n = self.n
        for i in range(n):
            M[i][xc]=M[i][n]
        return Matrix(M).det()

    def kramer(self):
        ort = self.det()
        if ort == 0:
            return 0
        n = self.n
        v = [0] * n
        for i in range(n):
            v[i]=self.detCol(i)/ort
        return v

    def solve(self):
        debug("===MATRIX SOLVE===")
        M = self.M
        debug("Start M:", *M, sep="\n")
        n = self.n
        debug("M", M)
        self.MM = self.copy()

        # ar = [-1] * n
        # an = [-1] * n
        # for i in range(n):
        #     pr1, pr2 = -1, 0
        #     pn1, pn2 = -1, 0
        #     for j in range(n):
        #         if M[i][j] != 0:
        #             pr1 = j
        #             pr2 += 1
        #         else:
        #             pn1 = j
        #             pn2 += 1
        #     if pr2 == 1:
        #         if ar[pr1] == -1:
        #             ar[pr1] = i
        #         else:
        #             return 0
        #     if pn2 == 1:
        #         if an[pn1] == -1:
        #             an[pn1] = i
        #         else:
        #             return 0
        # oM = M[:]
        # for i in range(n):
        #     iSt = ar[i]
        #     if iSt != -1:
        #         if iSt != i:
        #             M[i] = oM[iSt]
        #


        i = 0
        while i < n:
            j = i + 1
            while j < n:
                if (M[j][j] == 0.0) and (M[i][j] != 0.0) and (M[j][i] != 0.0):
                    M[i], M[j] = M[j], M[i]
                    break
                j += 1

            Mii = M[i][i]
            if Mii == 0:
                j = i + 1
                while j < n and M[j][i] == 0:
                    j += 1
                if j == n:
                    return 0
                    # debug("Exception", M)
                    # raise Exception("j == n")
                if j > i:
                    M[i], M[j] = M[j], M[i]

                Mii = M[i][i]

            if i > 0:
                for j in range(i):
                    Mij = M[i][j]
                    if Mij != 0:
                        Mj = M[j] * Mij
                        if Mj[i] != M[i][i]:
                            M[i] = M[i] - Mj
                        else:
                            k = i + 1

                Mii = M[i][i]

            if Mii == 0:
                continue

            if Mii != 1:
                M[i] = M[i] / Mii

            i += 1
        debug("1 M:", *M, sep="\n")
        res = [0] * n
        for i in range(n-1, -1, -1):
            res[i] = M[i][n]
            for j in range(i + 1, n):
                Mij = M[i][j]
                if Mij != 0:
                    M[i][n] -= M[j][n] * Mij
            res[i] = M[i][n]
        debug("RES", res)
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
