import json
from instrucao import Instrucao

class ISA:
    def __init__(self, isaFile, outFile):
        self.labels = {}
        self.linhas = []
        self.pc = 0
        self.registers = []
        if outFile:
            self.outFile = open(outFile, "w")
        else:
            self.outFile = None
        isa = json.load(open(isaFile))
        self.instrucoes = {}
        for instrucao in isa["subset"]:
            self.instrucoes[isa["subset"][instrucao]["mnemonic"]] = Instrucao(
                isa["subset"][instrucao]["opcode"],
                isa["subset"][instrucao]["funct3"],
                isa["subset"][instrucao]["type"],
                isa["subset"][instrucao]["paramCount"],
                isa["subset"][instrucao]["params"],
                isa["subset"][instrucao].get("funct7", -1)
            )
        self.types = isa["types"]
        self.registers = isa["registers"]

    def __str__(self):
        return f"Labels: {self.labels}\nCode: {self.linhas}\nInstruction Set: {self.instrucoes}\nTypes: {self.types}"

    def assemble(self, asmFile):
        with open(asmFile) as fp:
            self.linhas = list(map(lambda x: x.strip ("\n"), fp.readlines()))
        for index, linha in enumerate(self.linhas):
            self.linhas[index] = self.seekLabels(linha)
        self.linhas = list(filter(lambda x: x != "", self.linhas))
        self.pc = 0
        for linha in self.linhas:
            self.parseLines(linha)
        if self.outFile:
            self.outFile.close()

    def compilationError(self, message, code = -1):
        print(message)
        exit(code)
    
    def seekRegisterValue(self, name):
        for register in self.registers:
            if name == register[0]:
                return register[1]
        return None

    def parseRegister(self, token, linha):
        linhaBinario = ""
        if token[0] == "x":
            index = int(token[1:])
            if 0 <= index <= 31:
                linhaBinario = self.registers[index][1]
            else:
                self.compilationError(f"Erro na linha {linha} no PC {self.pc}. Indice do registrador incorreto")
        else:
            index = self.seekRegisterValue(token)
            if index:
                linhaBinario = index
            else:
                self.compilationError(f"Erro na linha {linha} no PC {self.pc}. Nome do registrador inválido em {token}")
        return linhaBinario

    def get_twos_complement_binary(self, number, bit_width):
        if number >= 0:
            return format(number, f'0{bit_width}b')
        else:
            abs_number = abs(number)
            mask = (1 << bit_width) - 1
            inverted_bits = abs_number ^ mask
            twos_complement_value = inverted_bits + 1
            return format(twos_complement_value, f'0{bit_width}b')
            
    def parseLines(self, linha):
        paramCount = linha.count(",") + 1
        tokens = linha.split(" ")
        if self.instrucoes[tokens[0]].paramCount == paramCount:
            tokens = list(map(lambda x: x.split(","), tokens))
            tokensTmp = []
            for i, token in enumerate(tokens):
                for j in range(len(tokens[i])):
                    tokens[i][j] = tokens[i][j].strip(")").split("(")
            for token in tokens:
                tokensTmp.extend(token)
            tokens = []
            for token in tokensTmp:
                tokens.extend(token)
            tokens = list(filter(lambda x: x != "", tokens))
            params = {}
            for index, field in enumerate(self.instrucoes[tokens[0]].params):
                if field in ["rs1", "rs2", "rd"]:
                    params[field] = self.parseRegister(tokens[index + 1], linha)
                elif field == "imm":
                    if self.instrucoes[tokens[0]].type == "B":
                        params[field] = str(self.labels[tokens[index + 1]] - self.pc)
                    else:
                        params[field] = tokens[index + 1]
                    base = 10
                    if params[field].startswith("0x"):
                        base = 16
                    elif params[field].startswith("0b"):
                        base = 2
                    try:
                        params[field] = self.get_twos_complement_binary(int(params[field], base), 13)
                    except:
                        self.compilationError(f"Erro na linha {linha} no PC {self.pc} no paramentro {params[field]}.Esperado um imediato mas foi passado outro parametro")
            params["funct3"] = self.instrucoes[tokens[0]].funct3
            params["opcode"] = self.instrucoes[tokens[0]].opcode
            try:
                params["funct7"] = self.instrucoes[tokens[0]].funct7
            except:
                pass

            linhaBinario = ""
            for field in self.types[self.instrucoes[tokens[0]].type]:
                if field.startswith("imm"):
                    values = field.strip("]").split("[")[1]
                    values = list(map(int, values.split(":")))
                    if len(values) == 1:
                        linhaBinario += params["imm"][12 - values[0]]
                    else:
                        linhaBinario += params["imm"][12 - values[0]: 13 - values[1]]
                else:
                    linhaBinario += params[field]
            if self.outFile:
                self.outFile.write(linhaBinario + "\n")
            else:
                print(linhaBinario)
        else:
            self.compilationError(f"Erro na linha {linha} no PC {self.pc}. Numero de parâmetros incorreto")
        self.pc += 4
    
    def seekLabels(self, linha):
        linha = linha.strip("\t ")
        if ":" in linha:
            linha = linha.split(":")
            self.labels[linha[0]] = self.pc
            if linha[1] != "":
                self.pc += 4
            return linha[1]
        else:
            self.pc += 4
            return linha