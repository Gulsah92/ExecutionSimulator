import Memory
import CPU
import sys
import BinReader

program_name = sys.argv[0]
file_path = sys.argv[1]

# Instantiate CPU and Memory
cpu = CPU.cpu()
mem = Memory.Memory()

# Open binary file and get binaries as list
binaries = BinReader.Binary(file_path).binl

# Register dictionary to look up char values of registers


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
            cpu.A = mem.get(cpu.pc)[2]
            cpu.pc = cpu.pc + 1
        # Todo: Add register, direct memory and indirect memory addressing modes
    # Store op
    elif mem.get(cpu.pc)[0] == '000011':
        # Register addressing
        if mem.get(cpu.pc)[1] == '01':
            cpu.set()
            cpu.pc = cpu.pc + 1


        # {'HALT': '000001', 'LOAD': '000010', 'STORE': '000011', 'ADD': '000100', 'SUB': '000101', 'INC': '000110',
        #  'DEC': '000110', 'MUL': '001000', 'DIV': '001001', 'XOR': '001010', 'AND': '001011', 'OR': '001100',
        #  'NOT': '001101', 'SHL': '001110', 'SHR': '001111', 'NOP': '010000', 'PUSH': '010001', 'POP': '010010',
        #  'CMP': '010011', 'JMP': '010100', 'JZ': '010101', 'JE': '010101', 'JNZ': '010110', 'JNE': '010110',
        #  'JC': '010111', 'JNC': '011000', 'JA': '011001', 'JAE': '100000', 'JB': '100001', 'JBE': '100010',
        #  'READ': '100011', 'PRINT': '100100'}

print(binaries)
print(str(mem)[0:100])

print(mem.get(cpu.pc))