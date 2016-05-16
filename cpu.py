
class Registers:
    """Class to hold the registers of the CPU, and allow easy access to them individually and as pairs"""
    def __init__(self):
        #Easy references to the binary representations of the address
        self.RegA = 0b111 # 111
        self.RegB = 0b000 # 000
        self.RegC = 0b001 # 001
        self.RegD = 0b010 # 010
        self.RegE = 0b011 # 011
        self.RegH = 0b100 # 100
        self.RegL = 0b101 # 101

        self.a = 0 # 111
        self.b = 0 # 000
        self.c = 0 # 001
        self.d = 0 # 010
        self.e = 0 # 011
        self.f = 0 #
        self.h = 0 # 100
        self.l = 0 # 101
        self.pc = 0x0100
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

    def setPair(pair, val):
        if (pair == "af"):
            self.f = val & 0b11111111
            self.a = val >> 8

        elif (pair == "bc"):
            self.c = val & 0b11111111
            self.b = val >> 8

        elif (pair == "de"):
            self.e = val & 0b11111111
            self.d = val >> 8

        elif (pair == "hl"):
            self.l = val & 0b11111111
            self.h = val >> 8

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
        #8-bit load instructions
        if(self.opcode == 1 and self.r != 0b110 and self.rb != 0b110): #load instruction r <- rp
            tmp = self.reg.getReg(self.rp)
            self.reg.setReg(self.r, tmp)

        elif(self.opcode == 1 and self.rp == 0b110): # r <- mem[HL]
            memaddr = self.reg.getPair("hl")
            tmp = self.mem.read(memaddr)
            self.reg.setReg(self.r, tmp)

        elif(self.opcode == 1 and self.r == 0b110): #mem[HL] <- rp
            memaddr = self.reg.getPair("hl")
            tmp = self.reg.getReg(self.rp)
            self.mem.write(memaddr, tmp)

        elif(self.opcode == 0 and self.rp == 0b110 and self.r != 0b110): #r <- n
            tmpreg = self.r
            self.fetch() #pull next byte, updates PC along with it.
            self.decode()
            self.reg.setReg(tmpreg, self.n)

        elif(self.opcode == 0 and self.r == 0b110 and self.rp == 0b110): #mem[HL] <- n
            tmpreg = self.reg.getPair("hl")
            self.fetch()
            self.decode()
            self.mem.write(tmpreg, self.n)

        elif(self.opcode == 0 and self.r == 0b001 and self.rp == 0b010): #A <- mem[BC]
            memaddr = self.reg.getPair("bc")
            tmp = self.mem.read(memaddr)
            self.reg.setReg(self.reg.RegA, tmp)

        elif(self.opcode == 0 and self.r == 0b011 and selg.rp == 0b010): #A <- mem[DE]
            memaddr = self.reg.getPair("de")
            tmp = self.mem.read(memaddr)
            self.reg.setReg(self.reg.RegA, tmp)

        elif(self.opcode == 3 and self.r == 0b110 and self.rp == 0b010): #A <- mem[0xFF00 + C]
            memaddr = self.reg.getReg(self.reg.RegC) + 0xFF00
            tmp = self.mem.read(memaddr)
            self.reg.setReg(self.reg.RegA, tmp)

        elif(self.opcode == 3 and self.r == 0b100 and self.rp == 0b010): #mem[0xFF00 + C] <- A
            memaddr = self.reg.getReg(self.reg.RegC) + 0xFF00
            tmp = self.reg.getReg(self.reg.RegA)
            self.mem.write(memaddr, tmp)

        elif(self.opcode == 3 and self.r == 0b110  and self.rp == 0b000): #A <- mem[n]
            self.fetch()
            self.decode()
            tmp = self.mem.read(self.n)
            self.reg.setReg(self.reg.RegA, tmp)

        elif(self.opcode == 3 and self.r == 0b100 and self.rp == 0b000): #mem[n] <- A
            self.fetch()
            self.decode()
            tmp = self.reg.getReg(self.reg.RegA)
            memaddr = 0xFF00 + self.n #this only writes into mem >= 0xFF00
            self.mem.write(memaddr, tmp)


        elif(self.opcode == 3 and self.r == 0b111 and self.rp == 0b010): #A <- mem[nn]
            self.fetch()
            self.decode()
            memaddr = self.n << 8
            self.fetch()
            self.decode()
            memaddr = memaddr + self.n
            tmp = self.mem.read(memaddr)
            self.reg.setReg(self.reg.RegA, tmp)

        elif(self.opcode == 3 and self.r == 0b101 and self.rp == 0b010): #mem[nn] <- A
            self.fetch()
            self.decode()
            memaddr = self.n << 8
            self.fetch()
            self.decode()
            memaddr = memaddr + self.n
            tmp = self.getReg(self.reg.RegA)
            self.mem.write(memaddr, tmp)

        elif(self.opcode == 0 and self.r == 0b101 and self.rp == 0b010): #A <- mem[HL], HL = HL + 1
            memaddr = self.reg.getPair("hl")
            tmp = self.mem.read(memaddr)
            self.reg.setReg(self.reg.RegA, tmp)
            memaddr = memaddr + 1
            self.reg.setPair("hl", memaddr)

        elif(self.opcode == 0 and self.r == 0b111 and self.rp == 0b010): #A <- mem[HL], HL = HL - 1
            memaddr = self.reg.getPair("hl")
            tmp = self.mem.read(memaddr)
            self.reg.setReg(self.reg.RegA, tmp)
            memaddr = memaddr - 1
            self.reg.setPair("hl", memaddr)

        elif(self.opcode == 0 and self.r == 0b000 and self.rp == 0b010): #mem[BC] <- A
            memaddr = self.reg.getPair("bc")
            tmp = self.reg.getReg(self.reg.RegA)
            self.mem.write(memaddr, tmp)

        elif(self.opcode == 0 and self.r == 0b010 and self.rp == 0b010): #mem[DE] <- A
            memaddr = self.reg.getPair("de")
            tmp = self.reg.getReg(self.reg.RegA)
            self.mem.write(memaddr, tmp)

        elif(self.opcode == 0 and self.r == 0b100 and self.rp == 0b010): #mem[HL] <- A, HL = HL + 1
            memaddr = self.reg.getPair("hl")
            tmp = self.reg.getReg(self.reg.RegA)
            self.mem.write(memaddr, tmp)
            memaddr = memaddr + 1
            self.reg.setPair("hl", memaddr)

        elif(self.opcode == 0 and self.r == 0b110 and self.rp == 0b010): #mem[HL] <- A, HL = HL - 1
            memaddr = self.reg.getPair("hl")
            tmp = self.reg.getReg(self.reg.RegA)
            self.mem.write(memaddr, tmp)
            memaddr = memaddr - 1
            self.reg.setPair("hl", memaddr)

        #16 bit load instructions
        elif(self.opcode == 0 and self.rp == 0b001 and self.r%2 == 0): #dd <- nn
            if(self.r == 0b000):
                pair = "bc"

            elif(self.r == 0b010):
                pair = "de"

            elif(self.r == 0b100):
                pair = "hl"

            elif(self.r == 0b110):
                pair = "sp"

            self.fetch()
            self.decode()
            tmp = self.n
            self.fetch()
            self.decode()
            tmp = tmp | (self.n << 8)

            self.reg.setPair(pair, tmp)

        elif(self.opcode == 3 and self.r == 0b111 and self.rp == 0b001): #SP <- HL
            tmp = self.reg.getPair("hl")
            self.reg.setPair("sp", tmp)

        elif(self.opcode == 3 and self.rp == 0b101 and self.r%2 == 0): #mem[SP-1] <- ddH, mem[SP-2] <- ddL
            memaddr = self.reg.getReg("sp")
            if(self.r == 0b000):
                pair = "bc"

            elif(self.r == 0b010):
                pair = "de"

            elif(self.r == 0b100):
                pair = "hl"

            elif(self.r == 0b110):
                pair = "af"

            tmp = self.reg.getPair(pair)
            low = tmp & 0b11111111
            high = tmp >> 8

            self.mem.write(memaddr - 1, high)
            self.mem.write(memaddr - 2, low)
            self.reg.setReg("sp", memaddr - 2)

        elif(self.opcode == 3 and self.rp == 0b001 and self.r%2 == 0): #qqL <- mem[SP], qqH <- mem[SP+1], SP <- SP + 2
            memaddr = self.reg.getReg("sp")
            if(self.r == 0b000):
                hreg == self.reg.RegB
                lreg == self.reg.RegC

            elif(self.r == 0b010):
                hreg == self.reg.RegD
                lreg == self.reg.RegE

            elif(self.r == 0b100):
                hreg == self.reg.RegH
                lreg == self.reg.RegL

            elif(self.r == 0b110):
                hreg == self.reg.RegA
                lreg == "f"

            tmpL = self.mem.read(memaddr)
            tmpH = self.mem.read(memaddr + 1)
            self.reg.setReg(lreg, tmpL)
            self.reg.setReg(hreg, tmpH)
            self.reg.setReg("sp", memaddr - 2)

        elif(self.opcode == 3 and self.r == 0b111 and self.rp == 0b000): #HL <- SP + e
            self.fetch()
            self.decode()
            tmp = self.reg.getReg("sp") + self.n
            self.reg.setPair("hl", tmp)

        elif(self.opcode == 0 and self.r == 0b001 and self.rp == 0b000): #mem[nn] <- SPl, mem[nn+1] <-SPh
            self.fetch()
            self.decode()
            memaddr = self.n
            self.fetch()
            self.decode()
            memaddr = memaddr | (self.n << 8)

            tmp = self.getReg("sp")
            tmpL = tmp & 0b11111111
            tmpH = tmp >> 8
            self.mem.write(memaddr, tmpL)
            self.mem.write(memaddr + 1, tmpH)

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
print(cp.mem.read(258))
cp.mem.write(258, 140)
print(cp.mem.read(258))

for i in range(6): #instructions start at 256
    cp.fetch()
    cp.decode()
    cp.execute()
#print(m.read(0xFFFFF))
