from escalonador import Escalonador

file = open("input.txt", "r")

line = file.readline()
tmp = line.split("|")

escalonador = Escalonador("input.txt", int(tmp[1])) 

if (tmp[0] == "alternanciaCircular"):
    escalonador.alternanciaCircular()
elif(tmp[0] == ""):
    pass