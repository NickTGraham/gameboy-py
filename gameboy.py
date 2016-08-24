from cpu import *

def main():
    processor = CPU()
    readFile("sample.bin", processor.mem)
    running = 0
    processor.reg.pc = 0
    while running == 0 and processor.reg.pc < 35:
        processor.fetch()
        processor.decode()
        running = processor.execute()

def readFile(filename, mem):
    file = open(filename, 'rb')
    memaddr = 0
    try:
        byte = file.read(1)
        #byte = byte.decode()
        while byte != '\n':
            print('byte ' + bin(ord(byte)))
            mem.write(memaddr, ord(byte))
            memaddr += 1
            byte = file.read(1)
            #byte = byte.decode()
    finally:
        file.close()

def test():
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

    cp.setInst(0b11101000)
    cp.decode()
    cp.execute()

    for i in range(6): #instructions start at 256
        cp.fetch()
        cp.decode()
        cp.execute()
    #print(m.read(0xFFFFF))

if __name__ == '__main__':
    main()
