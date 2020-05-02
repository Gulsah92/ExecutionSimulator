class Memory:

    def __init__(self):
        self.memlimit = 2**16
        self.mem = [None] * (2**16)

    def __str__(self):
        return str(self.mem)

    def set2mem(self, data, ind):
        self.mem[ind] = data

    def get(self, index):
        return self.mem[index]
