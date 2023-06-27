from escalonador import *


f = open("input.txt", "r")
s = f.readline()
x = f.readline().split("|")
x1 = list(map(int, x[6].split(" ")))
proc = Processo(x[0], int(x[1]), int(x[2]), int(x[3]), int(x[4]), int(x[5]),x1)
print(proc.sequenciaMemoria)