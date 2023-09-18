from PyQt5.QtCore import QObject, QThread, pyqtSignal, Qt
from util import writeLog, lerTempo
import threading
import escalonador
import interface
# numDispositivos = número de threads que devem ser incializadas

dispositivos = []

lock = threading.Lock()

tempo = 0

def initDispositivo(id, numSimultaneos, tempoOperacao):
    # Incializar thread de dispositivo

    global dispositivos
    
    thread = Dispositivo(id, numSimultaneos, tempoOperacao)
    thread.start()
    dispositivos.append(thread)
    return thread.__str__()

class Dispositivo(QThread):

    device_changed = pyqtSignal(str, int)

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
        tempo = lerTempo()
        writeLog(f"Processo {processo.nome} entrou em ES no tempo {tempo}")
        if self.usoAtual > self.numSimultaneos:
            writeLog(f"Dispositivo {self.id} sobrecarregado, negando ES")
            return False
        for i in range(0, len(self.processosAtual)):
            if self.processosAtual[i] == None:
                self.processosAtual[i] = threading.Thread(target=runIO, args=(self.id, i, processo, self.tempoOperacao))
                self.processosAtual[i].start()
                self.usoAtual += 1

                return True
        return False
    def liberarProcesso(self, index, processo):
        writeLog(f"Dispositivo {self.id} liberando processo {processo.nome}")
        escalonador.vetprocessos.append(processo)
        self.usoAtual -= 1
        self.processosAtual[index] = None
        self.device_changed.emit(self.__str__(), self.id)
        
    
    def run(self):
        # inicializa a thread dispositivo
        return None


def runIO(deviceID, ind, processo, tempoOperacao):
    lock.acquire() #causando deadlock
    tempo = lerTempo()
    tempoFim = tempo + tempoOperacao
    lock.release()
    while True:
        lock.acquire()
        tempo = lerTempo()
        print(tempo)
        if tempo >= tempoFim:
            dispositivos[deviceID].liberarProcesso(ind, processo)
            writeLog(f"Processo {processo.nome} terminou ES")
            lock.release()
            break
        lock.release()
    return tempoFim
