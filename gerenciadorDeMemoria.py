from PyQt5.QtCore import QThread, pyqtSignal, Qt

from escalonador import *

memoriaSecundaria = None # Assumindo que a soma da memória de todos os processos é no máximo o tamanho da memória.

def initDrive():
    global memoriaSecundaria
    memoriaSecundaria = [0] * (tamMem/tamPag)

class Memoria:
    def __init__(self, tamMem, tamPag):
        self.tamMem = tamMem # tamanho da memória principal
        self.memoria = [0] * (tamMem/tamPag) # vetor de páginas, cada posição guarda o PID de um processo ou 0, indicando que está vazio

class GerenciadorDeMemoria(QThread):
    '''Ideia: receber um sinal do escalonador indicando um acesso a memória'''
    def __init__(self):
        global memPol
        global tamMem
        global tamPag
        global percAloc
        global acessosPorCiclo
        self.memoria = Memoria(tamMem, tamPag)
        self.percAloc = percAloc
        self.memPol = memPol
        self.acessosPorCiclo = acessosPorCiclo

    def run(self):
        pass

