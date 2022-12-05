from Vectors import *

debug = print
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
    debug(V, D, sep="\n")
    #Vi = 0
    Ai = 0
    Bi = 1
    i  = 1
    faza = 0
    while i<n:
        if faza==0:
            posL = posPoint2(V, D, Ai, Bi)
            if posL:
                return posL
            if i < n-1:
                i += 1
                faza += 1
        if faza == 1:
            AB =  V[Bi] - V[Ai]
            lAB = AB.len
            eAB = AB / lAB
            while i<n:
                AC = V[i] - V[Ai]
                lAC = AC.len
                sAB_AC = eAB * AC
                Ci = i
                i += 1
                if abs(sAB_AC) == lAC:
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
            pos = posPoint3(V, D, Ai, Bi, Ci)
            if pos:
                return pos
            faza += 1
        if faza == 3:
            nABC = AB ** AC
            while i < n:
                Di = i
                i += 1
                AD = V[Di] - V[Ai]
                snABC_AD = nABC * AD
                if round(snABC_AD, 10) == 0:
                    sAB_AD = eAB * AD
                    if D[Ci] < D[Di] and sAB_AC > sAB_AD:
                        Ci = Di
                        AC = AD
                        sAB_AC = sAB_AD
                        break
                else:
                    faza+=1
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
            F = Vector3(Mat.solve())
            if F == 0:
                return 0
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


def main():
    n = int(inputD())
    arP = [list(map(float, inputD().split())) for _ in range(n)]
    debug(arP)
    out = getPosition(arP)
    if out != 0:
        print(1, *[round(num, 5) for num in out])
    else:
        print(0)
    debug("TRUE:", trueOutput)


if __name__ == '__main__':
    main()
