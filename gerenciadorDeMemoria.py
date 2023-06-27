from escalonador import *

memoriaSecundaria = [0] * (tamMem/tamPag) # Assumindo que a soma da memória de todos os processos é no máximo o tamanho da memória.

class Memoria:
    def __init__(self, tamMmem, tamPag):
        self.tamMem = tamMem # tamanho da memória principal
        self.memoria = [0] * (tamMem/tamPag) # vetor de páginas, cada posição guarda o PID de um processo ou 0, indicando que está vazio

class GerenciadorDeMemoria(QThread):
    '''Ideia: receber um sinal do escalonador indicando um acesso á memória'''
    def __init__(self) -> None:
        pass

