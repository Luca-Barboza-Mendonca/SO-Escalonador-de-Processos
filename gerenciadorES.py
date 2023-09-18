from PyQt5.QtCore import QObject, QThread, pyqtSignal, Qt
from interface import *
# numDispositivos = número de threads que devem ser incializadas

dispositivos = []

tempo = 0

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


        for i in range(0, len(self.processosAtual)):
            if self.processosAtual[i] != None:
                self.processosAtual[i].IOend.connect(self.liberarProcesso)
        QThread.__init__(self)

    def __str__(self):
        return f"Dispositivo {self.id} Uso Máximo: {self.numSimultaneos} Uso Atual: {self.usoAtual}"
    
    def addProcesso(self, processo):
        if self.usoAtual > self.numSimultaneos:
            return False
        for i in range(0, len(self.processosAtual)):
            if self.processosAtual[i] == None:
                self.processosAtual[i] = IODispositivo(i, processo, self.tempoOperacao)
                self.processosAtual[i].start()
                self.usoAtual += 1

                return True
            try:
                if self.processosAtual[i].isActive == False:
                    self.processosAtual[i] = IODispositivo(i, processo, self.tempoOperacao)
                    self.processosAtual[i].start()
            except:
                pass
    def liberarProcesso(self, index):
        processo = self.processosAtual[index]
        global vetprocessos
        vetprocessos.append(processo.processo)
        self.usoAtual -= 1
    
    def run(self):
        # inicializa a thread dispositivo
        return None

class IODispositivo(QThread):

    IOend = pyqtSignal(int)

    def __init__(self, ind, processo, tempoOperacao):
        self.index = ind
        self.processo = processo
        global tempo
        self.tempoFim = tempo + tempoOperacao
        self.isActive = True
        QThread.__init__(self)

    def run(self):
        global tempo
        while tempo < self.tempoFim:
            pass

        self.stop()

    def stop(self):
        self.isActive = False
        self.IOend.emit(self.index)
        return self.tempoFim