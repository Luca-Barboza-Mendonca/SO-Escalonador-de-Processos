import typing
from PyQt5.QtCore import QObject
from escalonador import *
import threading

# numDispositivos = número de threads que devem ser incializadas

dispositivos = []

def initDispositivo(id, numSimultaneos, tempoOperacao):
    # Incializar thread de dispositivo

    global dispositivos
    
    for i in range(0, numDispositivos):
        thread = Dispositivo(id, numSimultaneos, tempoOperacao)
        dispositivos.append(thread)

class Dispositivo(QThread):

    text_device = pyqtSignal(str)

    def __init__(self, id, numSimultaneos, tempoOperacao):
        self.id = id
        self.numSimultaneos = numSimultaneos
        self.tempoOperacao = tempoOperacao
