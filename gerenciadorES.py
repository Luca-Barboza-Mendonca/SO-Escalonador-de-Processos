from PyQt5.QtCore import QThread, pyqtSignal, Qt
from escalonador import *
from interface import *
# numDispositivos = número de threads que devem ser incializadas

dispositivos = []

def initDispositivo(id, numSimultaneos, tempoOperacao):
    # Incializar thread de dispositivo

    global dispositivos
    global window
    
    thread = Dispositivo(id, numSimultaneos, tempoOperacao)
    dispositivos.append(thread)
    return thread.__str__()

class Dispositivo(QThread):

    text_device = pyqtSignal(str)

    def __init__(self, id, numSimultaneos, tempoOperacao):
        self.id = id
        self.numSimultaneos = numSimultaneos
        self.tempoOperacao = tempoOperacao
        self.usoAtual = 0
        QThread.__init__(self)

    def __str__(self):
        return f"Dispositivo {self.id} Uso Máximo: {self.numSimultaneos} Uso Atual: {self.usoAtual}"