from PyQt5.QtCore import QObject, QThread, pyqtSignal, Qt
from util import writeLog, lerTempo
import threading
import escalonador
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
            try:
                if self.processosAtual[i].is_alive() == False:
                    self.processosAtual[i] = threading.Thread(target=runIO, args=(self.id, i, processo, self.tempoOperacao))
                    self.processosAtual[i].start()
            except:
                pass
        return False
    def liberarProcesso(self, index, processo):
        writeLog(f"Dispositivo {self.id} liberando processo {processo.nome}")
        global vetprocessos
        escalonador.vetprocessos.append(processo)
        self.usoAtual -= 1
        self.processosAtual[index] = None
        
    
    def run(self):
        # inicializa a thread dispositivo
        return None


def runIO(deviceID, ind, processo, tempoOperacao):
    lock.acquire()
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
            break
        lock.release()
    return tempoFim
