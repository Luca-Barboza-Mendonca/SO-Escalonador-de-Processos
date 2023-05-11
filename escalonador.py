import time
import os

class Processo:
    '''Registro que guarda todas as informações de um processo'''
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
        '''Executa cada processo 1 vez pela fração de CPU, iterando sobre o vetor de processos até
        que o tempo restante de todos seja 0, para isso, guarda-se o tempo total de execução do 
        conjunto de processos quando esse conjunto é criado, quando o valor total de tempo de execução é 0,
        significa que todos os processos foram executados.'''

        vetprocessos = []
        
        file = open(self.input, "r")
        
        tmp = file.readline()
        
        i = 0
        totalCpuTimeLeft = 0
        
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
    
    def prioridade(self):
        '''Executa o processo de maior prioridade até o fim antes de executar outro processo.
        Utiliza uma fila de prioridades para manter acesso O(1) ao próximo processo que deve
        ser executado, sacrificando complexidade na construção do vetor de processos.'''
        
        vetprocessos = []

        file = open(self.input, "r")
        
        tmp = file.readline()
        
        i = 0
        totalCpuTimeLeft = 0

        while (tmp != ""):
            tmp = file.readline()
            if (tmp == ""):
                break
            x = tmp.split("|")
            processo = Processo(x[0], int(x[1]), int(x[2]), int(x[3]), int(x[4]), int(x[5]))
            vetprocessos.append(processo)
            vetprocessos = sorted(vetprocessos, key=lambda x: x.prioridade, reverse=True)
            totalCpuTimeLeft += int(x[2])
            i += 1
        
        while(totalCpuTimeLeft > 0):
            prioridade = vetprocessos[0]
            while (prioridade.tempoRestante > 0):
                print(f"Processo {prioridade.PID} executando")
                print(f"Tempo restante: {prioridade.tempoRestante}")

                if (self.cpufrac <= prioridade.tempoRestante):
                    prioridade.tempoRestante -= self.cpufrac
                    self.cpuTime += self.cpufrac
                    totalCpuTimeLeft -= self.cpufrac
                elif (self.cpufrac > prioridade.tempoRestante):
                    self.cpuTime += prioridade.tempoRestante
                    totalCpuTimeLeft -= prioridade.tempoRestante
                    prioridade.tempoRestante = 0
                time.sleep(0.01)
                os.system("cls")
            
            vetprocessos.pop(0)
        print(f"Todos os processos terminaram, tempo final de CPU {self.cpuTime}")