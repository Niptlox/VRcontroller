


from Vectors import *

debug = print
inputD = input
from debuger import *


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
    EAB = AB / lAB
    x = (D[Ai] ** 2 - D[Bi] ** 2 + lAB ** 2) / (2 * lAB)
    N = V[Ai] + EAB * x
    return x, N


def posPoint3(V, D, Ai, Bi, Ci, getN=False):
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

    debug("X N", x, N)
    NM = ePAB * hAMB
    M = N + NM
    Cd = round(D[Ci], 5)
    lCM = round((M - V[Ci]).len, 5)
    debug("Cd, lCM", Cd, lCM)
    if Cd == lCM:
        return M.xyz
    M = N - NM
    lCM = round((M - V[Ci]).len, 5)
    debug("Cd, lCM", Cd, lCM)
    if Cd == lCM:
        return M.xyz
    if getN:
        return (0, N)
    return 0


def posPoint4(V, D, Ai, Bi, Ci, Di):
    pts = [None] * 4
    plates = ((Ai, Bi, Ci), (Ai, Ci, Di), (Ai, Bi, Di), (Bi, Ci, Di))
    for i in range(4):
        ABCi = plates[i]
        out = posPoint3(V, D, *ABCi, getN=True)
        debug("OUT ABC", out)
        if out != 0:
            if len(out) == 3:
                return out
            pts[i] = out[1]
    debug("Start 4")

    AB = V[Bi] - V[Ai]
    AC = V[Ci] - V[Ai]
    AD = V[Di] - V[Ai]
    eAB = AB.E
    eAC = AC.E
    AB_AC = eAB ** eAC
    EABC = AB_AC.E
    if round(AD * EABC, 10) == 0:
        return 0
    debug("LEN", eAB.len, eAC.len, EABC.len)
    debug("AB", AB, "AC", AC)
    xAB, NAB = getXAB(V, D, Ai, Bi)
    xAC, NAC = getXAB(V, D, Ai, Ci)
    matrix = [[NAB, AB],
              [NAC, AC],
              [V[Ai], EABC]]
    Mat = Matrix(matrix)
    debug("Matrix solve", *matrix, sep="\n")
    F = Vector3(Mat.solve())
    if F == 0:
        return 0
    debug("F", F)
    AF = F - V[Ai]
    lAF = AF.len
    debug("EABC", EABC, AB.E, AC.E)
    debug("D[Ai], lAF", D[Ai], lAF)
    h = math.sqrt(D[Ai] * D[Ai] - lAF * lAF)
    M = F + EABC * h
    debug("Point M1:", M)
    MD = M - V[Di]
    distDmy = round((MD).len, 5)
    distD = round(D[Di], 5)
    if distDmy == distD:
        return M.xyz
    M = F - EABC * h
    debug("Point M2:", M)
    MD = M - V[Di]
    distDmy = round((MD).len, 5)
    if distDmy == distD:
        return M.xyz
    return 0


def getPosition(n, arP):
    # towers = Towers(arTowers)
    # если дистанция == 0
    for x, y, z, d in arP:
        if d == 0:
            return x, y, z
    if n == 1:
        return 0
    V = [Vector3(xyzd[:3]) for xyzd in arP]
    D = [xyzd[3] for xyzd in arP]
    debug(V, D, sep="\n")

    if n == 2:
        return posPoint2(V, D, 0, 1)
    elif n == 3:
        return posPoint3(V, D, 0, 1, 2)
    elif n == 4:
        Ai, Bi, Ci, Di = 0, 1, 2, 3
        return posPoint4(V, D, Ai, Bi, Ci, Di)



def main():
    n = int(inputD())
    arP = [list(map(float, inputD().split())) for _ in range(n)]
    debug(arP)
    out = getPosition(n, arP)
    if out != 0:
        print(1, *[round(num, 5) for num in out])
    else:
        print(0)
    debug("TRUE:", trueOutput)


if __name__ == '__main__':
    main()
