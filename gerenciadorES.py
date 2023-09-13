from PyQt5.QtCore import QThread, pyqtSignal, Qt
from escalonador import *
from interface import *
# numDispositivos = número de threads que devem ser incializadas

dispositivos = []

def initDispositivo(id, numSimultaneos, tempoOperacao):
    # Incializar thread de dispositivo

    global dispositivos
    
    thread = Dispositivo(id, numSimultaneos, tempoOperacao)
    thread.start()
    dispositivos.append(thread)
    return thread.__str__()

class Dispositivo(QThread):

    text_device = pyqtSignal(str)

    def __init__(self, id, numSimultaneos, tempoOperacao):
        self.id = id - 1
        self.numSimultaneos = numSimultaneos
        self.tempoOperacao = tempoOperacao
        self.usoAtual = 0
        self.processosAtual = [None] * numSimultaneos
        QThread.__init__(self)

    def __str__(self):
        return f"Dispositivo {self.id} Uso Máximo: {self.numSimultaneos} Uso Atual: {self.usoAtual}"
    
    def addProcesso(self, processo):
        if self.usoAtual > self.numSimultaneos:
            return False
        for i in range(0, len(self.processosAtual)):
            if self.processosAtual[i] == None:
                self.processosAtual[i] = processo
                self.usoAtual += 1

                return True
    
    def run(self):
        # inicializa a thread dispositivo
        return None