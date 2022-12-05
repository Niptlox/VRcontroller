from Vectors import *
import random

debug = lambda *st, **qw: None
inputD = input
from debuger import *


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


TEN = 10 ** 11


def mround10(n):
    r = round(n, 11)
    ir = int(r)
    cn = r - ir
    cn *= TEN
    ln = cn % 10
    k = cn - ln
    rm = ir + k / TEN
    return rm


def check(V, D, n, M):
    for i in range(n):
        # T = M - V[i]
        # lT = T.len
        # rlT = round(lT, 10)
        # rlT = mround10(lT)
        # Dn = round(D[i], 9)
        # Dn = D[i]
        # if abs(round(lT, 10) - D[i]) > 0.0000000002:
        if abs(round((M - V[i]).len, 10) - D[i]) > 0.0000000002:
            return False
    return True


def getPosition(pArP, pMres):
    global faza
    # d print("pMres", pMres)
    # towers = Towers(arTowers)
    # если дистанция == 0
    V, D, arP = [], [], []
    n = 0
    pArP.sort(key=lambda x: x[3], reverse=True)
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
    debug(V, D, sep="\n")
    # Vi = 0
    sAB_AC = 0
    # базой выбираем максимально удаленную точку
    Ai = 0
    i = 1
    faza = 1
    # точка
    M = 0
    Bmaz = -1
    ABCmax = 0
    while i < n or faza < 0:
        if faza < 0:
            # Проверка точки М на правильность
            resM = round(M, 5)
            if check(V, D, n, resM):
                return resM.xyz
            else:
                faza = -faza
        if faza == 1:
            # Подсчет точки если она на пряиой AB
            # ахождения лучшей точки B
            while i < n:
                Bi = i
                i += 1
                AB = V[Bi] - V[Ai]
                lAB = round(AB.len, 10)
                pABC = 0.5 * (lAB + D[Ai] + D[Bi])
                ABC = pABC * (pABC - lAB) * (pABC - D[Ai]) * (pABC - D[Bi])
                if ABC > ABCmax:
                    ABCmax = ABC
                    Bmax = Bi
                if lAB == D[Bi] + D[Ai]:
                    M = V[Ai] + AB * (D[Ai] / lAB)
                    faza = -faza
                    break
                if lAB == D[Ai] - D[Bi]:
                    M = V[Ai] + AB * (D[Ai] / lAB)
                    faza = -faza
                    break
                if lAB == D[Bi] - D[Ai]:
                    M = V[Ai] - AB * (D[Ai] / lAB)
                    faza = -faza
                    break
            if faza < 0:
                continue
            i = 1
            Bi = Bmax
            if Bi == i:
                i += 1
            faza += 1
        if faza == 2:
            # Нахождение точки С не лежащей на прямой AB
            AB = V[Bi] - V[Ai]
            lAB = AB.len
            eAB = AB / lAB
            while i < n:
                Ci = i
                AC = V[Ci] - V[Ai]
                lAC = AC.len
                sAB_AC = eAB * AC
                i += 1
                if Bi == i:
                    i += 1
                if round(abs(sAB_AC), 11) == round(lAC, 11):
                    pass
                    # if sAB_AC < 0:
                    #     Ai = Ci
                    #     break
                    # else:
                    #     if lAC > lAB:
                    #         Bi = Ci
                    #         break
                else:
                    faza += 1
                    break
        if faza == 3:
            # Нахождение точки М на треуголнике ABC
            eAC = AC / lAC
            # перпендикуляр AC AB
            PABC = eAB ** eAC
            # перпендикуляр AB до AC
            PAB_C = PABC ** AB
            ePAB_C = PAB_C.E
            x, N = getXAB(V, D, Ai, Bi)
            hAMB = math.sqrt(D[Ai] * D[Ai] - x * x)

            NM = ePAB_C * hAMB
            Cd = D[Ci]
            M_p = N + NM
            Mres_p = round(M_p, 5)
            CM_p = Mres_p - V[Ci]
            lCM_p = CM_p.len
            rlCM_p = round(lCM_p, 10)
            if Cd == rlCM_p:
                M = M_p
                faza = -2
                continue
            M = N - NM
            Mres = round(M, 5)
            CM = Mres - V[Ci]
            lCM = CM.len
            rlCM = round(lCM, 10)
            if Cd == rlCM:
                faza = -2
                continue
            faza += 1
            sAB_AC = eAB * AC

        if faza == 4:
            # Нахождение точки D не лежащей на поверхности ABC
            nABC = AB ** AC
            while i < n:
                Di = i
                i += 1
                if Bi == i:
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
            else:
                pass
                # d print("Не нашли точку D фаза 4")
        if faza == 5:
            enABC = nABC.E
            xAB = (D[Ai] ** 2 - D[Bi] ** 2 + lAB ** 2) / (2 * lAB)
            NAB = V[Ai] + eAB * xAB

            eAC = AC / lAC
            xAC = (D[Ai] ** 2 - D[Ci] ** 2 + lAC ** 2) / (2 * lAC)
            NAC = V[Ai] + eAC * xAC

            matrix = [[NAB, AB], [NAC, AC], [V[Ai], enABC]]
            Mat = Matrix(matrix)
            outMat = Mat.kramer()
            # outMat = Mat.solve()
            if outMat == 0:
                # d print("outMat == 0")
                # d print(matrix)
                # d print(Mat.MM.M)
                # d print(Mat.M)
                faza = 4
                continue
            F = Vector3(outMat)
            AF = F - V[Ai]
            sABC_F = enABC * AF
            rsABC_F = round(sABC_F, 10)
            if rsABC_F != 0.0:
                # d print("ALARM MATRIX")
                faza = 4
                continue
            lAF = AF.len
            rlAF = round(lAF, 10)
            if D[Ai] == rlAF:
                faza = 4
                continue
            h = math.sqrt(D[Ai] * D[Ai] - lAF * lAF)
            distD = D[Di]

            M_p = F + enABC * h
            rM_p = round(M_p, 5)
            MD_p = rM_p - V[Di]
            lMD_p = MD_p.len
            distDmy_p = round(lMD_p, 10)
            if distDmy_p == distD:
                M = rM_p
                faza = -4
                continue

            M = F - enABC * h
            rM = round(M, 5)
            MD = rM - V[Di]
            lMD = MD.len
            distDmy = round(lMD, 10)
            if distDmy == distD:
                M = rM
                faza = -4
                continue
            faza = 4
            continue
    return 0


def testDec(n):
    arP = [0] * n
    Mres = Vector3(
        (1.0 * random.randint(-10, 10) + 1.0 * random.random(), 1.0 * random.randint(-10, 10) + 1.0 * random.random(),
         1.0 * random.randint(-10, 10) + 1.0 * random.random()))
    Rt = 1.0 * random.randint(0, 20)
    for i in range(n):
        if Rt < 15:
            Dl = Vector3((1.0 * random.randint(-10, 10) + 1.0 * random.random(),
                          1.0 * random.randint(-10, 10) + 1.0 * random.random(),
                          1.0 * random.randint(-10, 10) + 1.0 * random.random()))
        elif Rt < 25:
            Dl = Vector3((1.0 * random.randint(-10, 10) + 1.0 * random.random(),
                          1.0 * random.randint(-10, 10) + 1.0 * random.random(), 0))
        elif Rt < 30:
            Dl = Vector3((1.0 * random.randint(-10, 10) + 1.0 * random.random(), 0, 0))
        p = Mres + Dl
        arP[i] = (p.x, p.y, p.z, Dl.len)
    return arP, Mres


def test(n):
    arP = [0] * n
    # Mres = Vector3((1.0 * random.randint(-10, 10), 1.0 * random.randint(-10, 10), 1.0 * random.randint(-10, 10)))
    Mres = Vector3((1.0 * random.randint(-10, 10), 1.0 * random.randint(-10, 10), 1.0 * random.randint(-10, 10)))
    # Rt = 1.0 * random.randint(0, 20)
    Rt = 2
    for i in range(n):
        if Rt < 15:
            Dl = Vector3((1.0 * random.randint(-10, 10), 1.0 * random.randint(-10, 10), 1.0 * random.randint(-10, 10)))
        elif Rt < 25:
            Dl = Vector3((1.0 * random.randint(-10, 10), 1.0 * random.randint(-10, 10), 0))
        elif Rt < 30:
            Dl = Vector3((1.0 * random.randint(-10, 10), 0, 0))
        p = Mres + Dl
        arP[i] = (p.x, p.y, p.z, round(Dl.len, 10))
    return arP, Mres


def main():
    # n = int(inputD())
    # arP = [list(map(float, inputD().split())) for _ in range(n)]
    for n in range(3, 2000):
        # n = n * 2
        arP, Mres = test(n)
        # Mres = []
        # print(1)
        # print(arP)
        out = getPosition(arP, Mres)
        if out != 0:
            # d print(1, type(out))
            print(1, *out)
        else:
            print(0)
            # input()
        # d print("faza", faza)
        # if faza != 4:
        # d print("=" * 31)
        # input()
        # print(Mres)

    debug("TRUE:", trueOutput)


if __name__ == '__main__':
    main()
