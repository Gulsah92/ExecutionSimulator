import Memory
import CPU
import sys
import BinReader

program_name = sys.argv[0]
file_path = sys.argv[1]

# Instantiate CPU and Memory
cp = CPU.cpu()
mem = Memory.Memory()

# Open binary file and get binaries as list
binaries = BinReader.Binary(file_path).binl

# Register dictionary to look up char values of registers
regs = {'0000000000000001': 'a', '0000000000000010': 'b', '0000000000000011': 'c', '0000000000000100': 'd',
        '0000000000000101': 'e', '0000000000000110': 's', '0000000000000000': 'pc'}

# Load instructions and data to memory starting from low address
ind = 0
for inst in binaries:
    mem.set(inst, ind)
    ind = ind + 1


# for inst in binaries:
#     mem.set(inst[0:8], ind)
#     ind = ind + 1
#     mem.set(inst[8:16], ind)
#     ind = ind + 1
#     mem.set(inst[16:], ind)
#     ind = ind + 1


# A function to convert binary represented as string to decimal
def bin2dec(binary):
    if binary[0] == '0':
        return int(binary, 2)
    elif binary[0] == '1':
        return int(binary, 2) - 2**16


# A function to convert dec to binary
def dec2bin(dec):
    if 2**15 > dec >= -(2 ** 15):
        if dec >= 0:
            return '0' + bin(dec)[2:].zfill(15)
        else:
            return '1' + bin(dec + 2**15)[2:].zfill(15)
    else:
        print('Integer overflow!!')


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
            cp.a = mem.get(cp.pc)[2]
            cp.pc = cp.pc + 1

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
            print(bin_asc)
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
            cp.a = dec2bin(a_dec_value)
            cp.pc = cp.pc + 1
            set_all_flags(a_dec_value)

        # Register addressing
        elif mem.get(cp.pc)[1] == '01':
            op_dec_value = bin2dec(cp.get(regs[mem.get(cp.pc)[2]]))
            a_dec_value = int(cp.a, 2)
            a_dec_value = op_dec_value + a_dec_value
            cp.a = dec2bin(a_dec_value)
            cp.pc = cp.pc + 1
            set_all_flags(a_dec_value)

        # Indirect memory
        elif mem.get(cp.pc)[1] == '10':
            op_dec_value = bin2dec(mem.get(bin2dec(cp.get(regs[mem.get(cp.pc)[2]]))))
            a_dec_value = int(cp.a, 2)
            a_dec_value = op_dec_value + a_dec_value
            cp.a = dec2bin(a_dec_value)
            cp.pc = cp.pc + 1
            set_all_flags(a_dec_value)

        # Direct memory
        elif mem.get(cp.pc)[1] == '11':
            op_dec_value = bin2dec(mem.get(bin2dec(mem.get(cp.pc)[2])))
            a_dec_value = int(cp.a, 2)
            a_dec_value = op_dec_value + a_dec_value
            cp.a = dec2bin(a_dec_value)
            cp.pc = cp.pc + 1
            set_all_flags(a_dec_value)

    # SUB op
    elif mem.get(cp.pc)[0] == '000101':

        # Immediate addressing
        if mem.get(cp.pc)[1] == '00':
            op_dec_value = bin2dec(mem.get(cp.pc)[2])
            a_dec_value = bin2dec(cp.a)
            a_dec_value = a_dec_value - op_dec_value
            print(a_dec_value)
            print(dec2bin(a_dec_value))
            cp.a = dec2bin(a_dec_value)
            cp.pc = cp.pc + 1
            set_all_flags(a_dec_value)

        # Register addressing
        elif mem.get(cp.pc)[1] == '01':
            op_dec_value = bin2dec(cp.get(regs[mem.get(cp.pc)[2]]))
            a_dec_value = int(cp.a, 2)
            a_dec_value = a_dec_value - op_dec_value
            cp.a = dec2bin(a_dec_value)
            cp.pc = cp.pc + 1
            set_all_flags(a_dec_value)

        # Indirect memory
        elif mem.get(cp.pc)[1] == '10':
            op_dec_value = bin2dec(mem.get(bin2dec(cp.get(regs[mem.get(cp.pc)[2]]))))
            a_dec_value = int(cp.a, 2)
            a_dec_value = a_dec_value - op_dec_value
            cp.a = dec2bin(a_dec_value)
            cp.pc = cp.pc + 1
            set_all_flags(a_dec_value)

        # Direct memory
        elif mem.get(cp.pc)[1] == '11':
            op_dec_value = bin2dec(mem.get(bin2dec(mem.get(cp.pc)[2])))
            a_dec_value = int(cp.a, 2)
            a_dec_value = a_dec_value - op_dec_value
            cp.a = dec2bin(a_dec_value)
            cp.pc = cp.pc + 1
            set_all_flags(a_dec_value)


    # MUL op
    elif mem.get(cp.pc)[0] == '001000':

        # Immediate addressing
        if mem.get(cp.pc)[1] == '00':
            op_dec_value = bin2dec(mem.get(cp.pc)[2])
            a_dec_value = bin2dec(cp.a)
            a_dec_value = op_dec_value * a_dec_value
            cp.a = bin(a_dec_value)[2:].zfill(16)
            cp.pc = cp.pc + 1
            set_all_flags(a_dec_value)
            print('mul')
            print(op_dec_value)
            print(a_dec_value)
            print(cp.a)

        # Register addressing
        elif mem.get(cp.pc)[1] == '01':
            op_dec_value = bin2dec(cp.get(regs[mem.get(cp.pc)[2]]))
            a_dec_value = int(cp.a, 2)
            a_dec_value = op_dec_value * a_dec_value
            cp.a = bin(a_dec_value)[2:].zfill(16)
            cp.pc = cp.pc + 1
            set_all_flags(a_dec_value)

        # Indirect memory
        elif mem.get(cp.pc)[1] == '10':
            op_dec_value = bin2dec(mem.get(bin2dec(cp.get(regs[mem.get(cp.pc)[2]]))))
            a_dec_value = int(cp.a, 2)
            a_dec_value = op_dec_value * a_dec_value
            cp.a = bin(a_dec_value)[2:].zfill(16)
            cp.pc = cp.pc + 1
            set_all_flags(a_dec_value)

        # Direct memory
        elif mem.get(cp.pc)[1] == '11':
            op_dec_value = bin2dec(mem.get(bin2dec(mem.get(cp.pc)[2])))
            a_dec_value = int(cp.a, 2)
            a_dec_value = op_dec_value * a_dec_value
            cp.a = bin(a_dec_value)[2:].zfill(16)
            cp.pc = cp.pc + 1
            set_all_flags(a_dec_value)

    # INC op
    elif mem.get(cp.pc)[0] == '000110':

        # Register addressing
        if mem.get(cp.pc)[1] == '01':
            op_dec_value = bin2dec(cp.get(regs[mem.get(cp.pc)[2]]))
            inc_val = op_dec_value + 1
            bin_val = bin(inc_val)[2:].zfill(16)
            cp.set(regs[mem.get(cp.pc)[2]], bin_val)
            cp.pc = cp.pc + 1
            set_all_flags(inc_val)

    # DEC op
    elif mem.get(cp.pc)[0] == '000111':

        # Register addressing
        if mem.get(cp.pc)[1] == '01':
            op_dec_value = bin2dec(cp.get(regs[mem.get(cp.pc)[2]]))
            dec_val = op_dec_value - 1
            bin_val = bin(dec_val)[2:].zfill(16)
            cp.set(regs[mem.get(cp.pc)[2]], bin_val)
            cp.pc = cp.pc + 1
            set_all_flags(dec_val)

    # DIV op
    elif mem.get(cp.pc)[0] == '001001':

        # Immediate addressing
        if mem.get(cp.pc)[1] == '00':
            op_dec_value = bin2dec(mem.get(cp.pc)[2])
            a_dec_value = bin2dec(cp.a)
            a_dec_value = a_dec_value // op_dec_value
            cp.a = bin(a_dec_value)[2:].zfill(16)
            cp.pc = cp.pc + 1
            set_all_flags(a_dec_value)

        # Register addressing
        elif mem.get(cp.pc)[1] == '01':
            op_dec_value = bin2dec(cp.get(regs[mem.get(cp.pc)[2]]))
            a_dec_value = int(cp.a, 2)
            a_dec_value = a_dec_value // op_dec_value
            cp.a = bin(a_dec_value)[2:].zfill(16)
            cp.pc = cp.pc + 1
            set_zf_sf(a_dec_value)

        # Indirect memory
        elif mem.get(cp.pc)[1] == '10':
            op_dec_value = bin2dec(mem.get(bin2dec(cp.get(regs[mem.get(cp.pc)[2]]))))
            a_dec_value = int(cp.a, 2)
            a_dec_value = a_dec_value // op_dec_value
            cp.a = bin(a_dec_value)[2:].zfill(16)
            cp.pc = cp.pc + 1
            set_zf_sf(a_dec_value)

        # Direct memory
        elif mem.get(cp.pc)[1] == '11':
            op_dec_value = bin2dec(mem.get(bin2dec(mem.get(cp.pc)[2])))
            a_dec_value = int(cp.a, 2)
            a_dec_value = a_dec_value // op_dec_value
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
            set_zf_sf(op_dec_value)

        # Indirect memory
        elif mem.get(cp.pc)[1] == '10':
            op_dec_value = bin2dec(mem.get(bin2dec(cp.get(regs[mem.get(cp.pc)[2]]))))
            not_op = bin(~op_dec_value)[2:].zfill(16)
            mem.set(not_op, bin2dec(cp.get(regs[mem.get(cp.pc)[2]])))
            cp.pc = cp.pc + 1
            set_zf_sf(op_dec_value)

        # Direct memory
        elif mem.get(cp.pc)[1] == '11':
            op_dec_value = bin2dec(mem.get(bin2dec(mem.get(cp.pc)[2])))
            not_op = bin(~op_dec_value)[2:].zfill(16)
            mem.set(not_op, bin2dec(mem.get(cp.pc)[2]))
            cp.pc = cp.pc + 1
            set_zf_sf(op_dec_value)

    # SHL op
    elif mem.get(cp.pc)[0] == '001110':

        # Register addressing
        if mem.get(cp.pc)[1] == '01':
            op_dec_value = bin2dec(cp.get(regs[mem.get(cp.pc)[2]]))
            sh_op = bin(op_dec_value << 1)[2:].zfill(16)
            cp.set(regs[mem.get(cp.pc)[2]], sh_op)
            cp.pc = cp.pc + 1
            set_all_flags(op_dec_value << 1)

    # SHR op
    elif mem.get(cp.pc)[0] == '001111':

        # Register addressing
        if mem.get(cp.pc)[1] == '01':
            op_dec_value = bin2dec(cp.get(regs[mem.get(cp.pc)[2]]))
            sh_op = bin(op_dec_value >> 1)[2:].zfill(16)
            cp.set(regs[mem.get(cp.pc)[2]], sh_op)
            cp.pc = cp.pc + 1
            set_zf_sf(op_dec_value >> 1)

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
    elif mem.get(cp.pc)[0] == '010010':

        # Register addressing
        if mem.get(cp.pc)[1] == '01':
            cp.s = cp.s + 1
            data = mem.get(cp.s)
            cp.set(regs[mem.get(cp.pc)[2]], data)
            cp.pc = cp.pc + 1

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


    # JMP op
    elif mem.get(cp.pc)[0] == '010100':

        # Immediate addressing
        if mem.get(cp.pc)[1] == '00':
            cp.pc = bin2dec(mem.get(cp.pc)[2])

    # JZ op
    elif mem.get(cp.pc)[0] == '010101':

        # Immediate addressing
        if mem.get(cp.pc)[1] == '00':
            if cp.zf:
                cp.pc = bin2dec(mem.get(cp.pc)[2])
            else:
                cp.pc = cp.pc + 1

    # JNZ op
    elif mem.get(cp.pc)[0] == '010110':

        # Immediate addressing
        if mem.get(cp.pc)[1] == '00':
            if not cp.zf:
                cp.pc = bin2dec(mem.get(cp.pc)[2])
            else:
                cp.pc = cp.pc + 1

    # JC op
    elif mem.get(cp.pc)[0] == '010101':

        # Immediate addressing
        if mem.get(cp.pc)[1] == '00':
            if cp.cf:
                cp.pc = bin2dec(mem.get(cp.pc)[2])
            else:
                cp.pc = cp.pc + 1

    # JNC op
    elif mem.get(cp.pc)[0] == '010101':

        # Immediate addressing
        if mem.get(cp.pc)[1] == '00':
            if not cp.cf:
                cp.pc = bin2dec(mem.get(cp.pc)[2])
            else:
                cp.pc = cp.pc + 1

    # JA op
    elif mem.get(cp.pc)[0] == '011001':

        # Immediate addressing
        if mem.get(cp.pc)[1] == '00':
            if not cp.cf:
                cp.pc = bin2dec(mem.get(cp.pc)[2])
            else:
                cp.pc = cp.pc + 1

    # JAE op
    elif mem.get(cp.pc)[0] == '100000':

        # Immediate addressing
        if mem.get(cp.pc)[1] == '00':
            if not cp.cf:
                cp.pc = bin2dec(mem.get(cp.pc)[2])
            else:
                cp.pc = cp.pc + 1

    # JB op
    elif mem.get(cp.pc)[0] == '100001':

        # Immediate addressing
        if mem.get(cp.pc)[1] == '00':
            if cp.cf:
                cp.pc = bin2dec(mem.get(cp.pc)[2])
            else:
                cp.pc = cp.pc + 1

    # JBE op
    elif mem.get(cp.pc)[0] == '100010':

        # Immediate addressing
        if mem.get(cp.pc)[1] == '00':
            if cp.cf or cp.zf:
                cp.pc = bin2dec(mem.get(cp.pc)[2])
            else:
                cp.pc = cp.pc + 1

    # READ
    elif mem.get(cp.pc)[0] == '100011':

        # Register addressing
        if mem.get(cp.pc)[1] == '01':
            get_char = True
            while get_char:
                r_char = input()
                try:
                    # chr(r_char).decode(int(r_char))
                    bin_char = bin(ord(r_char))[2:].zfill(16)
                    get_char = False
                except UnicodeDecodeError:
                    print('Enter an ASCII character!')
            cp.set(regs[mem.get(cp.pc)[2]], bin_char)
            cp.pc = cp.pc + 1

        # Indirect memory addressing
        if mem.get(cp.pc)[1] == '01':
            get_char = True
            while get_char:
                r_char = input()
                try:
                    # chr(r_char).decode(int(r_char))
                    bin_char = bin(ord(chr(r_char)))[2:]  # .zfill(16)
                    get_char = False
                except UnicodeDecodeError:
                    print('Enter an ASCII character!')
            mem.set(bin_char, bin2dec(cp.get(regs[mem.get(cp.pc)[2]])))
            cp.pc = cp.pc + 1

        # Direct memory addressing
        if mem.get(cp.pc)[1] == '01':
            get_char = True
            while get_char:
                r_char = input()
                try:
                    # chr(r_char).decode(int(r_char))
                    bin_char = bin(ord(r_char))[2:].zfill(16)
                    get_char = False
                except UnicodeDecodeError:
                    print('Enter an ASCII character!')
            mem.set(bin_char, bin2dec(bin2dec(mem.get(cp.pc)[2])))
            cp.pc = cp.pc + 1

    # If Label
    elif mem.get(cp.pc)[0] == '111111':
        cp.pc = cp.pc + 1
