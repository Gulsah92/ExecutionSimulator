#Flags ZF,CF,SF
#Register
#PC

class cpu:
    zf = 0
    cf = 0
    sf = 0
    pc = 0
    a = hex(0,4)
    b = hex(0,4)
    c = hex(0,4)
    d = hex(0,4)
    e = hex(0,4)
    s = 0

    def __str__(self):
        atslist = self.__getattribute__(self)

