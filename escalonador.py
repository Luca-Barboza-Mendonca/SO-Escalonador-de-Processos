import time
import os
import sys
from random import choices
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QPushButton, QLabel, QVBoxLayout, QWidget
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtGui import QFont

class Processo:
    '''Registro que guarda todas as informações de um processo'''
    def __init__(self,nome, PID,tempoRestante, prioridade, UID, memoria):
        self.nome = nome
        self.PID = PID
        self.tempoRestante = tempoRestante
        self.prioridade = prioridade
        self.UID = UID
        self.memoria = memoria

class Escalonador(QThread):
    '''Classe escalonador que roda como um thread, permitindo paralelismo na interface gráfica. Muito do código entre os diferentes algoritmos é repetido, isso é proposital
    para garantir modularidade entre os métodos de escalonamento, caso trabalhos futuros tenham o escopo de expandir essa implementação.'''
    text_changed = pyqtSignal(str)

    def __init__(self, inp):
        self.input = inp
        self.cpufrac = 0
        self.cpuTime = 0
        QThread.__init__(self)
    
    def __del__(self):
        self.wait()
    
    
    def alternanciaCircular(self):
        '''Executa cada processo 1 vez pela fração de CPU, iterando sobre o vetor de processos até
        que o tempo restante de todos seja 0, para isso, guarda-se o tempo total de execução do 
        conjunto de processos quando esse conjunto é criado, quando o valor total de tempo de execução é 0,
        significa que todos os processos foram executados.'''

        vetprocessos = []
        
        file = open(self.input, "r")
        tmp = "placeholder"

        if (self.input != "userinput.txt"):
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
                # Emitindo os resultados para a interface
                text = f"Processo {vetprocessos[j].PID} executando\nTempo restante: {vetprocessos[j].tempoRestante}"
                self.text_changed.emit(text)
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
                

                time.sleep(1)
                os.system("cls")
        file.close()
        print(f"Todos os processos terminaram, tempo final de CPU {self.cpuTime}")
        text = f"Todos os processos terminaram, tempo final de CPU {self.cpuTime}"
        self.text_changed.emit(text)
        if (self.input == "userinput.txt"):
            file = open("userinput.txt", "w")
            file.write("")
            file.close()
        os.system("cls")
    
    def prioridade(self):
        '''Executa o processo de maior prioridade até o fim antes de executar outro processo.
        Utiliza uma fila de prioridades para manter acesso O(1) ao próximo processo que deve
        ser executado, sacrificando complexidade na construção do vetor de processos.'''
        
        tmp = "placeholder"
        vetprocessos = []
        file = open(self.input, "r")
        if (self.input != "userinput.txt"):
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
                # Emitindo os resultados para a interface
                text = f"Processo {prioridade.PID} executando\nTempo restante: {prioridade.tempoRestante}"
                self.text_changed.emit(text)
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
                time.sleep(1)
                os.system("cls")
            
            vetprocessos.pop(0)
        file.close()
        print(f"Todos os processos terminaram, tempo final de CPU {self.cpuTime}")
        text = f"Todos os processos terminaram, tempo final de CPU {self.cpuTime}"
        self.text_changed.emit(text)

        if (self.input == "userinput.txt"):
            file = open("userinput.txt", "w")
            file.write("")
            file.close()
        os.system("cls")
    
    def loteria(self):
        '''É escolhido um processo dentro do vetor de processos a partir de uma escolha aleatória com pesos, isto é, a probabilidade de um processo ser escolhido depende
        do número de bilhetes que esse processo possui (prioridade), quando um processo é escolhido, ele roda por uma self.cpufrac, e a loteria é feita novamente até que 
        o tempo restante de CPU seja igual a zero.'''

        tmp = "placeholder"
        vetprocessos = []

        vetpesos = [] # guarda o número de bilhetes de cada processo, para ser passado no random.choices()

        file = open(self.input, "r")
        if (self.input != "userinput.txt"):
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
        
        while(totalCpuTimeLeft > 0):
            escolhido = choices(vetprocessos, vetpesos, k=1)[0] # Escolher 1 elemento de vetprocessos, com base nos pesos dados por vetpesos
            # choices não copia a lista que seleciona, então escolhido pode ser usado para alterar o vetor original.
            # indexar a lista também não cria uma cópia, permitindo a lógica abaixo.

            text = f"Processo {escolhido.PID} executando\nTempo restante: {escolhido.tempoRestante}"
            self.text_changed.emit(text)

            if (self.cpufrac <= escolhido.tempoRestante):
                escolhido.tempoRestante -= self.cpufrac
                self.cpuTime += self.cpufrac
                totalCpuTimeLeft -= self.cpufrac
            elif (self.cpufrac > escolhido.tempoRestante):
                self.cpuTime += escolhido.tempoRestante
                totalCpuTimeLeft -= escolhido.tempoRestante
                escolhido.tempoRestante = 0

                # Quando o processo termina de executar ele precisa sair do vetor
                vetpesos.remove(escolhido.prioridade)
                vetprocessos.remove(escolhido)
            
            time.sleep(0.01)
        
        file.close()

        text = f"Todos os processos terminaram, tempo final de CPU {self.cpuTime}"
        self.text_changed.emit(text)

        if (self.input == "userinput.txt"):
            file = open("userinput.txt", "w")
            file.write("")
            file.close()
        

    def run(self):
        # Inicializar o thread e ler o arquivo input

        file = open(self.input, "r")
        line = file.readline()
        tmp = line.split("|")
        metodo = tmp[0]
        self.cpufrac = int(tmp[1])
        if (tmp[0] == "alternanciaCircular"):
            self.alternanciaCircular()
        elif(tmp[0] == "prioridade"):
            self.prioridade()
        elif(tmp[0] == "loteria"):
            self.loteria()
        file.close()
        
        while True:
            self.input = "userinput.txt"
            if (metodo == "alternanciaCircular"):
                self.alternanciaCircular()
            elif(metodo == "prioridade"):
                self.prioridade()
            elif(metodo == "loteria"):
                self.loteria()

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
        
        self.thread = Escalonador("input.txt")
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
        file = open("userinput.txt", "a")
        file.write(textboxValue + "\n")
        self.textbox.setText("")


def main():
    app = QApplication([])
    window = Interface()
    window.show()

    sys.exit(app.exec())

if __name__ == '__main__':
    main()