
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

        self.cy = 0

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
                "hl": self.h << 8 | self.l,
                "sp": self.sp
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

    def setPair(self, pair, val):
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

    def setFlag(self, flag, val):
        if(flag == "z"):
            mask = 0b01111111
            tmp = self.f & mask
            self.f = tmp | (val << 7)
        elif(flag == "n"):
            mask = 0b10111111
            tmp = self.f & mask
            self.f = tmp | (val << 6)
        elif(flag == "h"):
            mask = 0b11011111
            tmp = self.f & mask
            self.f = tmp | (val << 5)
        elif(flag == "cy"):
            mask = 0b11101111
            tmp = self.f & mask
            self.f = tmp | (val << 4)

    def getFlag(self, flag):
        if(flag == "z"):
            mask = 0b10000000
            tmp = self.f & mask
            return tmp >> 7
        elif(flag == "n"):
            mask = 0b01000000
            tmp = self.f & mask
            return tmp >> 6
        elif(flag == "h"):
            mask = 0b00100000
            tmp = self.f & mask
            return tmp >> 5
        elif(flag == "cy"):
            mask = 0b00010000
            tmp = self.f & mask
            return tmp >> 4

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
        self.bcd = 0
        self.bcdcy = 0

    def fetch(self):
        self.inst = self.mem.read(self.reg.pc)
        self.reg.pc = self.reg.pc + 1

    def setInst(self, byte):
        self.inst = byte

    def decode(self):
        self.opcode = (self.inst & 0xc0) >> 6 #get bits 7 and 6 to find opcode
        self.r = (self.inst & 0x38) >> 3 #get bits 5, 4, and 3
        self.rp = (self.inst & 0x07) #get first 3 bits
        self.n = self.inst #get n in the event it is needed.

    def execute(self):
        #8-bit load instructions
        if(self.opcode == 1 and self.r != 0b110 and self.rp != 0b110): #load instruction r <- rp
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
            tmp = self.reg.getReg("sp")
            res = tmp  + self.n
            self.reg.setPair("hl", res)
            self.reg.setFlag('z', 0)
            self.reg.setFlag('n', 0)
            if((tmp >> 11) & 0b01 == (res >> 11) & 0b01):
                self.reg.setFlag('h', 0) #carry from 11th bit...
            else:
                self.reg.setFlag('h', 1)
            self.reg.setFlag('cy', (tmp & (1 << 16)) >> 16) #check for carry bit at end

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

        #8 bit arithmatic operations

        elif(self.opcode == 2 and self.r == 0b000 and self.rp != 0b110): #A <- A + rp
            regA = self.reg.getReg(self.regA)
            tmp = self.reg.getReg(self.rp)
            res = tmp + regA
            self.reg.setReg(self.reg.RegA, res)
            self.reg.setFlag('z', 1 if res == 0 else 0)
            self.reg.setFlag('n', 0)
            tmp4 = (tmp & 0b1000) >> 3
            A4 = (regA & 0b1000) >> 3
            res4 = (res & 0b1000) >> 3
            self.reg.setFlag('h', tmp4 ^ A4 ^ res4) #exclusive or the fourth bit s including result to find if their was a carry
            self.reg.setFlag('cy', res >> 8)

        elif(self.opcode == 3 and self.r == 0b000 and self.rp == 0b110): #A <- A + n
            self.fetch()
            self.decode()
            tmpA = self.getReg(self.RegA)
            tmp = self.n
            res = tmpA + tmp
            self.reg.setReg(self.RegA, res)

            self.reg.setFlag('z', 1 if res == 0 else 0)
            self.reg.setFlag('n', 0)
            self.reg.setFlag('cy', res >> 8)
            tmp4 = (tmp & 0b1000) >> 3
            A4 = (regA & 0b1000) >> 3
            res4 = (res & 0b1000) >> 3
            self.reg.setFlag('h', tmp4 ^ A4 ^ res4)

        elif(self.opcode == 2 and self.r == 0b000 and self.r == 0b110): #A <- A + mem[HL]
            memaddr = self.reg.getPair("hl")
            tmpA = self.reg.getReg(self.reg.RegA)
            tmp = self.mem.read(memaddr)
            res = tmp + tmpA
            self.reg.setReg(self.reg.RegA, res)

            self.reg.setFlag('z', 1 if res == 0 else 0)
            self.reg.setFlag('n', 0)
            self.reg.setFlag('cy', res >> 8)
            tmp4 = (tmp & 0b1000) >> 3
            A4 = (regA & 0b1000) >> 3
            res4 = (res & 0b1000) >> 3
            self.reg.setFlag('h', tmp4 ^ A4 ^ res4)

        elif(self.opcode == 2 and self.r == 0b001 and self.rp != 0b110): #A <- A + rp + CY
            tmpA = self.reg.getReg(self.reg.RegA)
            tmp = self.reg.getReg(self.rp)
            CY = self.reg.getFlag('cy')
            res = tmpA + tmp + CY
            self.reg.setReg(self.reg.RegA, tmpA + tmp + CY)

            self.reg.setFlag('z', 1 if res == 0 else 0)
            self.reg.setFlag('n', 0)
            self.reg.setFlag('cy', res >> 8)
            tmp4 = (tmp & 0b1000) >> 3
            A4 = (tmpA & 0b1000) >> 3
            res4 = (res & 0b1000) >> 3
            self.reg.setFlag('h', tmp4 ^ A4 ^ res4)

        elif(self.opcode == 3 and self.r == 0b001 and self.rp == 0b110): #A <- A + n + CY
            tmpA = self.reg.getReg(self.reg.RegA)
            CY = self.reg.getFlag('cy')
            self.fetch()
            self.decode()
            res = tmpA + self.n + CY
            self.reg.setReg(self.reg.RegA, tmp)

            self.reg.setFlag('z', 1 if res == 0 else 0)
            self.reg.setFlag('n', 0)
            self.reg.setFlag('cy', res >> 8)
            tmp4 = (tmp & 0b1000) >> 3
            A4 = (regA & 0b1000) >> 3
            res4 = (res & 0b1000) >> 3
            self.reg.setFlag('h', tmp4 ^ A4 ^ res4)


        elif(self.opcode == 2 and self.r == 0b001 and self.rp == 0b110): #A <- A + mem[HL] + CY
            tmpA = self.reg.getReg(self.reg.RegA)
            CY = self.reg.cy #TODO: Implement this...
            memaddr = self.reg.getPair("hl")
            tmp = self.mem.read(memaddr)
            res = tmpA + tmp + CY
            self.reg.setReg(self.reg.RegA, res)

            self.reg.setFlag('z', 1 if res == 0 else 0)
            self.reg.setFlag('n', 0)
            self.reg.setFlag('cy', res >> 8)
            tmp4 = (tmp & 0b1000) >> 3
            A4 = (regA & 0b1000) >> 3
            res4 = (res & 0b1000) >> 3
            self.reg.setFlag('h', tmp4 ^ A4 ^ res4)

        elif(self.opcode == 2 and self.r == 0b010 and self.rp != 0b110): #A <- A - rp
            tmpA = self.reg.getReg(self.reg.RegA)
            tmp = self.reg.getReg(self.rp)
            res = tmpA - tmp
            self.reg.setReg(self.reg.RegA, res)

            self.reg.setFlag('z', 1 if res == 0 else 0)
            self.reg.setFlag('n', 1)
            self.reg.setFlag('cy', 1 if (tmpA >> 7) == 0 and (tmp >> 7) == 1 else 0) #check for borrowing
            tmp4 = (tmp & 0b100) >> 2
            A4 = (self.reg.RegA & 0b100) >> 2
            self.reg.setFlag('h', 1 if A4 == 0 and tmp4 == 1 else 0) #borrow from bit four

        elif(self.opcode == 3 and self.r == 0b010 and self.rp == 0b110): #A <- A - n
            tmpA = self.reg.getReg(self.reg.RegA)
            self.fetch()
            self.decode()
            tmp = self.n
            res = tmpA - tmp
            self.reg.setReg(self.reg.RegA, res)

            self.reg.setFlag('z', 1 if res == 0 else 0)
            self.reg.setFlag('n', 1)
            self.reg.setFlag('cy', 1 if (tmpA >> 7) == 0 and (tmp >> 7) == 1 else 0) #check for borrowing
            tmp4 = (tmp & 0b100) >> 2
            A4 = (regA & 0b100) >> 2
            self.reg.setFlag('h', 1 if a4 == 0 and tmp4 == 1 else 0) #borrow from bit four

        elif(self.opcode == 2 and self.r == 0b010 and self.rp == 0b110): #A <- A - mem[HL]
            tmpA = self.reg.getReg(self.reg.RegA)
            memaddr = self.reg.getPair("hl")
            tmp = self.mem.read(memaddr)
            res = tmpA - tmp
            self.reg.setReg(self.reg.RegA, res)

            self.reg.setFlag('z', 1 if res == 0 else 0)
            self.reg.setFlag('n', 1)
            self.reg.setFlag('cy', 1 if (tmpA >> 7) == 0 and (tmp >> 7) == 1 else 0) #check for borrowing
            tmp4 = (tmp & 0b100) >> 2
            A4 = (regA & 0b100) >> 2
            self.reg.setFlag('h', 1 if a4 == 0 and tmp4 == 1 else 0) #borrow from bit four

        elif(self.opcode == 2 and self.r == 0b011 and self.rp != 0b110): #A <- A - rp - CY
            tmpA = self.reg.getReg(self.reg.RegA)
            tmp = self.reg.getReg(self.rp)
            CY = self.reg.cy
            self.reg.setReg(self.reg.RegA, tmpA - tmp - CY)

        elif(self.opcode == 3 and self.r == 0b011 and self.rp == 0b110): #A <- A - n - CY
            tmpA = self.reg.getReg(self.reg.RegA)
            CY = self.reg.getFlag('cy')
            self.fetch()
            self.decode()
            res = tmpA - self.n - CY
            self.self.setReg(self.reg.RegA, res)

            self.reg.setFlag('z', 1 if res == 0 else 0)
            self.reg.setFlag('n', 1)
            self.reg.setFlag('cy', 1 if (tmpA >> 7) == 0 and (tmp >> 7) == 1 else 0) #check for borrowing
            tmp4 = (tmp & 0b100) >> 2
            A4 = (regA & 0b100) >> 2
            self.reg.setFlag('h', 1 if a4 == 0 and tmp4 == 1 else 0) #borrow from bit four

        elif(self.opcode == 2 and self.r == 0b011 and self.rp == 0b110): #A <- A - mem[HL] - CY
            tmpA = self.reg.getReg(self.reg.RegA)
            CY = self.reg.cy
            memaddr = self.reg.getPair("hl")
            tmp = self.mem.read(memaddr)
            res = tmpA - tmp - CY
            self.reg.setReg(self.reg.RegA, res)

            self.reg.setFlag('z', 1 if res == 0 else 0)
            self.reg.setFlag('n', 1)
            self.reg.setFlag('cy', 1 if (tmpA >> 7) == 0 and (tmp >> 7) == 1 else 0) #check for borrowing
            tmp4 = (tmp & 0b100) >> 2
            A4 = (regA & 0b100) >> 2
            self.reg.setFlag('h', 1 if a4 == 0 and tmp4 == 1 else 0) #borrow from bit four

        elif(self.opcode == 2 and self.r == 0b100 and self.rp != 0b110): #A <- A & rp
            tmpA = self.reg.getReg(self.reg.RegA)
            tmp = self.reg.getReg(self.rp)
            res = tmpA & tmp
            self.reg.setReg(self.reg.RegA, res)

            self.reg.setFlag('z', 1 if res == 0 else 0)
            self.reg.setFlag('n', 0)
            self.reg.setFlag('cy', 0)
            self.reg.setFlag('h', 1)

        elif(self.opcode == 3 and self.r == 0b100 and self.rp == 0b110): #A <- A & n
            tmpA = self.reg.getReg(self.reg.RegA)
            self.fetch()
            self.decode()
            tmp = self.n
            res = tmpA & tmp
            self.reg.setReg(self.reg.RegA, res)

            self.reg.setFlag('z', 1 if res == 0 else 0)
            self.reg.setFlag('n', 0)
            self.reg.setFlag('cy', 0)
            self.reg.setFlag('h', 1)

        elif(self.opcode == 2 and self.r == 0b100 and self.rp == 0b110): #A <- A & mem[HL]
            tmpA = self.reg.getReg(self.reg.RegA)
            memaddr = self.reg.getPair("hl")
            tmp = self.mem.read(memaddr)
            res = tmpA & tmp
            self.reg.setReg(self.reg.RegA, res)

            self.reg.setFlag('z', 1 if res == 0 else 0)
            self.reg.setFlag('n', 0)
            self.reg.setFlag('cy', 0)
            self.reg.setFlag('h', 1)

        elif(self.opcode == 2 and self.r == 0b110 and self.rp != 0b110): #A <- A | rp
            tmpA = self.reg.getReg(self.reg.RegA)
            tmp = self.reg.getReg(self.rp)
            res = tmpA | tmp
            self.reg.setReg(self.reg.RegA, res)

            self.reg.setFlag('z', 1 if res == 0 else 0)
            self.reg.setFlag('n', 0)
            self.reg.setFlag('cy', 0)
            self.reg.setFlag('h', 0)

        elif(self.opcode == 3 and self.r == 0b110 and self.rp == 0b110): #A <- A | n
            tmpA = self.reg.getReg(self.reg.RegA)
            self.fetch()
            self.decode()
            tmp = self.n
            res = tmpA | tmp
            self.reg.setReg(self.reg.RegA, res)

            self.reg.setFlag('z', 1 if res == 0 else 0)
            self.reg.setFlag('n', 0)
            self.reg.setFlag('cy', 0)
            self.reg.setFlag('h', 0)

        elif(self.opcode == 2 and self.r == 0b110 and self.rp == 0b110): #A <- A | mem[HL]
            tmpA = self.reg.getReg(self.reg.RegA)
            memaddr = self.reg.getPair("hl")
            tmp = self.mem.read(memaddr)
            res = tmpA | tmp
            self.reg.setReg(self.reg.RegA, res)

            self.reg.setFlag('z', 1 if res == 0 else 0)
            self.reg.setFlag('n', 0)
            self.reg.setFlag('cy', 0)
            self.reg.setFlag('h', 0)

        elif(self.opcode == 2  and self.r == 0b101 and self.rp != 0b110): #A <- A xor rp
            tmpA = self.reg.getReg(self.reg.RegA)
            tmp = self.reg.getReg(self.rp)
            res = tmpA ^ tmp
            self.reg.setReg(self.reg.RegA, res)

            self.reg.setFlag('z', 1 if res == 0 else 0)
            self.reg.setFlag('n', 0)
            self.reg.setFlag('cy', 0)
            self.reg.setFlag('h', 0)

        elif(self.opcode == 3 and self.r == 0b101 and self.rp == 0b110): #A <- A xor n
            tmpA = self.reg.getReg(self.reg.RegA)
            self.fetch()
            self.decode()
            res = tmpA ^ self.n
            self.reg.setReg(self.reg.RegA, res)

            self.reg.setFlag('z', 1 if res == 0 else 0)
            self.reg.setFlag('n', 0)
            self.reg.setFlag('cy', 0)
            self.reg.setFlag('h', 0)

        elif(self.opcode == 2 and self.r == 0b101 and self.rp == 0b110): #A <- A xor mem[HL]
            tmpA = self.reg.getReg(self.reg.RegA)
            memaddr = self.reg.getPair("hl")
            tmp = self.mem.read(memaddr)
            res = tmpA ^ tmp
            self.reg.setReg(self.reg.RegA, res)

            self.reg.setFlag('z', 1 if res == 0 else 0)
            self.reg.setFlag('n', 0)
            self.reg.setFlag('cy', 0)
            self.reg.setFlag('h', 0)

        elif(self.opcode == 2 and self.r == 0b111 and self.rp != 0b110): #A == rp
            #"Compares the contents and sets flag if they are equal" <- not exactly a helpful description...
            tmpA = self.reg.getReg(self.reg.RegA)
            tmp == self.reg.getReg(self.rp)

            self.reg.setFlag('z', 1 if tmpA == tmp else 0)
            self.reg.setFlag('n', 1)
            self.reg.setFlag('cy', 1 if tmpA < tmp else 0)
            self.reg.setFlag('h', 1 if tmpA > tmp else 0)

        elif(self.opcode == 3 and self.r == 0b111 and self.rp == 0b110): #A == n
            tmpA == self.reg.getReg(self.reg.RegA)
            self.fetch()
            self.decode()

            self.reg.setFlag('z', 1 if tmpA == tmp else 0)
            self.reg.setFlag('n', 1)
            self.reg.setFlag('cy', 1 if tmpA < tmp else 0)
            self.reg.setFlag('h', 1 if tmpA > tmp else 0)

        elif(self.opcode == 2 and self.r == 0b111 and self.rp == 0b110): #A == mem[HL]
            tmpA == self.reg.getReg(self.reg.RegA)
            memaddr = self.reg.getPair("hl")
            tmp = self.mem.read(memaddr)

            self.reg.setFlag('z', 1 if tmpA == tmp else 0)
            self.reg.setFlag('n', 1)
            self.reg.setFlag('cy', 1 if tmpA < tmp else 0)
            self.reg.setFlag('h', 1 if tmpA > tmp else 0)

        elif(self.opcode == 0 and self.r != 0b110 and self.rp == 0b100): #r <- r + 1
            tmp == self.reg.getReg(self.r)
            res = tmp + 1
            self.reg.setReg(self.r, res)

            self.reg.setFlag('z', 1 if tmp == 0 else 0)
            self.reg.setFlag('n', 0)
            tmp4 = (tmp & 0b1000) >> 3
            res4 = (res & 0b1000) >> 3
            self.reg.setFlag('h', tmp4 ^ res4)

        elif(self.opcode == 0 and self.r == 0b110 and self.rp == 0b100): #mem[HL] <- mem[HL] + 1
            memaddr = self.reg.getPair("hl")
            tmp = self.mem.read(memaddr)
            res = tmp + 1
            self.mem.write(memaddr, res)

            self.reg.setFlag('z', 1 if tmp == 0 else 0)
            self.reg.setFlag('n', 0)
            tmp4 = (tmp & 0b1000) >> 3
            res4 = (res & 0b1000) >> 3
            self.reg.setFlag('h', tmp4 ^ res4)

        elif(self.opcode == 0 and self.r != 0b110 and self.rp == 0b101): #r <- r - 1
            tmp = self.reg.getReg(self.r)
            res = tmp - 1
            self.reg.setReg(self.r, res)

            self.reg.setFlag('z', 1 if res == 0 else 0)
            self.reg.setFlag('n', 1)
            tmp4 = (tmp & 0b1000) >> 3
            res4 = (res & 0b1000) >> 3
            self.reg.setFlag('h', tmp4 ^ res4)

        elif(self.opcode == 0 and self.r == 0b110 and self.rp == 0b101): #mem[HL] <- mem[HL] - 1
            memaddr = self.reg.getPair("hl")
            tmp = self.mem.read(memaddr)
            self.mem.write(memaddr, tmp - 1)

            self.reg.setFlag('z', 1 if tmp == 1 else 0)
            self.reg.setFlag('n', 1)
            tmpbottom = tmp & 0b111
            self.reg.setFlag('h', 1 if tmpbottom == 0 else 0)

        #16 bit arithmatic operations
        elif(self.opcode == 0 and self.r % 2 == 1 and self.rp == 0b001): #HL <- HL + ss
            tmpHL = self.reg.getPair("hl")
            if(self.r == 0b001):
                tmp = self.reg.getPair("bc")
            elif(self.r == 0b011):
                tmp = self.reg.getPair("de")
            elif(self.r == 0b101):
                tmp = self.reg.getPair("hl")
            elif(self.r == 0b111):
                tmp = self.reg.getPair("sp")
            res = tmpHL + tmp
            self.reg.setPair("hl", res)

            self.reg.setFlag('n', 0)
            tmp11 = (tmp >> 10) & 0b1
            res11 = (res >> 10) & 0b1
            tmpHL11 (tmpHL >> 10) & 0b1
            self.reg.setFlag('h', tmp11 ^ res11 ^ tmpHL11)
            self.reg.setFlag('cy', res >> 15)

        elif(self.opcode == 3 and self.r == 0b101 and self.rp == 0b000): #SP <- SP + n
            tmpSL = self.reg.getReg("sp")
            self.fetch()
            self.decode()
            tmp = self.n
            res = tmpSL + tmp
            self.reg.setPair("sp", res)

            self.reg.setFlag('z', 0)
            self.reg.setFlag('n', 0)
            tmp11 = (tmp >> 10) & 0b1
            res11 = (res >> 10) & 0b1
            tmpSL11 = (tmpSL >> 10) & 0b1
            self.reg.setFlag('h', tmp11 ^ res11 ^ tmpSL11)
            self.reg.setFlag('cy', res >> 15)

        elif(self.opcode == 0 and self.r%2 == 0 and self.rp == 0b011): #ss <- ss + 1
            if(self.r == 0b000):
                pair = "bc"
            elif(self.r == 0b010):
                pair = "de"
            elif(self.r == 0b100):
                pair = "hl"
            elif(self.r == 0b110):
                pair = "sp"

            tmp = self.reg.getPair(pair)
            self.reg.setPair(pair, tmp + 1) #No flags get changed

        elif(self.opcode == 0 and self.r%2 == 1 and self.rp == 0b011): #ss <- ss - 1
            if(self.r == 0b001):
                pair = "bc"
            elif(self.r == 0b011):
                pair = "de"
            elif(self.r == 0b101):
                pair = "hl"
            elif(self.r == 0b111):
                pair = "sp"

            tmp = self.reg.getPair(pair)
            self.reg.setPair(pair, tmp - 1)

        #Rotate and Shift
        elif(self.opcode == 0 and self.r == 0b000 and self.rp == 0b111): # A << 1 + A[0], CY = A[7]
            tmpA = self.reg.getReg(self.reg.RegA)
            bit = (tmpA & 0b10000000) >> 7
            tmpA = (tmpA << 1) + bit
            self.reg.setFlag('cy', bit)
            self.reg.setReg(self.reg.RegA, tmpA)
            self.reg.setFlag('z', 0)
            self.reg.setFlag('h', 0)
            self.reg.setFlag('n', 0)

        elif(self.opcode == 0 and self.r == 0b010 and self.rp == 0b111): #A << 1 + A[7]
            tmpA = self.reg.getReg(self.reg.RegA)
            bit = (tmpA & 0b10000000) >> 7
            tmpA = (tmpA << 1) | self.reg.cy
            self.reg.setFlag('cy', bit)
            self.reg.setReg(self.reg.RegA, tmpA)
            self.reg.setFlag('z', 0)
            self.reg.setFlag('h', 0)
            self.reg.setFlag('n', 0)

        elif(self.opcode == 0 and self.r == 0b001 and self.rp == 0b111): #A >> 1 + (A[0] << 7)
            tmpA = self.reg.getReg(self.reg.RegA)
            bit = tmpA & 0b01
            tmpA = (tmpA >> 1) | (bit << 7)
            self.reg.setFlag('cy', bit)
            self.reg.setReg(self.reg.RegA, tmpA)
            self.reg.setFlag('z', 0)
            self.reg.setFlag('h', 0)
            self.reg.setFlag('n', 0)

        elif(self.opcode == 0 and self.r == 0b011 and self.rp == 0b111): #A >> 1 + (A[0] << 7)
            tmpA = self.reg.getReg(self.reg.RegA)
            bit = tmpA & 0b01
            tmpA = (tmpA >> 1) | (self.reg.cy << 7)
            self.reg.setFlag('cy', bit)
            self.reg.setReg(self.reg.RegA, tmpA)
            self.reg.setFlag('z', 0)
            self.reg.setFlag('h', 0)
            self.reg.setFlag('n', 0)

        elif(self.opcode == 3 and self.r == 0b001 and self.rp == 0b011): #rshifts of r or (HL)
            self.fetch()
            self.decode()
            if(self.r == 0b000):
                if(self.rp != 0b110):
                    tmp = self.reg.getReg(self.rp)
                    bit = (tmp & 0b10000000) >> 7
                    tmp = (tmp << 1) | bit
                    self.reg.setFlag('cy', bit)
                    self.reg.setReg(self.rp, tmp)
                else:
                    memaddr = self.reg.getPair("hl")
                    tmp = self.mem.read(memaddr)
                    bit = (tmp & 0b10000000) >> 7
                    tmp = (tmp << 1) | bit
                    self.reg.setFlag('cy', bit)
                    self.mem.write(memaddr, tmp)
            elif(self.r == 0b010):
                if(self.rp != 0b110):
                    tmp = self.reg.getReg(self.rp)
                    bit = (tmp & 0b10000000) >> 7
                    tmp = (tmp << 1) | self.reg.cy
                    self.reg.setFlag('cy', bit)
                    self.reg.setReg(self.rp, tmp)
                else:
                    memaddr = self.reg.getPair("hl")
                    tmp = self.mem.read(memaddr)
                    bit = (tmp & 0b10000000) >> 7
                    tmp = (tmp << 1) | self.reg.cy
                    self.reg.setFlag('cy', bit)
                    self.mem.write(memaddr, tmp)
            elif(self.r == 0b001):
                if(self.rp != 0b110):
                    tmp = self.reg.getReg(self.rp)
                    bit = (tmp & 0b01)
                    tmp = (tmp >> 1) | (bit << 7)
                    self.reg.setFlag('cy', bit)
                    self.reg.setReg(self.rp, tmp)
                else:
                    memaddr = self.reg.getPair("hl")
                    tmp = self.mem.read(memaddr)
                    bit = tmp & 0b01
                    tmp = (tmp >> 1) | (bit << 7)
                    self.reg.setFlag('cy', bit)
                    self.mem.write(memaddr, tmp)
            elif(self.r == 0b011):
                if(self.rp != 0b110):
                    tmp = self.reg.getReg(self.rp)
                    bit = (tmp & 0b01)
                    tmp = (tmp >> 1) | (self.reg.cy << 7)
                    self.reg.setFlag('cy', bit)
                    self.reg.setReg(self.rp, tmp)
                else:
                    memaddr = self.reg.getPair("hl") #NOTE: so this is not what the manual said the opcode was, but the manual seems wrong. so if there weird issues later it could be this
                    tmp = self.mem.read(memaddr)
                    bit = tmp & 0b01
                    tmp = (tmp >> 1) | (self.reg.cy << 7)
                    self.reg.setFlag('cy', bit)
                    self.mem.write(memaddr, tmp)
            elif(self.r == 0b100):
                if(self.rp != 0b110):
                    tmp = self.reg.getReg(self.rp)
                    bit = (tmp & 0b10000000) >> 7
                    tmp = (tmp << 1)
                    self.reg.setFlag('cy', bit)
                    self.reg.setReg(self.rp, tmp)
                else:
                    memaddr = self.reg.getPair("hl")
                    tmp = self.mem.read(memaddr)
                    bit = (tmp & 0b10000000) >> 7
                    tmp = (tmp << 1)
                    self.reg.setFlag('cy', bit)
                    self.mem.write(memaddr, tmp)
            elif(self.r == 0b101):
                if(self.rp != 0b110):
                    tmp = self.reg.getReg(self.rp)
                    bitL = (tmp & 0b01)
                    bitH = tmp & 0b10000000
                    tmp = (tmp >> 1) | bitH
                    self.reg.setFlag('cy', bitL)
                    self.reg.setReg(self.rp, tmp)
                else:
                    memaddr = self.reg.getPair("hl")
                    tmp = self.mem.read(memaddr)
                    bitL = tmp & 0b01
                    bitH = tmp & 0b10000000
                    tmp = (tmp >> 1) | bitH
                    self.reg.setFlag('cy', bitL)
                    self.mem.write(memaddr, tmp)
            elif(self.r == 0b111):
                if(self.rp != 0b110):
                    tmp = self.reg.getReg(self.rp)
                    bit = (tmp & 0b01)
                    tmp = (tmp >> 1)
                    self.reg.setFlag('cy', bit)
                    self.reg.setReg(self.rp, tmp)
                else:
                    memaddr = self.reg.getPair("hl")
                    tmp = self.mem.read(memaddr)
                    bit = tmp & 0b01
                    tmp = (tmp >> 1)
                    self.reg.setFlag('cy', bit)
                    self.mem.write(memaddr, tmp)
            elif(self.r == 0b110):
                if(self.rp != 0b110):
                    tmp = self.reg.getReg(self.rp)
                    low4 = (tmp & 0b01111)
                    high4 = (tmp & 0b11110000)
                    tmp = (low4 << 4) | (high4 >> 4)
                    self.reg.setReg(self.rp, tmp)
                    self.reg.setFlag('cy', 0)
                else:
                    memaddr = self.reg.getPair("hl")
                    tmp = self.mem.read(memaddr)
                    low4 = (tmp & 0b01111)
                    high4 = (tmp & 0b11110000)
                    tmp = (low4 << 4) | (high4 >> 4)
                    self.mem.write(memaddr, tmp)
                    self.reg.setFlag('cy', 0)
            self.reg.setFlag('z', 1 if tmp == 0 else 0)
            self.reg.setFlag('n', 0)
            self.reg.setFlag('h', 0)

        #Bit operations
        elif(self.opcode == 3 and self.r == 0b001 and self.rp == 0b011):
            self.fetch()
            self.decode()
            if(self. opcode == 1 and self.rp != 0b110): #move compliment of selected bit to the Zero flags
                tmp = self.reg.getReg(self.rp)
                if(self.r == 0b000):
                    bit = tmp & 0b00000001
                elif(self.r == 0b001):
                    bit = (tmp & 0b00000010) >> 1
                elif(self.r == 0b010):
                    bit = (tmp & 0b00000100) >> 2
                elif(self.r == 0b011):
                    bit = (tmp & 0b00001000) >> 3
                elif(self.r == 0b100):
                    bit = (tmp & 0b00010000) >> 4
                elif(self.r == 0b101):
                    bit = (tmp & 0b00100000) >> 5
                elif(self.r == 0b110):
                    bit = (tmp & 0b01000000) >> 6
                elif(self.r == 0b111):
                    bit = (tmp & 0b10000000) >> 7
                self.reg.setFlag('z', ~bit)
                self.reg.setFlag('h', 1)
                self.reg.setFlag('n', 0)
            elif(self.opcode == 1 and self.rp == 0b110): #move compliment of selected bit to the Zero flags
                memaddr = self.reg.getPair("hl")
                tmp = self.mem.read(memaddr)
                if(self.r == 0b000):
                    bit = tmp & 0b00000001
                elif(self.r == 0b001):
                    bit = (tmp & 0b00000010) >> 1
                elif(self.r == 0b010):
                    bit = (tmp & 0b00000100) >> 2
                elif(self.r == 0b011):
                    bit = (tmp & 0b00001000) >> 3
                elif(self.r == 0b100):
                    bit = (tmp & 0b00010000) >> 4
                elif(self.r == 0b101):
                    bit = (tmp & 0b00100000) >> 5
                elif(self.r == 0b110):
                    bit = (tmp & 0b01000000) >> 6
                elif(self.r == 0b111):
                    bit = (tmp & 0b10000000) >> 7
                self.reg.setFlag('z', ~bit)
                self.reg.setFlag('h', 1)
                self.reg.setFlag('n', 0)
            elif(self.opcode == 3 and self.rp != 0.110): #set bit to 1
                tmp = self.reg.getReg(self.rp)
                if(self.r == 0b000):
                    tmp = tmp | 0b00000001
                elif(self.r == 0b001):
                    tmp = tmp | 0b00000010
                elif(self.r == 0b010):
                    tmp = tmp | 0b00000100
                elif(self.r == 0b011):
                    tmp = tmp | 0b00001000
                elif(self.r == 0b100):
                    tmp = tmp | 0b00010000
                elif(self.r == 0b101):
                    tmp = tmp | 0b00100000
                elif(self.r == 0b110):
                    tmp = tmp | 0b01000000
                elif(self.r == 0b111):
                    tmp = tmp | 0b10000000
                self.reg.setReg(self.rp, tmp)
            elif(self.opcode == 3 and self.rp == 0b110): #set bit to 1
                memaddr = self.reg.getPair("hl")
                tmp = self.mem.read(memaddr)
                if(self.r == 0b000):
                    tmp = tmp | 0b00000001
                elif(self.r == 0b001):
                    tmp = tmp | 0b00000010
                elif(self.r == 0b010):
                    tmp = tmp | 0b00000100
                elif(self.r == 0b011):
                    tmp = tmp | 0b00001000
                elif(self.r == 0b100):
                    tmp = tmp | 0b00010000
                elif(self.r == 0b101):
                    tmp = tmp | 0b00100000
                elif(self.r == 0b110):
                    tmp = tmp | 0b01000000
                elif(self.r == 0b111):
                    tmp = tmp | 0b10000000
                self.mem.write(memaddr, tmp)
            elif(self.opcode == 3 and self.rp != 0b110): #set bit to 0
                tmp = self.reg.getReg(self.rp)
                if(self.r == 0b000):
                    tmp = tmp & 0b11111110
                elif(self.r == 0b001):
                    tmp = tmp & 0b11111101
                elif(self.r == 0b010):
                    tmp = tmp & 0b11111011
                elif(self.r == 0b011):
                    tmp = tmp & 0b11110111
                elif(self.r == 0b100):
                    tmp = tmp & 0b11101111
                elif(self.r == 0b101):
                    tmp = tmp & 0b11011111
                elif(self.r == 0b110):
                    tmp = tmp & 0b10111111
                elif(self.r == 0b111):
                    tmp = tmp & 0b01111111
                self.reg.setReg(self.rp, tmp)
            elif(self.opcode == 3 and self.rp == 0b110): #set bit to 0
                memaddr = self.reg.getPair("hl")
                tmp = self.mem.read(memaddr)
                if(self.r == 0b000):
                    tmp = tmp & 0b11111110
                elif(self.r == 0b001):
                    tmp = tmp & 0b11111101
                elif(self.r == 0b010):
                    tmp = tmp & 0b11111011
                elif(self.r == 0b011):
                    tmp = tmp & 0b11110111
                elif(self.r == 0b100):
                    tmp = tmp & 0b11101111
                elif(self.r == 0b101):
                    tmp = tmp & 0b11011111
                elif(self.r == 0b110):
                    tmp = tmp & 0b10111111
                elif(self.r == 0b111):
                    tmp = tmp & 0b01111111
                self.mem.write(memaddr, tmp)

        #jump instructions
        elif(self.opcode == 3 and self.r == 0b000 and self.rp == 0b011): #PC <- nn
            self.fetch()
            self.decode()
            addr = self.n
            self.fetch()
            self.decode()
            addr = (self.n << 8) | addr
            self.reg.pc = addr

        elif(self.opcode == 3 and self.r < 4 and self.rp == 0b010): #conditional jump
            cond = self.r
            self.fetch()
            self.decode()
            addr = self.n
            self.fetch()
            self.decode()
            addr = (self.n << 8) | addr
            if(cond == 0b000 and self.reg.z == 0):
                self.reg.pc = addr
            elif(cond == 0b001 and self.reg.z == 1):
                self.reg.pc = addr
            elif(cond == 0b010 and self.reg.cy == 0):
                self.reg.pc = addr
            elif(cond == 0b011 and self.reg.cy == 1):
                self.reg.pc = addr

        elif(self.opcode == 0 and self.r == 0b011 and self.rp == 0b000): #relative jump PC <- PC + e
            self.fetch()
            self.decode()
            self.reg.pc = self.reg.pc + self.n + 1 #NOTE: I do not know if I need the one there

        elif(self.opcode == 0 and self.r > 3 and self.rp == 0b000): #conditional relative jump
            cond = self.r
            self.fetch()
            self.decode()
            if(cond == 0b000 and self.reg.z == 0):
                self.reg.pc = self.reg.pc + self.n
            elif(cond == 0b001 and self.reg.z == 1):
                self.reg.pc = self.reg.pc + self.n
            elif(cond == 0b010 and self.reg.cy == 0):
                self.reg.pc = self.reg.pc + self.n
            elif(cond == 0b011 and self.reg.cy == 1):
                self.reg.pc = self.reg.pc + self.n

        elif(self.opcode == 3 and self.r == 0b101 and self.rp == 0b001): #jump to mem[HL]
            memaddr = self.reg.getPair("hl")
            self.reg.pc = self.mem.read(memaddr)

        #Call and Return instructions
        elif(self.opcode == 3 and self.r == 0b001 and self.rp == 0b101): #mem[SP - 1, - 2] <- PC, PC <- nn, SP <- SP - 2
            memaddr = self.reg.getReg("sp")
            self.mem.write(memaddr - 1, (self.pc & 0b1111111100000000) >> 8)
            self.mem.write(memaddr - 2, (self.pc & 0b11111111))
            self.reg.setReg("sp", memaddr - 2)
            self.fetch()
            self.decode()
            tmp = self.n
            self.fetch()
            self.decode()
            tmp = tmp | (self.n << 8)
            self.pc = tmp

        elif(self.opcode == 3 and self.r < 4 and self.rp == 0b100): #conditional Call
            if(cond == 0b000 and self.reg.z == 0):
                memaddr = self.reg.getReg("sp")
                self.mem.write(memaddr - 1, (self.pc & 0b1111111100000000) >> 8)
                self.mem.write(memaddr - 2, (self.pc & 0b11111111))
                self.reg.setReg("sp", memaddr - 2)
                self.fetch()
                self.decode()
                tmp = self.n
                self.fetch()
                self.decode()
                tmp = tmp | (self.n << 8)
                self.pc = tmp
            elif(cond == 0b001 and self.reg.z == 1):
                memaddr = self.reg.getReg("sp")
                self.mem.write(memaddr - 1, (self.pc & 0b1111111100000000) >> 8)
                self.mem.write(memaddr - 2, (self.pc & 0b11111111))
                self.reg.setReg("sp", memaddr - 2)
                self.fetch()
                self.decode()
                tmp = self.n
                self.fetch()
                self.decode()
                tmp = tmp | (self.n << 8)
                self.pc = tmp
            elif(cond == 0b010 and self.reg.cy == 0):
                memaddr = self.reg.getReg("sp")
                self.mem.write(memaddr - 1, (self.pc & 0b1111111100000000) >> 8)
                self.mem.write(memaddr - 2, (self.pc & 0b11111111))
                self.reg.setReg("sp", memaddr - 2)
                self.fetch()
                self.decode()
                tmp = self.n
                self.fetch()
                self.decode()
                tmp = tmp | (self.n << 8)
                self.pc = tmp
            elif(cond == 0b011 and self.reg.cy == 1):
                memaddr = self.reg.getReg("sp")
                self.mem.write(memaddr - 1, (self.pc & 0b1111111100000000) >> 8)
                self.mem.write(memaddr - 2, (self.pc & 0b11111111))
                self.reg.setReg("sp", memaddr - 2)
                self.fetch()
                self.decode()
                tmp = self.n
                self.fetch()
                self.decode()
                tmp = tmp | (self.n << 8)
                self.pc = tmp

        elif(self.opcode == 3 and self.r == 0b001 and self.rp == 0b001): #Return PC <- mem[SP], SP <- SP + 2
            memaddr = self.reg.getReg("sp")
            tmpPC = self.mem.read(memaddr)
            tmpPC = tmpPC | (self.mem.read(memaddr + 1) << 8)
            self.reg.pc = tmpPC
            self.reg.setReg("sp", memaddr + 2)

        elif(self.opcode == 3 and self.r == 0b011 and self.rp == 0b001): #Return from Interupt PC <- mem[SP], SP <- SP + 2
            memaddr = self.reg.getReg("sp")
            tmpPC = self.mem.read(memaddr)
            tmpPC = tmpPC | (self.mem.read(memaddr + 1) << 8)
            self.reg.pc = tmpPC
            self.reg.setReg("sp", memaddr + 2)

        elif(self.opcode == 3 and self.r < 4 and self.rp == 0b000): #Conditional Return
            if(cond == 0b000 and self.reg.z == 0):
                memaddr = self.reg.getReg("sp")
                tmpPC = self.mem.read(memaddr)
                tmpPC = tmpPC | (self.mem.read(memaddr + 1) << 8)
                self.reg.pc = tmpPC
                self.reg.setReg("sp", memaddr + 2)
            elif(cond == 0b001 and self.reg.z == 1):
                memaddr = self.reg.getReg("sp")
                tmpPC = self.mem.read(memaddr)
                tmpPC = tmpPC | (self.mem.read(memaddr + 1) << 8)
                self.reg.pc = tmpPC
                self.reg.setReg("sp", memaddr + 2)
            elif(cond == 0b010 and self.reg.cy == 0):
                memaddr = self.reg.getReg("sp")
                tmpPC = self.mem.read(memaddr)
                tmpPC = tmpPC | (self.mem.read(memaddr + 1) << 8)
                self.reg.pc = tmpPC
                self.reg.setReg("sp", memaddr + 2)
            elif(cond == 0b011 and self.reg.cy == 1):
                memaddr = self.reg.getReg("sp")
                tmpPC = self.mem.read(memaddr)
                tmpPC = tmpPC | (self.mem.read(memaddr + 1) << 8)
                self.reg.pc = tmpPC
                self.reg.setReg("sp", memaddr + 2)

        elif(self.opcode == 3 and self.rp == 0b111): #RST
            memaddr = self.reg.getReg("sp")
            self.mem.write(memaddr - 1, self.pc >> 8)
            self.mem.wrtie(memaddr - 2, self.pc & 0b11111111)
            self.reg.setReg("sp", memaddr - 2)
            if(self.r == 0b000):
                self.reg.pc = 0x00
            elif(self.r == 0b001):
                self.reg.pc = 0x08
            elif(self.r == 0b010):
                self.reg.pc = 0x10
            elif(self.r == 0b011):
                self.reg.pc = 0x18
            elif(self.r == 0b100):
                self.reg.pc = 0x20
            elif(self.r == 0b101):
                self.reg.pc = 0x28
            elif(self.r == 0b110):
                self.reg.pc = 0x30
            elif(self.r == 0b111):
                self.reg.pc = 0x38

        #General Purpose Insructions
        elif(self.opcode == 0 and self.r == 0b101 and self.rp == 0b111): #invert
            tmp = self.reg.getReg(self.reg.RegA)
            self.reg.setReg(self.reg.RegA, ~tmp)
            self.reg.setFlag('h', 1)
            self.reg.setFlag('n', 1)

        elif(self.opcode == 0 and self.r == 0b000 and self.rp == 0b000): #NOP
            pass

        elif(self.opcode == 1 and self.r == 0b110 and self.rp == 0b110): #Halt
            #I think this works...
            memaddr = self.reg.getReg('sp')
            self.mem.write(memaddr + 1, pc & 0b11111111)
            self.mem.write(memaddr + 2, pc >> 8)
            return -2

        elif(self.opcode == 0 and self.r == 0b010 and self.rp == 0b000): #stop
            #reset all the flags
            self.fetch()
            self.decode()
            if(self.n == 0):
                return -1

        elif(self.opcode == 0 and self.r == 0b100 and self.rp == 0b111): #binary coded decimal adjustment
            self.reg.setReg(self.reg.RegA, self.bcd)
            self.reg.setFlag('cy', self.bcdcy)
            self.reg.setFlag('h', 0)
            self.reg.setFlag('z', 1 if self.bcd == 0 else 0)

        self.prev = self.inst
        print(self.opcode, self.r, self.rp, self.n)
        return 0

    def BCDCalc(add, n, cy, h, A): #calculate what the BCD Result would be if needed. return A, CY
        low == A & 0b1111
        high == (A & 0b11110000) >> 4
        if (add and n == 0): #must adjust the A value for addition
            if(cy == 0 and h == 0):
                if(high <= 0x9 and low <= 0x9):
                    return A, 0
                elif(high <= 0x8 and low >= 0xA):
                    return A + 0x06, 0
                elif(high >= 0xA and low <= 0x9):
                    return A + 0x60, 1
                elif(high >= 0x9 and low >= 0xA):
                    return A + 0x66, 1
            elif(cy == 0 and h == 1):
                if(high <= 0x9 and low <= 0x3):
                    return A + 0x06, 0
                elif(high >= 0xA and low <= 0x03):
                    return A + 0x66, 1
            elif(cy == 1 and h == 0):
                if(high < 0x2):
                    if(low <= 0x9):
                        return A + 0x06, 1
                    else:
                        return A + 0x66, 1
            elif(cy == 1 and h == 1):
                if(high <= 0x03 and low <= 0x03):
                    return A + 0x66, 1

        elif(not add and n == 1): #Adjust A for subtraction
            if(cy == 0 and h == 0 and high <= 0x9 and low <= 0x9):
                return A, 0
            elif(cy == 0 and h == 1 and high <= 0x8 and low >= 0x6):
                return A + 0xFA, 0
            elif(cy == 1 and h == 0 and high >= 0x7 and low <= 0x9):
                return A + 0xA, 1
            elif(cy == 1 and h == 1 and high >= 0x6 and low >= 0x6):
                return A + 0x9A, 1

        #No adjustment
        return A, cy

class Memory():
    """Class for reading and writing to the memory"""
    def __init__(self):
        self.mem = [0] * 0xFFFF #Create an array the size of the GameBoy's memory

    def read(self, address):
        if(address > 0xFFFE):
            raise ValueError("Address out of memory")
        else:
            return self.mem[address]

    def write(self, address, value):
        if (address > 0xFFFE):
            raise ValueError("Address out of memory")
        else:
            self.mem[address] = value
