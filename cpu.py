
class Registers:
    """Class to hold the registers of the CPU, and allow easy access to them individually and as pairs"""

    def __init__(self):
        global a, b, c, d, e, f, h, l, sp, pc
        a = 0
        b = 0
        c = 0
        d = 0
        e = 0
        f = 0
        h = 0
        l = 0
        pc = 0x0100
        sp = 0xFFFE

    def getReg(self, reg):
        global a, b, c, d, e, f, h, l, sp, pc
        return {
                "a": a,
                "b": b,
                "c": c,
                "d": d,
                "e": e,
                "f": f,
                "h": h,
                "l": l,
                "pc": pc,
                "sp": sp
                }[reg]

    def getPair(self, pair):
        global a, b, c, d, e, f, h, l, sp, pc
        return {
                "af": a << 8 | f,
                "bc": b << 8 | c,
                "de": d << 8 | e,
                "hl": h << 8 | l
                }[pair]

    def setReg(self, reg, val):
        global a, b, c, d, e, f, h, l, sp, pc

        if (reg == "a"):
            a = val

        elif (reg == "b"):
            b = val

        elif (reg == "c"):
            c = val

        elif (reg == "d"):
            d = val

        elif (reg == "e"):
            e = val

        elif (reg == "f"):
            f = val

        elif (reg == "h"):
            h = val

        elif (reg == "l"):
            l = val

        elif (reg == "sp"):
            sp = val

        elif (reg == "pc"):
            pc = val


class CPU():
    """Class contains the overall CPU Structure, including decoding the instructions"""

    def __init__(self):
        self.reg = Registers()
        self.opcode = 0
        self.r = 0
        self.rp = 0
        self.n = 0
        self.inst = 0

    def fetch(self):
        pass
        
    def setInst(self, byte):
        self.inst = byte

    def decode(self):
        self.opcode = (self.inst & 0xc0) >> 6 #get bits 7 and 6 to find opcode
        self.r = (self.inst & 0x38) #get bits 5, 4, and 3
        self.rp = (self.inst & 0x07) #get first 3 bits
        self.n = self.inst #get n in the event it is needed.

    def execute(self):
        pass
x = Registers()
cp = CPU()
print(x.getReg("b"))
x.setReg("b", 5)
print(x.getReg("b"))
print(x.getPair("bc"))
inst = 192
print((inst&192) >> 6)
cp.setInst(34)
print(cp.inst)
cp.decode()
print(cp.opcode)
