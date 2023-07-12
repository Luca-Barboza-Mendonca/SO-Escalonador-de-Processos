from escalonador import *
from escalonador import Processo

class Pagina:
    def __init__(self):
        self.ultimoAcesso = 0
        self.tempoEntrada = 0
    
    def setUltimoAcesso(self, tempo):
        self.ultimoAcesso = tempo
    
    def setTempoEntrada(self, tempo):
        self.tempoEntrada = tempo

class Memoria:
    def __init__(self, tamMem, tamPag):
        self.tamMem = tamMem # tamanho da memória principal
        self.memoria = [0] * (tamMem//tamPag) # vetor de páginas, cada posição guarda o PID de um processo ou 0, indicando que está vazio

    def getTamMem(self):
        return self.tamMem
    
    def addPagina(self, pagina, tempo):
        pagina.setTempoEntrada(tempo)
        self.memoria.append(pagina)
    
    def removePagina(self, pagina):
        self.memoria.remove(pagina)

class GerenciadorDeMemoria():
    '''Objeto gerenciador é utilizado diretamente pelo escalonador, não sendo acessível pela interface e descomplicando a sincronização'''
    def __init__(self, memPol, tamMem, tamPag, percAloc, acessosPorCiclo):
        self.memoriaFIFO = Memoria(tamMem, tamPag)
        self.memoriaMRU = Memoria(tamMem, tamPag)
        self.memoriaNUF = Memoria(tamMem, tamPag)
        self.memoriaOtimo = Memoria(tamMem, tamPag)
        self.percAloc = percAloc
        self.memPol = memPol
        self.acessosPorCiclo = acessosPorCiclo
    
    def getTamMem(self):
        return self.memoria.getTamMem()
    
    def requireMem(self, processo: Processo, tempoAtual: int):
        '''Função Interface que é chamada pelo escalonador para requerir a memória do processo,
        roda todos os algoritmos e guarda as informações relevantes de benchmark. Sempre que esse processo é chamado, ele requere
        o tempo de CPU atual'''
        self.fifo(processo, tempoAtual)
        self.MRU(processo, tempoAtual)
        self.NUF(processo, tempoAtual)
        self.Otimo(processo, tempoAtual)

    
    def fifo(self, processo: Processo, tempo: int):
        acessos = processo.sequenciaMemoria

    def MRU(self, processo, tempo):
        pass

    def NUF(self, processo, tempo):
        pass

    def Otimo(self, processo, tempo):
        pass