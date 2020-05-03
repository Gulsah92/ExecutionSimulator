import Memory
import CPU
import sys
import BinReader

# program_name = sys.argv[0]
# file_path = sys.argv[1]

# Instantiate CPU and Memory
cp = CPU.cpu()
mem = Memory.Memory()

# Open binary file and get binaries as list
binaries = BinReader.Binary('test.bin').binl

# Register dictionary to look up char values of registers
regs = {'0000000000000001': 'a', '0000000000000010': 'b', '0000000000000011': 'c', '0000000000000100': 'd',
        '0000000000000101': 'e', '0000000000000110': 's', '0000000000000000': 'pc'}

# Load instructions and data to memory starting from low address
ind = 0
for inst in binaries:
    mem.set(inst, ind)
    ind = ind + 1


# A function to convert binary represented as string to decimal
def bin2dec(binary):
    return int(binary, 2)


# A function to set all CPU flags
def set_all_flags(value):
    if value == 0:
        cp.zf = True
    if value < 0:
        cp.sf = True
    if value > 65535:
        cp.cf = True


# A function to set SF and ZF CPU flags
def set_zf_sf(value):
    if value == 0:
        cp.zf = True
    if value < 0:
        cp.sf = True


# Run instructions using registers and memory
IsRunning = True
while IsRunning:
    # print(mem.get(cp.pc))

    # Halt op
    if mem.get(cp.pc)[0] == '000001':
        IsRunning = False

    # Load op
    elif mem.get(cp.pc)[0] == '000010':

        # immediate addressing
        if mem.get(cp.pc)[1] == '00':
            # print(mem.get(cp.pc)[2])
            cp.a = mem.get(cp.pc)[2]
            # print(cp)
            cp.pc = cp.pc + 1
            # print(cp)

        # Register addressing
        elif mem.get(cp.pc)[1] == '01':
            cp.a = cp.get(regs[mem.get(cp.pc)[2]])
            cp.pc = cp.pc + 1

        # Direct memory
        elif mem.get(cp.pc)[1] == '11':
            cp.a = mem.get(int(mem.get(cp.pc)[2], 2))
            cp.pc = cp.pc + 1

        # Indirect memory
        elif mem.get(cp.pc)[1] == '10':
            cp.a = mem.get(cp.get(int(regs[mem.get(cp.pc)[2]], 2)))
            cp.pc = cp.pc + 1

    # Store op
    elif mem.get(cp.pc)[0] == '000011':

        # Register addressing
        if mem.get(cp.pc)[1] == '01':
            cp.set(regs[mem.get(cp.pc)[2]], cp.get('a'))
            cp.pc = cp.pc + 1
            # print(cp)

        # Direct memory
        elif mem.get(cp.pc)[1] == '11':
            data = cp.a
            mem.set(data, bin2dec(mem.get(cp.pc)[2]))
            cp.pc = cp.pc + 1

        # Indirect memory
        elif mem.get(cp.pc)[1] == '10':
            data = cp.a
            mem.set(data, bin2dec(cp.get(regs[mem.get(cp.pc)[2]])))
            cp.pc = cp.pc + 1
    #  Print op
    elif mem.get(cp.pc)[0] == '100100':
        # Immediate addressing
        if mem.get(cp.pc)[1] == '00':
            bin_asc = mem.get(cp.pc)[2]
            if bin_asc[0:8] == '00000000':
                print(chr(bin2dec(bin_asc)))
                cp.pc = cp.pc + 1
            else:
                print(chr(bin2dec(bin_asc[8:])) + chr(bin2dec(bin_asc[:8])))
                cp.pc = cp.pc + 1

        # Register addressing
        elif mem.get(cp.pc)[1] == '01':
            bin_asc = cp.get(regs[mem.get(cp.pc)[2]])
            if bin_asc[0:8] == '00000000':
                print(chr(bin2dec(bin_asc)))
                cp.pc = cp.pc + 1
            else:
                print(chr(bin2dec(bin_asc[8:])) + chr(bin2dec(bin_asc[:8])))
                cp.pc = cp.pc + 1

        # Indirect memory
        elif mem.get(cp.pc)[1] == '10':
            bin_asc = mem.get(bin2dec(cp.get(regs[mem.get(cp.pc)[2]])))
            if bin_asc[0:8] == '00000000':
                print(chr(bin2dec(bin_asc)))
                cp.pc = cp.pc + 1
            else:
                print(chr(bin2dec(bin_asc[8:])) + chr(bin2dec(bin_asc[:8])))
                cp.pc = cp.pc + 1

        # Direct memory
        elif mem.get(cp.pc)[1] == '11':
            bin_asc = mem.get(bin2dec(mem.get(cp.pc)[2]))
            if bin_asc[0:8] == '00000000':
                print(chr(bin2dec(bin_asc)))
                cp.pc = cp.pc + 1
            else:
                print(chr(bin2dec(bin_asc[8:])) + chr(bin2dec(bin_asc[:8])))
                cp.pc = cp.pc + 1
    # ADD op
    elif mem.get(cp.pc)[0] == '000100':

        # Immediate addressing
        if mem.get(cp.pc)[1] == '00':
            op_dec_value = bin2dec(mem.get(cp.pc)[2])
            a_dec_value = bin2dec(cp.a)
            a_dec_value = op_dec_value + a_dec_value
            cp.a = bin(a_dec_value)[2:].zfill(16)
            cp.pc = cp.pc + 1
            set_all_flags(a_dec_value)

        # Register addressing
        elif mem.get(cp.pc)[1] == '01':
            op_dec_value = bin2dec(cp.get(regs[mem.get(cp.pc)[2]]))
            a_dec_value = int(cp.a, 2)
            a_dec_value = op_dec_value + a_dec_value
            cp.a = bin(a_dec_value)[2:].zfill(16)
            cp.pc = cp.pc + 1
            set_all_flags(a_dec_value)

        # Indirect memory
        elif mem.get(cp.pc)[1] == '10':
            op_dec_value = bin2dec(mem.get(bin2dec(cp.get(regs[mem.get(cp.pc)[2]]))))
            a_dec_value = int(cp.a, 2)
            a_dec_value = op_dec_value + a_dec_value
            cp.a = bin(a_dec_value)[2:].zfill(16)
            cp.pc = cp.pc + 1
            set_all_flags(a_dec_value)

        # Direct memory
        elif mem.get(cp.pc)[1] == '11':
            op_dec_value = bin2dec(mem.get(bin2dec(mem.get(cp.pc)[2])))
            a_dec_value = int(cp.a, 2)
            a_dec_value = op_dec_value + a_dec_value
            cp.a = bin(a_dec_value)[2:].zfill(16)
            cp.pc = cp.pc + 1
            set_all_flags(a_dec_value)

    # Todo: GULSAH sub, mul, inc, dec instructions

    # DIV op
    elif mem.get(cp.pc)[0] == '001001':

        # Immediate addressing
        if mem.get(cp.pc)[1] == '00':
            op_dec_value = bin2dec(mem.get(cp.pc)[2])
            a_dec_value = bin2dec(cp.a)
            a_dec_value = op_dec_value // a_dec_value
            cp.a = bin(a_dec_value)[2:].zfill(16)
            cp.pc = cp.pc + 1
            set_all_flags(a_dec_value)

        # Register addressing
        elif mem.get(cp.pc)[1] == '01':
            op_dec_value = bin2dec(cp.get(regs[mem.get(cp.pc)[2]]))
            a_dec_value = int(cp.a, 2)
            a_dec_value = op_dec_value // a_dec_value
            cp.a = bin(a_dec_value)[2:].zfill(16)
            cp.pc = cp.pc + 1
            set_zf_sf(a_dec_value)

        # Indirect memory
        elif mem.get(cp.pc)[1] == '10':
            op_dec_value = bin2dec(mem.get(bin2dec(cp.get(regs[mem.get(cp.pc)[2]]))))
            a_dec_value = int(cp.a, 2)
            a_dec_value = op_dec_value // a_dec_value
            cp.a = bin(a_dec_value)[2:].zfill(16)
            cp.pc = cp.pc + 1
            set_zf_sf(a_dec_value)

        # Direct memory
        elif mem.get(cp.pc)[1] == '11':
            op_dec_value = bin2dec(mem.get(bin2dec(mem.get(cp.pc)[2])))
            a_dec_value = int(cp.a, 2)
            a_dec_value = op_dec_value // a_dec_value
            cp.a = bin(a_dec_value)[2:].zfill(16)
            cp.pc = cp.pc + 1
            set_zf_sf(a_dec_value)
    # XOR op
    elif mem.get(cp.pc)[0] == '001010':

        # Immediate addressing
        if mem.get(cp.pc)[1] == '00':
            op_dec_value = bin2dec(mem.get(cp.pc)[2])
            a_dec_value = bin2dec(cp.a)
            a_dec_value = op_dec_value ^ a_dec_value
            cp.a = bin(a_dec_value)[2:].zfill(16)
            cp.pc = cp.pc + 1
            set_zf_sf(a_dec_value)

        # Register addressing
        elif mem.get(cp.pc)[1] == '01':
            op_dec_value = bin2dec(cp.get(regs[mem.get(cp.pc)[2]]))
            a_dec_value = int(cp.a, 2)
            a_dec_value = op_dec_value ^ a_dec_value
            cp.a = bin(a_dec_value)[2:].zfill(16)
            cp.pc = cp.pc + 1
            set_zf_sf(a_dec_value)

        # Indirect memory
        elif mem.get(cp.pc)[1] == '10':
            op_dec_value = bin2dec(mem.get(bin2dec(cp.get(regs[mem.get(cp.pc)[2]]))))
            a_dec_value = int(cp.a, 2)
            a_dec_value = op_dec_value ^ a_dec_value
            cp.a = bin(a_dec_value)[2:].zfill(16)
            cp.pc = cp.pc + 1
            set_zf_sf(a_dec_value)

        # Direct memory
        elif mem.get(cp.pc)[1] == '11':
            op_dec_value = bin2dec(mem.get(bin2dec(mem.get(cp.pc)[2])))
            a_dec_value = int(cp.a, 2)
            a_dec_value = op_dec_value ^ a_dec_value
            cp.a = bin(a_dec_value)[2:].zfill(16)
            cp.pc = cp.pc + 1
            set_zf_sf(a_dec_value)

    # AND op
    elif mem.get(cp.pc)[0] == '001011':

        # Immediate addressing
        if mem.get(cp.pc)[1] == '00':
            op_dec_value = bin2dec(mem.get(cp.pc)[2])
            a_dec_value = bin2dec(cp.a)
            a_dec_value = op_dec_value & a_dec_value
            cp.a = bin(a_dec_value)[2:].zfill(16)
            cp.pc = cp.pc + 1
            set_zf_sf(a_dec_value)

        # Register addressing
        elif mem.get(cp.pc)[1] == '01':
            op_dec_value = bin2dec(cp.get(regs[mem.get(cp.pc)[2]]))
            a_dec_value = int(cp.a, 2)
            a_dec_value = op_dec_value & a_dec_value
            cp.a = bin(a_dec_value)[2:].zfill(16)
            cp.pc = cp.pc + 1
            set_zf_sf(a_dec_value)

        # Indirect memory
        elif mem.get(cp.pc)[1] == '10':
            op_dec_value = bin2dec(mem.get(bin2dec(cp.get(regs[mem.get(cp.pc)[2]]))))
            a_dec_value = int(cp.a, 2)
            a_dec_value = op_dec_value & a_dec_value
            cp.a = bin(a_dec_value)[2:].zfill(16)
            cp.pc = cp.pc + 1
            set_zf_sf(a_dec_value)

        # Direct memory
        elif mem.get(cp.pc)[1] == '11':
            op_dec_value = bin2dec(mem.get(bin2dec(mem.get(cp.pc)[2])))
            a_dec_value = int(cp.a, 2)
            a_dec_value = op_dec_value & a_dec_value
            cp.a = bin(a_dec_value)[2:].zfill(16)
            cp.pc = cp.pc + 1
            set_zf_sf(a_dec_value)

    # OR op
    elif mem.get(cp.pc)[0] == '001100':

        # Immediate addressing
        if mem.get(cp.pc)[1] == '00':
            op_dec_value = bin2dec(mem.get(cp.pc)[2])
            a_dec_value = bin2dec(cp.a)
            a_dec_value = op_dec_value | a_dec_value
            cp.a = bin(a_dec_value)[2:].zfill(16)
            cp.pc = cp.pc + 1
            set_zf_sf(a_dec_value)

        # Register addressing
        elif mem.get(cp.pc)[1] == '01':
            op_dec_value = bin2dec(cp.get(regs[mem.get(cp.pc)[2]]))
            a_dec_value = int(cp.a, 2)
            a_dec_value = op_dec_value | a_dec_value
            cp.a = bin(a_dec_value)[2:].zfill(16)
            cp.pc = cp.pc + 1
            set_zf_sf(a_dec_value)

        # Indirect memory
        elif mem.get(cp.pc)[1] == '10':
            op_dec_value = bin2dec(mem.get(bin2dec(cp.get(regs[mem.get(cp.pc)[2]]))))
            a_dec_value = int(cp.a, 2)
            a_dec_value = op_dec_value | a_dec_value
            cp.a = bin(a_dec_value)[2:].zfill(16)
            cp.pc = cp.pc + 1
            set_zf_sf(a_dec_value)

        # Direct memory
        elif mem.get(cp.pc)[1] == '11':
            op_dec_value = bin2dec(mem.get(bin2dec(mem.get(cp.pc)[2])))
            a_dec_value = int(cp.a, 2)
            a_dec_value = op_dec_value | a_dec_value
            cp.a = bin(a_dec_value)[2:].zfill(16)
            cp.pc = cp.pc + 1
            set_zf_sf(a_dec_value)

    # NOT op
    elif mem.get(cp.pc)[0] == '001101':

        # !!!! Burası cok saçma bunu hocaya sormalı
        # Immediate addressing
        if mem.get(cp.pc)[1] == '00':
            op_dec_value = bin2dec(mem.get(cp.pc)[2])
            a_dec_value = bin2dec(cp.a)
            a_dec_value = ~a_dec_value
            cp.a = bin(a_dec_value)[2:].zfill(16)
            cp.pc = cp.pc + 1
            set_zf_sf(a_dec_value)

        # Register addressing
        elif mem.get(cp.pc)[1] == '01':
            op_dec_value = bin2dec(cp.get(regs[mem.get(cp.pc)[2]]))
            not_op = bin(~op_dec_value)[2:].zfill(16)
            cp.set(cp.get(regs[mem.get(cp.pc)[2]]), not_op)
            cp.pc = cp.pc + 1
            set_zf_sf(a_dec_value)

        # Indirect memory
        elif mem.get(cp.pc)[1] == '10':
            op_dec_value = bin2dec(mem.get(bin2dec(cp.get(regs[mem.get(cp.pc)[2]]))))
            not_op = bin(~op_dec_value)[2:].zfill(16)
            mem.set(not_op, bin2dec(cp.get(regs[mem.get(cp.pc)[2]])))
            cp.pc = cp.pc + 1
            set_zf_sf(a_dec_value)

        # Direct memory
        elif mem.get(cp.pc)[1] == '11':
            op_dec_value = bin2dec(mem.get(bin2dec(mem.get(cp.pc)[2])))
            not_op = bin(~op_dec_value)[2:].zfill(16)
            mem.set(not_op, bin2dec(mem.get(cp.pc)[2]))
            cp.pc = cp.pc + 1
            set_zf_sf(a_dec_value)

    # SHL op
    elif mem.get(cp.pc)[0] == '001110':

        # Register addressing
        if mem.get(cp.pc)[1] == '01':
            op_dec_value = bin2dec(cp.get(regs[mem.get(cp.pc)[2]]))
            sh_op = bin(op_dec_value << 1)[2:].zfill(16)
            cp.set(cp.get(regs[mem.get(cp.pc)[2]]), sh_op)
            cp.pc = cp.pc + 1
            set_all_flags(a_dec_value)

    # SHR op
    elif mem.get(cp.pc)[0] == '001111':

        # Register addressing
        if mem.get(cp.pc)[1] == '01':
            op_dec_value = bin2dec(cp.get(regs[mem.get(cp.pc)[2]]))
            sh_op = bin(op_dec_value >> 1)[2:].zfill(16)
            cp.set(cp.get(regs[mem.get(cp.pc)[2]]), sh_op)
            cp.pc = cp.pc + 1
            set_zf_sf(a_dec_value)

    # NOP op
    elif mem.get(cp.pc)[0] == '010000':
        cp.pc = cp.pc + 1

    # PUSH op
    elif mem.get(cp.pc)[0] == '010001':

        # Register addressing
        if mem.get(cp.pc)[1] == '01':
            data = cp.get(regs[mem.get(cp.pc)[2]])
            mem.set(data, cp.s)
            cp.pc = cp.pc + 1
            cp.s = cp.s - 1

    # Pop op
    elif mem.get(cp.pc)[0] == '010001':

        # Register addressing
        if mem.get(cp.pc)[1] == '01':
            data = mem.get(cp.s)
            cp.a = data
            cp.pc = cp.pc + 1
            cp.s = cp.s + 1

    # CMP op
    elif mem.get(cp.pc)[0] == '010011':

        # Immediate addressing
        if mem.get(cp.pc)[1] == '00':
            dec_op = bin2dec(mem.get(cp.pc)[2])
            dec_a = bin2dec(cp.a)
            if dec_op < dec_a:
                cp.sf = False
                cp.zf = False
                cp.cf = False
            elif dec_op == dec_a:
                cp.sf = False
                cp.zf = True
                cp.cf = False
            elif dec_op > dec_a:
                cp.sf = True
                cp.zf = False
                cp.cf = True
            cp.pc = cp.pc + 1

        # Register addressing
        elif mem.get(cp.pc)[1] == '00':
            dec_op = bin2dec(cp.get(regs[(mem.get(cp.pc)[2])]))
            dec_a = bin2dec(cp.a)
            if dec_op < dec_a:
                cp.sf = False
                cp.zf = False
                cp.cf = False
            elif dec_op == dec_a:
                cp.sf = False
                cp.zf = True
                cp.cf = False
            elif dec_op > dec_a:
                cp.sf = True
                cp.zf = False
                cp.cf = True
            cp.pc = cp.pc + 1

        # Indirect memory addressing
        elif mem.get(cp.pc)[1] == '00':
            dec_op = bin2dec(mem.get(bin2dec(cp.get(regs[(mem.get(cp.pc)[2])]))))
            dec_a = bin2dec(cp.a)
            if dec_op < dec_a:
                cp.sf = False
                cp.zf = False
                cp.cf = False
            elif dec_op == dec_a:
                cp.sf = False
                cp.zf = True
                cp.cf = False
            elif dec_op > dec_a:
                cp.sf = True
                cp.zf = False
                cp.cf = True
            cp.pc = cp.pc + 1

        # Direct memory addressing
        elif mem.get(cp.pc)[1] == '00':
            dec_op = bin2dec(mem.get(bin2dec(mem.get(cp.pc)[2])))
            dec_a = bin2dec(cp.a)
            if dec_op < dec_a:
                cp.sf = False
                cp.zf = False
                cp.cf = False
            elif dec_op == dec_a:
                cp.sf = False
                cp.zf = True
                cp.cf = False
            elif dec_op > dec_a:
                cp.sf = True
                cp.zf = False
                cp.cf = True
            cp.pc = cp.pc + 1

        # {'HALT': '000001', 'LOAD': '000010', 'STORE': '000011', 'ADD': '000100', 'SUB': '000101', 'INC': '000110',
        #  'DEC': '000110', 'MUL': '001000', 'DIV': '001001', 'XOR': '001010', 'AND': '001011', 'OR': '001100',
        #  'NOT': '001101', 'SHL': '001110', 'SHR': '001111', 'NOP': '010000', 'PUSH': '010001', 'POP': '010010',

        #  'CMP': '010011', 'JMP': '010100', 'JZ': '010101', 'JE': '010101', 'JNZ': '010110', 'JNE': '010110',
        #  'JC': '010111', 'JNC': '011000', 'JA': '011001', 'JAE': '100000', 'JB': '100001', 'JBE': '100010',
        #  'READ': '100011', 'PRINT': '100100'}

# print(binaries)
# print(str(mem)[0:100])
#
# print(mem.get(cp.pc))
