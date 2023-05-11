from escalonador import Escalonador

file = open("input.txt", "r")

line = file.readline()
tmp = line.split("|")

escalonador = Escalonador("input.txt", int(tmp[1])) 

escalonador.alternanciaCircular()