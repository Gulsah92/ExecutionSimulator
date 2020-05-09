#Flags ZF,CF,SF
#Register
#PC


class cpu:
    zf = False
    cf = False
    sf = False
    pc = 0
    a = '0000000000000000'
    b = '0000000000000000'
    c = '0000000000000000'
    d = '0000000000000000'
    e = '0000000000000000'
    s = (2**16) - 1

    def __str__(self):
        return 'zf=' + str(self.zf) + '\ncf=' + str(self.cf) + '\nsf=' + str(self.sf) + '\npc=' + str(self.pc) + '\na=' + str(self.a) +  '\nb=' + str(self.b) +  '\nc=' + str(self.c) + '\nd=' + str(self.d) + '\ne=' + str(self.e) + '\ns=' + str(self.s)

    # Set given value to given register
    def set(self, register, value):
        if register == 'zf':
            self.zf = value
        elif register == 'cf':
            self.cf = value
        elif register == 'sf':
            self.sf = value
        elif register == 'pc':
            self.pc = value
        elif register == 'a':
            self.a = value
        elif register == 'b':
            self.b = value
        elif register == 'c':
            self.c = value
        elif register == 'd':
            self.d = value
        elif register == 'e':
            self.e = value
        elif register == 's':
            self.s = value
        else:
            print('Invalid registry!')

    # Get value at given register
    def get(self, register):
        if register == 'zf':
            return self.zf
        elif register == 'cf':
            return self.cf
        elif register == 'sf':
            return self.sf
        elif register == 'pc':
            return self.pc
        elif register == 'a':
            return self.a
        elif register == 'b':
            return self.b
        elif register == 'c':
            return self.c
        elif register == 'd':
            return self.d
        elif register == 'e':
            return self.e
        elif register == 's':
            return self.s
        else:
            print('Invalid registry!')