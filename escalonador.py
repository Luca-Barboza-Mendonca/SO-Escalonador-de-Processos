import time
import os

class Processo:
    def __init__(self,nome, PID,tempoRestante, prioridade, UID, memoria):
        self.nome = nome
        self.PID = PID
        self.tempoRestante = tempoRestante
        self.prioridade = prioridade
        self.UID = UID
        self.memoria = memoria

class Escalonador:

    def __init__(self, inp, cpufrac):
        self.input = inp
        self.cpufrac = cpufrac
        self.cpuTime = 0
    
    
    def alternanciaCircular(self):
        
        vetprocessos = []
        
        file = open(self.input, "r")
        
        tmp = file.readline()
        
        totalCpuTimeLeft = 0
        i = 0
        
        while ((tmp) != ""):
            tmp = file.readline()
            if (tmp == ""):
                break
            x = tmp.split("|")
            processo = Processo(x[0], int(x[1]), int(x[2]), int(x[3]), int(x[4]), int(x[5]))
            vetprocessos.append(processo)
            totalCpuTimeLeft += int(x[2])
            i += 1
        j = 0
        
        while (totalCpuTimeLeft > 0):
            j = 0
            for j in range(0, i):
                print(f"Processo {vetprocessos[j].PID} executando")
                print(f"Tempo restante: {vetprocessos[j].tempoRestante}")
                
                if (self.cpufrac <= vetprocessos[j].tempoRestante):
                    self.cpuTime += self.cpufrac
                    vetprocessos[j].tempoRestante -= self.cpufrac
                    totalCpuTimeLeft -= self.cpufrac
                elif (self.cpufrac > vetprocessos[j].tempoRestante):
                    self.cpuTime += vetprocessos[j].tempoRestante
                    totalCpuTimeLeft -= vetprocessos[j].tempoRestante
                    vetprocessos[j].tempoRestante = 0
                

                time.sleep(0.01)
                os.system("cls")
        print(f"Todos os processos terminaram, tempo final de CPU {self.cpuTime}")
            
        
        