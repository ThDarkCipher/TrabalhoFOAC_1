class Instrucao:
    def __init__(self, opcode, funct3, type, paramCount, params, funct7 = - 1):
        self.opcode = opcode
        self.funct3 = funct3
        if funct7 != -1:
            self.funct7 = funct7
        self.type = type
        self.paramCount = paramCount
        self.params = params

    def __repr__(self):
        return f"[opcode: {self.opcode}, funct3: {self.funct3}, type: {self.type}]"