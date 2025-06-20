#!/usr/bin/env python3

from isa import ISA
import sys

outFile = None
args = sys.argv
try:
    for i in range(len(args)):
        if args[i] == "-o":
            outFile = args[i+1]
except:
    print("Argumentos insuficientes. Arquivo de saída solicitado, mas não especificado.")
    exit(-1)

isa = ISA("isa.json", outFile)
isa.assemble("input.asm")
# print(isa)