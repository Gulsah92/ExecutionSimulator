import Memory
import CPU
import sys
import BinReader

# program_name = sys.argv[0]
# file_path = sys.argv[1]

# Instantiate CPU and Memory
cpu = CPU.cpu()
mem = Memory.Memory()

# Open binary file and get binaries as list
binaries = BinReader.Binary('test.bin').binl

# Register dictionary to look up char values of registers
regs = {'0000000000000001' : 'a', '0000000000000010' : 'b', '0000000000000011' : 'c', '0000000000000100' : 'd',
        '0000000000000101' : 'e', '0000000000000110' : 's', '0000000000000000' : 'pc'}

#Load instructions and data to memory
for inst in binaries:
    mem.set2mem(inst,binaries.index(inst))

#Run instructions using PC and memory
IsRunning = True
while IsRunning:
    # Halt op
    if mem.get(cpu.pc)[0] == '000001':
        IsRunning = False
    # Load op
    elif mem.get(cpu.pc)[0] == '000010':
        # immediate addressing
        if mem.get(cpu.pc)[1] == '00':
            # print(mem.get(cpu.pc)[2])
            cpu.a = mem.get(cpu.pc)[2]
            # print(cpu)
            cpu.pc = cpu.pc + 1
            # print(cpu)
        # Todo: Add register, direct memory and indirect memory addressing modes
    # Store op
    elif mem.get(cpu.pc)[0] == '000011':
        # Register addressing
        if mem.get(cpu.pc)[1] == '01':
            cpu.set(regs[mem.get(cpu.pc)[2]], cpu.get('a'))
            cpu.pc = cpu.pc + 1
            # print(cpu)
        # Todo: Add direct memory and indirect memory addressing
    #  Print op
    elif mem.get(cpu.pc)[0] == '100100':
        # Register addressing
        if mem.get(cpu.pc)[1] == '01':
            bin_asc = cpu.get(regs[mem.get(cpu.pc)[2]])
            if bin_asc[0:8] == '00000000':
                dec_asc = int(bin_asc[8:], 2)
                print(chr(dec_asc))
                cpu.pc = cpu.pc + 1
            else:
                dec_asc_2 = int(bin_asc[8:], 2)
                dec_asc_1 = int(bin_asc[:8], 2)
                print(chr(dec_asc_1) + chr(dec_asc_2))
                cpu.pc = cpu.pc + 1

        # {'HALT': '000001', 'LOAD': '000010', 'STORE': '000011', 'ADD': '000100', 'SUB': '000101', 'INC': '000110',
        #  'DEC': '000110', 'MUL': '001000', 'DIV': '001001', 'XOR': '001010', 'AND': '001011', 'OR': '001100',
        #  'NOT': '001101', 'SHL': '001110', 'SHR': '001111', 'NOP': '010000', 'PUSH': '010001', 'POP': '010010',
        #  'CMP': '010011', 'JMP': '010100', 'JZ': '010101', 'JE': '010101', 'JNZ': '010110', 'JNE': '010110',
        #  'JC': '010111', 'JNC': '011000', 'JA': '011001', 'JAE': '100000', 'JB': '100001', 'JBE': '100010',
        #  'READ': '100011', 'PRINT': '100100'}

# print(binaries)
# print(str(mem)[0:100])
#
# print(mem.get(cpu.pc))