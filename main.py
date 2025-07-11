#!/usr/bin/env python3

from isa import ISA
import sys

outFile = None
args = sys.argv
inFile = ""
try:
    for i in range(len(args)):
        if args[i] == "-o":
            outFile = args[i+1]
        elif args[i] != "python3" and args[i] != "./main.py" and args[i] != "main.py" and args[i - 1] != "-o":
            inFile = args[i]
except:
    print("Argumentos insuficientes. Arquivo de saída solicitado, mas não especificado.")
    exit(-1)

isa = ISA("isa.json", outFile)
isa.assemble(inFile)
# print(isa)