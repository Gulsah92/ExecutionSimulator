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
for instruction in binaries:
    mem.set(instruction[:8], ind)
    ind = ind + 1
    mem.set(instruction[8:16], ind)
    ind = ind + 1
    mem.set(instruction[16:], ind)
    ind = ind + 1


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

    # Halt op
    if mem.get(cp.pc)[:6] == '000001':
        IsRunning = False

    # Load op
    elif mem.get(cp.pc)[:6] == '000010':

        # immediate addressing
        if mem.get(cp.pc)[6:8] == '00':
            cp.a = mem.get_operand(cp.pc)
            cp.pc = cp.pc + 3

        # Register addressing
        elif mem.get(cp.pc)[6:8] == '01':
            cp.a = cp.get(regs[mem.get_operand(cp.pc)])
            cp.pc = cp.pc + 3

        # Direct memory
        elif mem.get(cp.pc)[6:8] == '11':
            cp.a = mem.get(bin2dec(mem.get_operand(cp.pc)))
            cp.pc = cp.pc + 3

        # Indirect memory
        elif mem.get(cp.pc)[6:8] == '10':
            cp.a = mem.get(bin2dec(cp.get(regs[mem.get_operand(cp.pc)])))
            cp.pc = cp.pc + 3

    # Store op
    elif mem.get(cp.pc)[:6] == '000011':

        # Register addressing
        if mem.get(cp.pc)[6:8] == '01':
            cp.set(regs[mem.get_operand(cp.pc)], cp.get('a'))
            cp.pc = cp.pc + 3

        # Direct memory
        elif mem.get(cp.pc)[6:8] == '11':
            data = cp.a
            mem.set(data, bin2dec(mem.get_operand(cp.pc)))
            cp.pc = cp.pc + 3

        # Indirect memory
        elif mem.get(cp.pc)[6:8] == '10':
            data = cp.a
            mem.set(data, bin2dec(cp.get(regs[mem.get_operand(cp.pc)])))
            cp.pc = cp.pc + 3
    #  Print op
    elif mem.get(cp.pc)[:6] == '100100':
        # Immediate addressing
        if mem.get(cp.pc)[6:8] == '00':
            bin_asc = mem.get_operand(cp.pc)
            if -9 <= bin2dec(bin_asc) <= 9:
                print(chr(abs(bin2dec(bin_asc)) + 48))
                cp.pc = cp.pc + 3
            else:
                print(chr(bin2dec(bin_asc)))
                cp.pc = cp.pc + 3

        # Register addressing
        elif mem.get(cp.pc)[6:8] == '01':
            bin_asc = cp.get(regs[mem.get_operand(cp.pc)])
            if -9 <= bin2dec(bin_asc) <= 9:
                print(chr(abs(bin2dec(bin_asc)) + 48))
                cp.pc = cp.pc + 3
            else:
                print(chr(bin2dec(bin_asc)))
                cp.pc = cp.pc + 3

        # Indirect memory
        elif mem.get(cp.pc)[6:8] == '10':
            bin_asc = mem.get(bin2dec(cp.get(regs[mem.get_operand(cp.pc)])))
            if -9 <= bin2dec(bin_asc) <= 9:
                print(chr(abs(bin2dec(bin_asc)) + 48))
                cp.pc = cp.pc + 3
            else:
                print(chr(bin2dec(bin_asc)))
                cp.pc = cp.pc + 3

        # Direct memory
        elif mem.get(cp.pc)[6:8] == '11':
            bin_asc = mem.get(bin2dec(mem.get_operand(cp.pc)))
            if -9 <= bin2dec(bin_asc) <= 9:
                print(chr(abs(bin2dec(bin_asc)) + 48))
                cp.pc = cp.pc + 3
            else:
                print(chr(bin2dec(bin_asc)))
                cp.pc = cp.pc + 3
    # ADD op
    elif mem.get(cp.pc)[:6] == '000100':

        # Immediate addressing
        if mem.get(cp.pc)[6:8] == '00':
            op_dec_value = bin2dec(mem.get_operand(cp.pc))
            a_dec_value = bin2dec(cp.a)
            a_dec_value = op_dec_value + a_dec_value
            cp.a = dec2bin(a_dec_value)
            cp.pc = cp.pc + 3
            set_all_flags(a_dec_value)

        # Register addressing
        elif mem.get(cp.pc)[6:8] == '01':
            op_dec_value = bin2dec(cp.get(regs[mem.get_operand(cp.pc)]))
            a_dec_value = int(cp.a, 2)
            a_dec_value = op_dec_value + a_dec_value
            cp.a = dec2bin(a_dec_value)
            cp.pc = cp.pc + 3
            set_all_flags(a_dec_value)

        # Indirect memory
        elif mem.get(cp.pc)[6:8] == '10':
            op_dec_value = bin2dec(mem.get(bin2dec(cp.get(regs[mem.get_operand(cp.pc)]))))
            a_dec_value = int(cp.a, 2)
            a_dec_value = op_dec_value + a_dec_value
            cp.a = dec2bin(a_dec_value)
            cp.pc = cp.pc + 3
            set_all_flags(a_dec_value)

        # Direct memory
        elif mem.get(cp.pc)[6:8] == '11':
            op_dec_value = bin2dec(mem.get(bin2dec(mem.get_operand(cp.pc))))
            a_dec_value = int(cp.a, 2)
            a_dec_value = op_dec_value + a_dec_value
            cp.a = dec2bin(a_dec_value)
            cp.pc = cp.pc + 3
            set_all_flags(a_dec_value)

    # SUB op
    elif mem.get(cp.pc)[:6] == '000101':
        print(cp)

        # Immediate addressing
        if mem.get(cp.pc)[6:8] == '00':
            op_dec_value = bin2dec(mem.get_operand(cp.pc))
            a_dec_value = bin2dec(cp.a)
            a_dec_value = a_dec_value - op_dec_value
            cp.a = dec2bin(a_dec_value)
            cp.pc = cp.pc + 3
            set_all_flags(a_dec_value)

        # Register addressing
        elif mem.get(cp.pc)[6:8] == '01':
            op_dec_value = bin2dec(cp.get(regs[mem.get_operand(cp.pc)]))
            a_dec_value = int(cp.a, 2)
            a_dec_value = a_dec_value - op_dec_value
            cp.a = dec2bin(a_dec_value)
            cp.pc = cp.pc + 3
            set_all_flags(a_dec_value)

        # Indirect memory
        elif mem.get(cp.pc)[6:8] == '10':
            op_dec_value = bin2dec(mem.get(bin2dec(cp.get(regs[mem.get_operand(cp.pc)]))))
            a_dec_value = int(cp.a, 2)
            a_dec_value = a_dec_value - op_dec_value
            cp.a = dec2bin(a_dec_value)
            cp.pc = cp.pc + 3
            set_all_flags(a_dec_value)

        # Direct memory
        elif mem.get(cp.pc)[6:8] == '11':
            op_dec_value = bin2dec(mem.get(bin2dec(mem.get_operand(cp.pc))))
            a_dec_value = int(cp.a, 2)
            a_dec_value = a_dec_value - op_dec_value
            cp.a = dec2bin(a_dec_value)
            cp.pc = cp.pc + 3
            set_all_flags(a_dec_value)

    # MUL op
    elif mem.get(cp.pc)[:6] == '001000':

        # Immediate addressing
        if mem.get(cp.pc)[6:8] == '00':
            op_dec_value = bin2dec(mem.get_operand(cp.pc))
            a_dec_value = bin2dec(cp.a)
            a_dec_value = op_dec_value * a_dec_value
            cp.a = dec2bin(a_dec_value)
            cp.pc = cp.pc + 3
            set_all_flags(a_dec_value)

        # Register addressing
        elif mem.get(cp.pc)[6:8] == '01':
            op_dec_value = bin2dec(cp.get(regs[mem.get_operand(cp.pc)]))
            a_dec_value = int(cp.a, 2)
            a_dec_value = op_dec_value * a_dec_value
            cp.a = dec2bin(a_dec_value)
            cp.pc = cp.pc + 3
            set_all_flags(a_dec_value)

        # Indirect memory
        elif mem.get(cp.pc)[6:8] == '10':
            op_dec_value = bin2dec(mem.get(bin2dec(cp.get(regs[mem.get_operand(cp.pc)]))))
            a_dec_value = int(cp.a, 2)
            a_dec_value = op_dec_value * a_dec_value
            cp.a = dec2bin(a_dec_value)
            cp.pc = cp.pc + 3
            set_all_flags(a_dec_value)

        # Direct memory
        elif mem.get(cp.pc)[6:8] == '11':
            op_dec_value = bin2dec(mem.get(bin2dec(mem.get_operand(cp.pc))))
            a_dec_value = int(cp.a, 2)
            a_dec_value = op_dec_value * a_dec_value
            cp.a = dec2bin(a_dec_value)
            cp.pc = cp.pc + 3
            set_all_flags(a_dec_value)

    # INC op
    elif mem.get(cp.pc)[:6] == '000110':
        print(cp)
        # Register addressing
        if mem.get(cp.pc)[6:8] == '01':
            op_dec_value = bin2dec(cp.get(regs[mem.get_operand(cp.pc)]))
            inc_val = op_dec_value + 1
            bin_val = dec2bin(inc_val)
            cp.set(regs[mem.get_operand(cp.pc)], bin_val)
            cp.pc = cp.pc + 3
            set_all_flags(inc_val)

    # DEC op
    elif mem.get(cp.pc)[:6] == '000111':

        # Register addressing
        if mem.get(cp.pc)[6:8] == '01':
            op_dec_value = bin2dec(cp.get(regs[mem.get_operand(cp.pc)]))
            dec_val = op_dec_value - 1
            bin_val = dec2bin(dec_val)
            cp.set(regs[mem.get_operand(cp.pc)], bin_val)
            cp.pc = cp.pc + 3
            set_all_flags(dec_val)

    # DIV op
    elif mem.get(cp.pc)[:6] == '001001':

        # Immediate addressing
        if mem.get(cp.pc)[6:8] == '00':
            op_dec_value = bin2dec(mem.get_operand(cp.pc))
            a_dec_value = bin2dec(cp.a)
            a_dec_value = a_dec_value // op_dec_value
            cp.a = dec2bin(a_dec_value)
            cp.pc = cp.pc + 3
            set_all_flags(a_dec_value)

        # Register addressing
        elif mem.get(cp.pc)[6:8] == '01':
            op_dec_value = bin2dec(cp.get(regs[mem.get_operand(cp.pc)]))
            a_dec_value = int(cp.a, 2)
            a_dec_value = a_dec_value // op_dec_value
            cp.a = dec2bin(a_dec_value)
            cp.pc = cp.pc + 3
            set_zf_sf(a_dec_value)

        # Indirect memory
        elif mem.get(cp.pc)[6:8] == '10':
            op_dec_value = bin2dec(mem.get(bin2dec(cp.get(regs[mem.get_operand(cp.pc)]))))
            a_dec_value = int(cp.a, 2)
            a_dec_value = a_dec_value // op_dec_value
            cp.a = dec2bin(a_dec_value)
            cp.pc = cp.pc + 3
            set_zf_sf(a_dec_value)

        # Direct memory
        elif mem.get(cp.pc)[6:8] == '11':
            op_dec_value = bin2dec(mem.get(bin2dec(mem.get_operand(cp.pc))))
            a_dec_value = int(cp.a, 2)
            a_dec_value = a_dec_value // op_dec_value
            cp.a = dec2bin(a_dec_value)
            cp.pc = cp.pc + 3
            set_zf_sf(a_dec_value)
    # XOR op
    elif mem.get(cp.pc)[:6] == '001010':

        # Immediate addressing
        if mem.get(cp.pc)[6:8] == '00':
            op_dec_value = bin2dec(mem.get_operand(cp.pc))
            a_dec_value = bin2dec(cp.a)
            a_dec_value = op_dec_value ^ a_dec_value
            cp.a = dec2bin(a_dec_value)
            cp.pc = cp.pc + 3
            set_zf_sf(a_dec_value)

        # Register addressing
        elif mem.get(cp.pc)[6:8] == '01':
            op_dec_value = bin2dec(cp.get(regs[mem.get_operand(cp.pc)]))
            a_dec_value = int(cp.a, 2)
            a_dec_value = op_dec_value ^ a_dec_value
            cp.a = dec2bin(a_dec_value)
            cp.pc = cp.pc + 3
            set_zf_sf(a_dec_value)

        # Indirect memory
        elif mem.get(cp.pc)[6:8] == '10':
            op_dec_value = bin2dec(mem.get(bin2dec(cp.get(regs[mem.get_operand(cp.pc)]))))
            a_dec_value = int(cp.a, 2)
            a_dec_value = op_dec_value ^ a_dec_value
            cp.a = dec2bin(a_dec_value)
            cp.pc = cp.pc + 3
            set_zf_sf(a_dec_value)

        # Direct memory
        elif mem.get(cp.pc)[6:8] == '11':
            op_dec_value = bin2dec(mem.get(bin2dec(mem.get_operand(cp.pc))))
            a_dec_value = int(cp.a, 2)
            a_dec_value = op_dec_value ^ a_dec_value
            cp.a = dec2bin(a_dec_value)
            cp.pc = cp.pc + 3
            set_zf_sf(a_dec_value)

    # AND op
    elif mem.get(cp.pc)[:6] == '001011':

        # Immediate addressing
        if mem.get(cp.pc)[6:8] == '00':
            op_dec_value = bin2dec(mem.get_operand(cp.pc))
            a_dec_value = bin2dec(cp.a)
            a_dec_value = op_dec_value & a_dec_value
            cp.a = dec2bin(a_dec_value)
            cp.pc = cp.pc + 3
            set_zf_sf(a_dec_value)

        # Register addressing
        elif mem.get(cp.pc)[6:8] == '01':
            op_dec_value = bin2dec(cp.get(regs[mem.get_operand(cp.pc)]))
            a_dec_value = int(cp.a, 2)
            a_dec_value = op_dec_value & a_dec_value
            cp.a = dec2bin(a_dec_value)
            cp.pc = cp.pc + 3
            set_zf_sf(a_dec_value)

        # Indirect memory
        elif mem.get(cp.pc)[6:8] == '10':
            op_dec_value = bin2dec(mem.get(bin2dec(cp.get(regs[mem.get_operand(cp.pc)]))))
            a_dec_value = int(cp.a, 2)
            a_dec_value = op_dec_value & a_dec_value
            cp.a = dec2bin(a_dec_value)
            cp.pc = cp.pc + 3
            set_zf_sf(a_dec_value)

        # Direct memory
        elif mem.get(cp.pc)[6:8] == '11':
            op_dec_value = bin2dec(mem.get(bin2dec(mem.get_operand(cp.pc))))
            a_dec_value = int(cp.a, 2)
            a_dec_value = op_dec_value & a_dec_value
            cp.a = dec2bin(a_dec_value)
            cp.pc = cp.pc + 3
            set_zf_sf(a_dec_value)

    # OR op
    elif mem.get(cp.pc)[:6] == '001100':

        # Immediate addressing
        if mem.get(cp.pc)[6:8] == '00':
            op_dec_value = bin2dec(mem.get_operand(cp.pc))
            a_dec_value = bin2dec(cp.a)
            a_dec_value = op_dec_value | a_dec_value
            cp.a = dec2bin(a_dec_value)
            cp.pc = cp.pc + 3
            set_zf_sf(a_dec_value)

        # Register addressing
        elif mem.get(cp.pc)[6:8] == '01':
            op_dec_value = bin2dec(cp.get(regs[mem.get_operand(cp.pc)]))
            a_dec_value = int(cp.a, 2)
            a_dec_value = op_dec_value | a_dec_value
            cp.a = dec2bin(a_dec_value)
            cp.pc = cp.pc + 3
            set_zf_sf(a_dec_value)

        # Indirect memory
        elif mem.get(cp.pc)[6:8] == '10':
            op_dec_value = bin2dec(mem.get(bin2dec(cp.get(regs[mem.get_operand(cp.pc)]))))
            a_dec_value = int(cp.a, 2)
            a_dec_value = op_dec_value | a_dec_value
            cp.a = dec2bin(a_dec_value)
            cp.pc = cp.pc + 3
            set_zf_sf(a_dec_value)

        # Direct memory
        elif mem.get(cp.pc)[6:8] == '11':
            op_dec_value = bin2dec(mem.get(bin2dec(mem.get_operand(cp.pc))))
            a_dec_value = int(cp.a, 2)
            a_dec_value = op_dec_value | a_dec_value
            cp.a = dec2bin(a_dec_value)
            cp.pc = cp.pc + 3
            set_zf_sf(a_dec_value)

    # NOT op
    elif mem.get(cp.pc)[:6] == '001101':

        # Register addressing
        if mem.get(cp.pc)[6:8] == '01':
            op_dec_value = bin2dec(cp.get(regs[mem.get_operand(cp.pc)]))
            not_op = dec2bin(~op_dec_value)
            cp.set(cp.get(regs[mem.get_operand(cp.pc)]), not_op)
            cp.pc = cp.pc + 3
            set_zf_sf(~op_dec_value)

        # Indirect memory
        elif mem.get(cp.pc)[6:8] == '10':
            op_dec_value = bin2dec(mem.get(bin2dec(cp.get(regs[mem.get_operand(cp.pc)]))))
            not_op = dec2bin(~op_dec_value)
            mem.set(not_op, bin2dec(cp.get(regs[mem.get_operand(cp.pc)])))
            cp.pc = cp.pc + 3
            set_zf_sf(~op_dec_value)

        # Direct memory
        elif mem.get(cp.pc)[6:8] == '11':
            op_dec_value = bin2dec(mem.get(bin2dec(mem.get_operand(cp.pc))))
            not_op = dec2bin(~op_dec_value)
            mem.set(not_op, bin2dec(mem.get_operand(cp.pc)))
            cp.pc = cp.pc + 3
            set_zf_sf(~op_dec_value)

    # SHL op
    elif mem.get(cp.pc)[:6] == '001110':

        # Register addressing
        if mem.get(cp.pc)[6:8] == '01':
            op_dec_value = bin2dec(cp.get(regs[mem.get_operand(cp.pc)]))
            sh_op = dec2bin(op_dec_value << 1)
            cp.set(regs[mem.get_operand(cp.pc)], sh_op)
            cp.pc = cp.pc + 3
            set_all_flags(op_dec_value << 1)

    # SHR op
    elif mem.get(cp.pc)[:6] == '001111':

        # Register addressing
        if mem.get(cp.pc)[6:8] == '01':
            op_dec_value = bin2dec(cp.get(regs[mem.get_operand(cp.pc)]))
            sh_op = dec2bin(op_dec_value >> 1)
            cp.set(regs[mem.get_operand(cp.pc)], sh_op)
            cp.pc = cp.pc + 3
            set_zf_sf(op_dec_value >> 1)

    # NOP op
    elif mem.get(cp.pc)[:6] == '010000':
        cp.pc = cp.pc + 3

    # PUSH op
    elif mem.get(cp.pc)[:6] == '010001':

        # Register addressing
        if mem.get(cp.pc)[6:8] == '01':
            data_l = cp.get(regs[mem.get_operand(cp.pc)])[0:4]
            data_r = cp.get(regs[mem.get_operand(cp.pc)])[4:]
            mem.set(data_l + data_r, cp.s-1)
            cp.pc = cp.pc + 3
            cp.s = cp.s - 2

    # Pop op
    elif mem.get(cp.pc)[:6] == '010010':

        # Register addressing
        if mem.get(cp.pc)[6:8] == '01':
            cp.s = cp.s + 2
            data = mem.get(cp.s - 1)
            cp.set(regs[mem.get_operand(cp.pc)], data)
            cp.pc = cp.pc + 3

    # CMP op
    elif mem.get(cp.pc)[:6] == '010011':

        # Immediate addressing
        if mem.get(cp.pc)[6:8] == '00':
            dec_op = bin2dec(mem.get_operand(cp.pc))
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
            cp.pc = cp.pc + 3

        # Register addressing
        elif mem.get(cp.pc)[6:8] == '01':
            dec_op = bin2dec(cp.get(regs[(mem.get_operand(cp.pc))]))
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
            cp.pc = cp.pc + 3

        # Indirect memory addressing
        elif mem.get(cp.pc)[6:8] == '10':
            dec_op = bin2dec(mem.get(bin2dec(cp.get(regs[(mem.get_operand(cp.pc))]))))
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
            cp.pc = cp.pc + 3

        # Direct memory addressing
        elif mem.get(cp.pc)[6:8] == '11':
            dec_op = bin2dec(mem.get(bin2dec(mem.get_operand(cp.pc))))
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
            cp.pc = cp.pc + 3

    # JMP op
    elif mem.get(cp.pc)[:6] == '010100':

        # Immediate addressing
        if mem.get(cp.pc)[6:8] == '00':
            cp.pc = bin2dec(mem.get_operand(cp.pc))

    # JZ op
    elif mem.get(cp.pc)[:6] == '010101':

        # Immediate addressing
        if mem.get(cp.pc)[6:8] == '00':
            if cp.zf:
                cp.pc = bin2dec(mem.get_operand(cp.pc))
            else:
                cp.pc = cp.pc + 3

    # JNZ op
    elif mem.get(cp.pc)[:6] == '010110':
        # Immediate addressing
        if mem.get(cp.pc)[6:8] == '00':
            if not cp.zf:
                cp.pc = bin2dec(mem.get_operand(cp.pc))
            else:
                cp.pc = cp.pc + 3

    # JC op
    elif mem.get(cp.pc)[:6] == '010101':

        # Immediate addressing
        if mem.get(cp.pc)[6:8] == '00':
            if cp.cf:
                cp.pc = bin2dec(mem.get_operand(cp.pc))
            else:
                cp.pc = cp.pc + 3

    # JNC op
    elif mem.get(cp.pc)[:6] == '010101':

        # Immediate addressing
        if mem.get(cp.pc)[6:8] == '00':
            if not cp.cf:
                cp.pc = bin2dec(mem.get_operand(cp.pc))
            else:
                cp.pc = cp.pc + 3

    # JA op
    elif mem.get(cp.pc)[:6] == '011001':

        # Immediate addressing
        if mem.get(cp.pc)[6:8] == '00':
            if cp.cf:
                cp.pc = bin2dec(mem.get_operand(cp.pc))
            else:
                cp.pc = cp.pc + 3

    # JAE op
    elif mem.get(cp.pc)[:6] == '100000':

        # Immediate addressing
        if mem.get(cp.pc)[6:8] == '00':
            print(cp)
            if cp.cf or cp.zf:
                cp.pc = bin2dec(mem.get_operand(cp.pc))
            else:
                cp.pc = cp.pc + 3

    # JB op
    elif mem.get(cp.pc)[:6] == '100001':

        # Immediate addressing
        if mem.get(cp.pc)[6:8] == '00':
            if not cp.cf:
                cp.pc = bin2dec(mem.get_operand(cp.pc))
            else:
                cp.pc = cp.pc + 3

    # JBE op
    elif mem.get(cp.pc)[:6] == '100010':

        # Immediate addressing
        if mem.get(cp.pc)[6:8] == '00':
            if not cp.cf or cp.zf:
                cp.pc = bin2dec(mem.get_operand(cp.pc))
            else:
                cp.pc = cp.pc + 3

    # READ
    elif mem.get(cp.pc)[:6] == '100011':

        # Register addressing
        if mem.get(cp.pc)[6:8] == '01':
            get_char = True
            while get_char:
                r_char = input()
                try:
                    # chr(r_char).decode(int(r_char))
                    bin_char = dec2bin(ord(r_char))
                    cp.set(regs[mem.get_operand(cp.pc)], bin_char)
                    get_char = False
                except UnicodeDecodeError:
                    print('Enter an ASCII character!')
            cp.pc = cp.pc + 3

        # Indirect memory addressing
        if mem.get(cp.pc)[6:8] == '10':
            get_char = True
            while get_char:
                r_char = input()
                try:
                    # chr(r_char).decode(int(r_char))
                    bin_char = dec2bin(ord(r_char))
                    mem.set(bin_char, bin2dec(cp.get(regs[mem.get_operand(cp.pc)])))
                    get_char = False
                except UnicodeDecodeError:
                    print('Enter an ASCII character!')
            cp.pc = cp.pc + 3

        # Direct memory addressing
        if mem.get(cp.pc)[6:8] == '11':
            get_char = True
            while get_char:
                r_char = input('Enter a character: ')
                try:
                    # chr(r_char).decode(int(r_char))
                    bin_char = dec2bin(ord(r_char))
                    mem.set(bin_char, bin2dec(mem.get_operand(cp.pc)))
                    get_char = False
                except UnicodeDecodeError:
                    print('Enter an ASCII character!')
            cp.pc = cp.pc + 3

