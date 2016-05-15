
class Registers:
    """Class to hold the registers of the CPU, and allow easy access to them individually and as pairs"""

    def __init__(self):
        self.a = 0
        self.b = 0
        self.c = 0
        self.d = 0
        self.e = 0
        self.f = 0
        self.h = 0
        self.l = 0
        self.pc = 0x0000
        self.sp = 0xFFFE

    def getReg(self, reg):
        return {
                "a": self.a,
                "b": self.b,
                "c": self.c,
                "d": self.d,
                "e": self.e,
                "f": self.f,
                "h": self.h,
                "l": self.l,
                "pc": self.pc,
                "sp": self.sp
                }[reg]

    def getPair(self, pair):
        return {
                "af": self.a << 8 | self.f,
                "bc": self.b << 8 | self.c,
                "de": self.d << 8 | self.e,
                "hl": self.h << 8 | self.l
                }[pair]

    def setReg(self, reg, val):
        if (reg == "a"):
            self.a = val

        elif (reg == "b"):
            self.b = val

        elif (reg == "c"):
            self.c = val

        elif (reg == "d"):
            self.d = val

        elif (reg == "e"):
            self.e = val

        elif (reg == "f"):
            self.f = val

        elif (reg == "h"):
            self.h = val

        elif (reg == "l"):
            self.l = val

        elif (reg == "sp"):
            self.sp = val

        elif (reg == "pc"):
            self.pc = val


class CPU():
    """Class contains the overall CPU Structure, including decoding the instructions"""

    def __init__(self):
        self.reg = Registers()
        self.opcode = 0
        self.r = 0
        self.rp = 0
        self.n = 0
        self.inst = 0
        self.mem = Memory()

    def fetch(self):
        self.inst = self.mem.read(self.reg.pc)
        self.reg.pc = self.reg.pc + 1

    def setInst(self, byte):
        self.inst = byte

    def decode(self):
        self.opcode = (self.inst & 0xc0) >> 6 #get bits 7 and 6 to find opcode
        self.r = (self.inst & 0x38) #get bits 5, 4, and 3
        self.rp = (self.inst & 0x07) #get first 3 bits
        self.n = self.inst #get n in the event it is needed.

    def execute(self):
        print(self.opcode, self.r, self.rp, self.n)


class Memory():
    """Class for reading and writing to the memory"""
    def __init__(self):
        self.mem = [0] * 0xFFFF #Create an array the size of the GameBoy's memory

    def read(self, address):
        if(address > 0xFFFF):
            raise ValueError("Address out of memory")
        else:
            return self.mem[address]

    def write(self, address, value):
        if (address > 0xFFFF):
            raise ValueError("Address out of memory")
        else:
            self.mem[address] = value

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
print(cp.mem.read(4))
cp.mem.write(4, 140)
print(cp.mem.read(4))

for i in range(6):
    cp.fetch()
    cp.decode()
    cp.execute()
#print(m.read(0xFFFFF))
