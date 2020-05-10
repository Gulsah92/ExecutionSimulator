class Memory:

    def __init__(self):
        self.memlimit = 2**16
        self.mem = [None] * (2**16)

    def __str__(self):
        return str(self.mem)

    def set(self, data, ind):
        self.mem[ind] = data[0:8]
        self.mem[ind + 1] = data[8:]

    def get(self, index):
        left_d = self.mem[index]
        right_d = self.mem[index + 1]
        return left_d + right_d

    # def get_inst(self, pc):
    #     return self.get(pc)

    def get_operand(self, pc):
        return self.mem[pc + 1] + self.mem[pc + 2]