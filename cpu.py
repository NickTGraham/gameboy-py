
class Registers:
    """Class to hold the registers of the CPU, and allow easy access to them individually and as pairs"""

    def __init__(self):
        self.a = 0 # 111
        self.b = 0 # 000
        self.c = 0 # 001
        self.d = 0 # 010
        self.e = 0 # 011
        self.f = 0 #
        self.h = 0 # 100
        self.l = 0 # 101
        self.pc = 0x0000
        self.sp = 0xFFFE

    def getReg(self, reg):
        return {
                0b111: self.a,
                0b000: self.b,
                0b001: self.c,
                0b010: self.d,
                0b110: self.e,
                "f": self.f,
                0b100: self.h,
                0b101: self.l,
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
        if (reg == 0b111):
            self.a = val

        elif (reg == 0b000):
            self.b = val

        elif (reg == 0b001):
            self.c = val

        elif (reg == 0b010):
            self.d = val

        elif (reg == 0b011):
            self.e = val

        elif (reg == "f"):
            self.f = val

        elif (reg == 0b100):
            self.h = val

        elif (reg == 0b101):
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
        #there are now switch case statements in python so...
        if(self.opcode == 1 and self.r != 0b110 and self.rb != 0b110): #load instruction
            tmp = self.reg.getReg(self.rp)
            self.reg.setReg(self.r, tmp)

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
print(x.getReg(0b000))
x.setReg(0b000, 5)
print(x.getReg(0b000))
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
