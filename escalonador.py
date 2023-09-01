import time
import os
import sys
import random
from copy import deepcopy
from random import choices
from sortedcontainers import SortedKeyList
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QPushButton, QLabel, QVBoxLayout, QWidget
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtGui import QFont

from gerenciadorDeMemoria import *
from interface import *
from gerenciadorES import *
from gerenciadorES import initDispositivo
from util import makeInput

memPol = None # Política de memória, local ou global
tamMem = None # Tamanho da memória
tamPag = None # Tamanho das página e molduras
percAloc = None # Percentual máximo de memória que um processo pode ter na memória principal
acessosPorCiclo = None # Acessos á memória por ciclo de cpu

vetprocessos = None
totalCpuTimeLeft = 0
vetpesos = [] # Só para o algoritmo de loteria
algo = 1

tempo = 0

class Processo:
    '''Registro que guarda todas as informações de um processo'''
    def __init__(self,nome, PID,tempoRestante, prioridade, UID, memoria, sequenciaMemoria, chance):
        self.nome = nome
        self.PID = PID
        self.tempoRestante = tempoRestante
        self.prioridade = prioridade
        self.UID = UID
        self.memoria = memoria
        self.sequenciaMemoria = sequenciaMemoria
        self.tempoRecebido = 0
        self.chanceBloquear = chance
        self.pronto = True # True para pronto, False para bloqueado

def initProcessos(modo):
    '''criar um vetor global para guardar os processos, esse deve ser atualizado pelo input do usuário.
    Deve receber um parâmetro modo que específica a estrutura do vetor de processos, correspondente a cada algoritmo de 
    escalonamento.'''

    global vetprocessos
    global totalCpuTimeLeft

    if modo == 1:

        # Alternância circular
        vetprocessos = []

        file = open("input.txt", "r")
        tmp = "placeholder"
        tmp = file.readline()
        tmp = tmp.split("|")
        tmp[7] = tmp[7].replace("\n", '')

        for i in range(0, int(tmp[7])):
            tmp = file.readline()

        i = 0

        while ((tmp) != ""):
            tmp = file.readline()
            if (tmp == ""):
                break
            x = tmp.split("|")
            processo = Processo(x[0], int(x[1]), int(x[2]), int(x[3]), int(x[4]), int(x[5]), list(map(int, x[6].split(" "))), int(x[7]))
            vetprocessos.append(processo)
            totalCpuTimeLeft += int(x[2])
            i += 1
        
        file = open("input.txt", "w")
        file.write("")
        file.close()
    elif modo == 2:

        # Prioridade
        
        vetprocessos = []
        tmp = "placeholder"
        file = open("input.txt", "r")
        tmp = file.readline()
        tmp = tmp.split("|")
        tmp[7] = tmp[7].replace("\n", '')

        for i in range(0, int(tmp[7])):
            tmp = file.readline()

        i = 0
        while (tmp != ""):
            tmp = file.readline()
            if (tmp == ""):
                break
            x = tmp.split("|")
            processo = Processo(x[0], int(x[1]), int(x[2]), int(x[3]), int(x[4]), int(x[5]), list(map(int, x[6].split(" "))), int(x[7]))
            vetprocessos.append(processo)
            vetprocessos = sorted(vetprocessos, key=lambda x: x.prioridade, reverse=True)
            totalCpuTimeLeft += int(x[2])
            i += 1
        file = open("input.txt", "w")
        file.write("")
        file.close()
    elif modo == 3:

        global vetpesos
        vetprocessos = []
        tmp = "placeholder"
        file = open("input.txt", "r")
        tmp = file.readline()
        tmp = tmp.split("|")
        tmp[7] = tmp[7].replace("\n", '')

        for i in range(0, int(tmp[7])):
            tmp = file.readline()
        
        i = 0
        totalCpuTimeLeft = 0

        while ((tmp) != ""):
            tmp = file.readline()
            if (tmp == ""):
                break
            x = tmp.split("|")
            processo = Processo(x[0], int(x[1]), int(x[2]), int(x[3]), int(x[4]), int(x[5]), list(map(int, x[6].split(" "))), int(x[7]))
            vetprocessos.append(processo)
            vetpesos.append(int(x[3]))  # guarda o peso do processo i na posição i
            totalCpuTimeLeft += int(x[2])
            i += 1
        file = open("input.txt", "w")
        file.write("")
        file.close()
    
    elif modo == 4:
        tmp = "placeholder"
        vetprocessos = SortedKeyList(key=lambda x: x.tempoRecebido)
        
        file = makeInput()
        
        i = 0
        totalCpuTimeLeft = 0

        while ((tmp) != ""):
            tmp = file.readline()
            if (tmp == ""):
                break
            x = tmp.split("|")
            processo = Processo(x[0], int(x[1]), int(x[2]), int(x[3]), int(x[4]), int(x[5]), list(map(int, x[6].split(" "))), int(x[7]))
            vetprocessos.add(processo)
            totalCpuTimeLeft += int(x[2])
            i += 1
        file = open("input.txt", "w")
        file.write("")
        file.close()

def addProcesso(proc):
    '''Adicionar um processo específicado pelo usuário ao vetor global'''
    x = proc.split("|")
    processo = Processo(x[0], int(x[1]), int(x[2]), int(x[3]), int(x[4]), int(x[5]), list(map(int, x[6].split(" "))), int(x[7]))
    global vetprocessos
    global totalCpuTimeLeft

    global algo
    if algo == 1:
        vetprocessos.append(processo)
    elif algo == 2:
        vetprocessos.append(processo)
        vetprocessos = sorted(vetprocessos, key=lambda x: x.prioridade, reverse=True)
    elif algo == 3:
        global vetpesos
        vetpesos.append(int(x[3]))
        vetprocessos.append(processo)
    elif algo == 4:
        vetprocessos.add(processo)
    
    totalCpuTimeLeft += int(x[2])


class Escalonador(QThread):
    '''Classe escalonador que roda como um thread, permitindo paralelismo na interface gráfica. Muito do código entre os diferentes algoritmos é repetido, isso é proposital
    para garantir modularidade entre os métodos de escalonamento, caso trabalhos futuros tenham o escopo de expandir essa implementação.'''
    text_changed = pyqtSignal(str)

    def __init__(self, inp, test=False):
        self.input = inp
        self.cpufrac = 0
        self.cpuTime = 0
        self.test = test # Só para desabilitar o sleep
        self.gerente = None
        QThread.__init__(self)
    
    def __del__(self):
        self.wait()
    
    
    def alternanciaCircular(self):
        '''Executa cada processo 1 vez pela fração de CPU, iterando sobre o vetor de processos até
        que o tempo restante de todos seja 0, para isso, guarda-se o tempo total de execução do 
        conjunto de processos quando esse conjunto é criado, quando o valor total de tempo de execução é 0,
        significa que todos os processos foram executados.'''

        global algo 
        algo = 1

        global totalCpuTimeLeft

        initProcessos(1) # inicializar o vetor global em modo alternância circular
        global tempo
        j = 0
        while (totalCpuTimeLeft > 0):
            #executar escalonamento

            j = 0
            for j in range(0, len(vetprocessos)):
                if (vetprocessos[j].tempoRestante == 0):
                    continue
                # Emitindo os resultados para a interface
                text = f"Processo {vetprocessos[j].PID} executando\nTempo restante: {vetprocessos[j].tempoRestante}"
                self.text_changed.emit(text)
                print(f"Processo {vetprocessos[j].PID} executando")
                print(f"Tempo restante: {vetprocessos[j].tempoRestante}")

                rand_numb = random.randint(1, 100)
                if (rand_numb <= vetprocessos[j].chanceBloquear):
                    # Run I/O manager
                    global numDispositivos
                    dispositivo = random.randint(1, numDispositivos)
                    
                
                self.gerente.requireMem(vetprocessos[j])
                if (self.cpufrac < vetprocessos[j].tempoRestante):
                    self.cpuTime += self.cpufrac
                    vetprocessos[j].tempoRestante -= self.cpufrac
                    totalCpuTimeLeft -= self.cpufrac
                    
                    tempo += self.cpufrac
                elif (self.cpufrac >= vetprocessos[j].tempoRestante):
                    self.cpuTime += vetprocessos[j].tempoRestante
                    totalCpuTimeLeft -= vetprocessos[j].tempoRestante
                    vetprocessos[j].tempoRestante = 0

                    tempo += vetprocessos[j].tempoRestante

                    fout = open("output.txt", "a")
                    fout.write(f"{vetprocessos[j].nome} encerrou em {self.cpuTime}\n")
                    fout.close()

                if (self.test):
                    time.sleep(1)
                os.system("cls")

        text = f"Todos os processos terminaram, tempo final de CPU {self.cpuTime}\nGerenciador de Memória: {self.gerente.outputMem()}"
        self.text_changed.emit(text)

    
    def prioridade(self):
        '''Executa o processo de maior prioridade até o fim antes de executar outro processo.
        Utiliza uma fila de prioridades para manter acesso O(1) ao próximo processo que deve
        ser executado, sacrificando complexidade na construção do vetor de processos.'''

        global algo 
        algo = 2
        
        
        global totalCpuTimeLeft
        global vetprocessos

        initProcessos(2) # inicializa o vetor global em modo prioridade
        
        while(totalCpuTimeLeft > 0):
            prioridade =deepcopy(vetprocessos[0])
            vetprocessos.pop(0)
            while (prioridade.tempoRestante > 0):
                # Emitindo os resultados para a interface
                text = f"Processo {prioridade.PID} executando\nTempo restante: {prioridade.tempoRestante}"
                self.text_changed.emit(text)
                print(f"Processo {prioridade.PID} executando")
                print(f"Tempo restante: {prioridade.tempoRestante}")

                self.gerente.requireMem(prioridade)
                if (self.cpufrac < prioridade.tempoRestante):
                    prioridade.tempoRestante -= self.cpufrac
                    self.cpuTime += self.cpufrac
                    totalCpuTimeLeft -= self.cpufrac
                elif (self.cpufrac >= prioridade.tempoRestante):
                    self.cpuTime += prioridade.tempoRestante
                    totalCpuTimeLeft -= prioridade.tempoRestante
                    prioridade.tempoRestante = 0
                    
                    fout = open("output.txt", "a")
                    fout.write(f"{prioridade.nome} encerrou em {self.cpuTime}\n")
                    fout.close()
                    
                if (self.test):
                    time.sleep(1)
                os.system("cls")
            
            
        # file.close()
        text = f"Todos os processos terminaram, tempo final de CPU {self.cpuTime}\nGerenciador de Memória: {self.gerente.outputMem()}"
        self.text_changed.emit(text)
    
    def loteria(self):
        '''É escolhido um processo dentro do vetor de processos a partir de uma escolha aleatória com pesos, em que a probabilidade de um processo ser escolhido depende
        do número de bilhetes que esse processo possui (prioridade), quando um processo é escolhido, ele roda por uma self.cpufrac, e a loteria é feita novamente até que 
        o tempo restante de CPU seja igual a zero.'''

        global algo 
        algo = 3

        global vetprocessos
        global vetpesos
        global totalCpuTimeLeft

        initProcessos(3) # inicializa o vetor global em modo loteria
        
        while(totalCpuTimeLeft > 0):
            escolhido = choices(vetprocessos, vetpesos, k=1)[0] # Escolher 1 elemento de vetprocessos, com base nos pesos dados por vetpesos
            # choices não copia a lista que seleciona, então escolhido pode ser usado para alterar o vetor original.
            # indexar a lista também não cria uma cópia, permitindo a lógica abaixo.

            text = f"Processo {escolhido.PID} executando\nTempo restante: {escolhido.tempoRestante}"
            self.text_changed.emit(text)

            self.gerente.requireMem(escolhido)
            if (self.cpufrac < escolhido.tempoRestante):
                escolhido.tempoRestante -= self.cpufrac
                self.cpuTime += self.cpufrac
                totalCpuTimeLeft -= self.cpufrac
            elif (self.cpufrac >= escolhido.tempoRestante):
                self.cpuTime += escolhido.tempoRestante
                totalCpuTimeLeft -= escolhido.tempoRestante
                escolhido.tempoRestante = 0

                fout = open("output.txt", "a")
                fout.write(f"{escolhido.nome} encerrou em {self.cpuTime}\n")
                fout.close()

                # Quando o processo termina de executar ele precisa sair do vetor
                vetpesos.remove(escolhido.prioridade)
                vetprocessos.remove(escolhido)

                
            
            if (self.test):
                time.sleep(1)
        

        text = f"Todos os processos terminaram, tempo final de CPU {self.cpuTime}\nGerenciador de Memória: {self.gerente.outputMem()}"
        self.text_changed.emit(text)
    
    def CFS(self):

        global algo 
        algo = 4
        
        global vetprocessos
        global totalCpuTimeLeft

        initProcessos(4)
        
        while(totalCpuTimeLeft > 0):
            prioridade = deepcopy(vetprocessos[0]) # faz uma cópia do objeto em 0, sem referencia ao vetor
            vetprocessos.pop(0) # remove o objeto temporariamente, necessário para forçar ordem

            text = f"Processo {prioridade.PID} executando\nTempo restante: {prioridade.tempoRestante}"
            self.text_changed.emit(text)

            # REQUERIR MEMÓRIA PARA O PROCESSO ANTES DE EXECUTAR
            self.gerente.requireMem(prioridade)

            if (self.cpufrac < prioridade.tempoRestante):
                prioridade.tempoRestante -= self.cpufrac
                self.cpuTime += self.cpufrac
                totalCpuTimeLeft -= self.cpufrac

                prioridade.tempoRecebido += self.cpufrac * prioridade.prioridade # assumindo que menor numero == mais prioridade
                vetprocessos.add(prioridade)
            elif (self.cpufrac >= prioridade.tempoRestante):
                self.cpuTime += prioridade.tempoRestante
                totalCpuTimeLeft -= prioridade.tempoRestante
                prioridade.tempoRestante = 0

                fout = open("output.txt", "a")
                fout.write(f"{prioridade.nome} encerrou em {self.cpuTime}\n")
                fout.close()
            if (self.test):
                time.sleep(1)

        text = f"Todos os processos terminaram, tempo final de CPU {self.cpuTime}\nGerenciador de Memória: {self.gerente.outputMem()}"
        self.text_changed.emit(text)

    def run(self):
        # Inicializar o thread e ler o arquivo input
        # algoritmoDeEscalonamento|fraçãoDeCPU|políticaMemória|tamanhoMemória|tamanhoPáginasMolduras|percentualAlocação|acessosPorCiclo

        file = open(self.input, "r")
        line = file.readline()
        tmp = line.split("|")
        tmp[7] = tmp[7].replace("\n", '')
        metodo = tmp[0]
        self.cpufrac = int(tmp[1])

        global memPol
        global tamMem
        global tamPag
        global percAloc
        global acessosPorCiclo
        memPol = tmp[2]
        tamMem = int(tmp[3])
        tamPag = int(tmp[4])
        percAloc = int(tmp[5])
        acessosPorCiclo = int(tmp[6])

        numDispositivos = int(tmp[7])
        self.gerente = GerenciadorDeMemoria(memPol, tamMem, tamPag, percAloc, acessosPorCiclo)
        
        
        # chamar inicialização de threads de dispositivos
        for i in range(0, numDispositivos):
            line = file.readline()
            line = line.split("|")
            id = int(line[0])
            numSimultaneos = int(line[1])
            tempoOp = int(line[2])

            initDispositivo(id, numSimultaneos, tempoOp, numDispositivos)
        

        if (metodo == "alternanciaCircular"):
            while True:
                self.alternanciaCircular()
        elif(metodo == "prioridade"):
            while True:
                self.prioridade()
        elif(metodo == "loteria"):
            while True:
                self.loteria()
        elif(metodo == "CFS"):
            while True:
                self.CFS()
        file.close()