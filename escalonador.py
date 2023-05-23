import time
import os
import sys
from copy import deepcopy
from random import choices
from sortedcontainers import SortedKeyList
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QPushButton, QLabel, QVBoxLayout, QWidget
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtGui import QFont


vetprocessos = None
totalCpuTimeLeft = 0
vetpesos = [] # Só para o algoritmo de loteria
algo = 1

class Processo:
    '''Registro que guarda todas as informações de um processo'''
    def __init__(self,nome, PID,tempoRestante, prioridade, UID, memoria):
        self.nome = nome
        self.PID = PID
        self.tempoRestante = tempoRestante
        self.prioridade = prioridade
        self.UID = UID
        self.memoria = memoria
        self.tempoRecebido = 0

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
        
        file = open("input.txt", "w")
        file.write("")
        file.close()
    elif modo == 2:

        # Prioridade
        
        vetprocessos = []
        tmp = "placeholder"
        file = open("input.txt", "r")
        tmp = file.readline()

        i = 0
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
        file = open("input.txt", "w")
        file.write("")
        file.close()
    elif modo == 3:

        global vetpesos
        tmp = "placeholder"
        file = open("input.txt", "r")
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
            vetpesos.append(int(x[3]))  # guarda o peso do processo i na posição i
            totalCpuTimeLeft += int(x[2])
            i += 1
        file = open("input.txt", "w")
        file.write("")
        file.close()
    
    elif modo == 4:
        tmp = "placeholder"
        vetprocessos = SortedKeyList(key=lambda x: x.tempoRecebido)
        
        file = open("input.txt", "r")
        tmp = file.readline()
        
        i = 0
        totalCpuTimeLeft = 0

        while ((tmp) != ""):
            tmp = file.readline()
            if (tmp == ""):
                break
            x = tmp.split("|")
            processo = Processo(x[0], int(x[1]), int(x[2]), int(x[3]), int(x[4]), int(x[5]))
            vetprocessos.add(processo)
            totalCpuTimeLeft += int(x[2])
            i += 1
        file = open("input.txt", "w")
        file.write("")
        file.close()

def addProcesso(proc):
    '''Adicionar um processo específicado pelo usuário ao vetor global'''
    x = proc.split("|")
    processo = Processo(x[0], int(x[1]), int(x[2]), int(x[3]), int(x[4]), int(x[5]))
    global vetprocessos
    global totalCpuTimeLeft
    totalCpuTimeLeft += int(x[2])

    global algo

    if algo == 2:
        vetprocessos = sorted(vetprocessos, key=lambda x: x.prioridade, reverse=True)
        vetprocessos.append(processo)
    elif algo == 3:
        global vetpesos
        vetpesos.append(int(x[3]))
        vetprocessos.append(processo)
    elif algo == 4:
        vetprocessos.add(processo)


class Escalonador(QThread):
    '''Classe escalonador que roda como um thread, permitindo paralelismo na interface gráfica. Muito do código entre os diferentes algoritmos é repetido, isso é proposital
    para garantir modularidade entre os métodos de escalonamento, caso trabalhos futuros tenham o escopo de expandir essa implementação.'''
    text_changed = pyqtSignal(str)

    def __init__(self, inp, test=False):
        self.input = inp
        self.cpufrac = 0
        self.cpuTime = 0
        self.test = test # Só para desabilitar o sleep
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

        j = 0
        while (totalCpuTimeLeft > 0):
            #executar escalonamento

            j = 0
            for j in range(0, i):
                # Emitindo os resultados para a interface
                text = f"Processo {vetprocessos[j].PID} executando\nTempo restante: {vetprocessos[j].tempoRestante}"
                self.text_changed.emit(text)
                print(f"Processo {vetprocessos[j].PID} executando")
                print(f"Tempo restante: {vetprocessos[j].tempoRestante}")
                
                if (self.cpufrac < vetprocessos[j].tempoRestante):
                    self.cpuTime += self.cpufrac
                    vetprocessos[j].tempoRestante -= self.cpufrac
                    totalCpuTimeLeft -= self.cpufrac
                elif (self.cpufrac >= vetprocessos[j].tempoRestante):
                    self.cpuTime += vetprocessos[j].tempoRestante
                    totalCpuTimeLeft -= vetprocessos[j].tempoRestante
                    vetprocessos[j].tempoRestante = 0

                    fout = open("output.txt", "a")
                    fout.write(f"{vetprocessos[j].nome} encerrou em {self.cpuTime}\n")
                    fout.close()

                if (self.test):
                    time.sleep(0.1)
                os.system("cls")

        print(f"Todos os processos terminaram, tempo final de CPU {self.cpuTime}")
        text = f"Todos os processos terminaram, tempo final de CPU {self.cpuTime}"
        self.text_changed.emit(text)
        os.system("cls")

    
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
            prioridade = vetprocessos[0]
            while (prioridade.tempoRestante > 0):
                # Emitindo os resultados para a interface
                text = f"Processo {prioridade.PID} executando\nTempo restante: {prioridade.tempoRestante}"
                self.text_changed.emit(text)
                print(f"Processo {prioridade.PID} executando")
                print(f"Tempo restante: {prioridade.tempoRestante}")

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
                    time.sleep(0.1)
                os.system("cls")
            
            vetprocessos.pop(0)
        # file.close()
        print(f"Todos os processos terminaram, tempo final de CPU {self.cpuTime}")
        text = f"Todos os processos terminaram, tempo final de CPU {self.cpuTime}"
        self.text_changed.emit(text)
        os.system("cls")
    
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
                time.sleep(0.1)
        

        text = f"Todos os processos terminaram, tempo final de CPU {self.cpuTime}"
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
                time.sleep(0.1)

        text = f"Todos os processos terminaram, tempo final de CPU {self.cpuTime}"
        self.text_changed.emit(text)

    def run(self):
        # Inicializar o thread e ler o arquivo input

        file = open(self.input, "r")
        line = file.readline()
        tmp = line.split("|")
        metodo = tmp[0]
        self.cpufrac = int(tmp[1])
        if (tmp[0] == "alternanciaCircular"):
            while True:
                self.alternanciaCircular()
        elif(tmp[0] == "prioridade"):
            while True:
                self.prioridade()
        elif(tmp[0] == "loteria"):
            while True:
                self.loteria()
        elif(tmp[0] == "CFS"):
            while True:
                self.CFS()
        file.close()

class Interface(QMainWindow):
    '''Classe de Interface utilizando o Framework PyQt5 para criar uma interface de usuário simples, assim como implementar capacidades de paralelismo
    no funcionamento do input de usuário. O código abaixo define apenas o funcionamento da interface, e não tem parte na lógica do escalonador.'''
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Escalonador")
        self.setGeometry(10,10,800,280)

        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setFont(QFont("Arial", 16))

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        central_widget.setLayout(layout)
        
        self.thread = Escalonador("input.txt", True) # mudar o segundo param. para desailitar sleep
        self.thread.text_changed.connect(self.label.setText)
        self.thread.start()

        self.textbox = QLineEdit(self)
        self.textbox.move(265, 20)
        self.textbox.resize(280,40)

        self.button = QPushButton('Adicionar processo', self)
        self.button.move(20,80)
        self.button.clicked.connect(self.on_click)
        layout.addWidget(self.button)
    
    def on_click(self):
        textboxValue = self.textbox.text()
        addProcesso(textboxValue)
        self.textbox.setText("")
        # código antigo
        # file = open("userinput.txt", "a")
        # file.write(textboxValue + "\n")


def main():
    file = open("output.txt", "w")
    file.write("")
    file.close()

    app = QApplication([])
    window = Interface()
    window.show()

    sys.exit(app.exec())

if __name__ == '__main__':
    main()