DEBUG = True
DEBUG = False
ISTdebug = 0


textInput = """4
-5.30710  7.24030 -1.23090  5.8376287360
-1.01140  2.40600  0.50000  1.6557115600
 0.35000  1.40000  3.56100  3.6476015421
 1.98000  1.75000 -2.05000  5.5483426363"""
trueOutput = "-2.00000 3.28010 1.50000"

textInput = """4
-1.09670  2.46050 -3.25040  4.3513370980
 0.53010 -1.37090 -3.25040  3.9144142014
 2.75010 -1.37090 -3.25040  4.3513370980
-2.44060  0.76030 -3.25040  4.7208526804"""
trueOutput = "0"

def debug(*st, **qw):
    if DEBUG:
        print("DEBUG: ", *st, **qw)


def debugO(self, *st, **qw):
    if DEBUG:
        print("DEBUG OBJECT:", self, type(self))
        if qw.get("vars"):
            print("OBJECT VARS:", self.__dict__)
        if st:
            print("DEBUG: ", *st, **qw)


def inputD(stIN=""):
    global ISTdebug, textInput
    if not DEBUG:
        return input(stIN)
    arrayInput = textInput.split("\n")
    ISTdebug += 1
    return arrayInput[ISTdebug - 1]
