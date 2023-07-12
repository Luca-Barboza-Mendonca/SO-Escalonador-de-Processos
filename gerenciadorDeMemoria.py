from escalonador import *

tempo = 0

class Pagina:
    def __init__(self, index,  ultimoAcesso, tempoEntrada):
        self.index = index
        self.ultimoAcesso = ultimoAcesso
        self.tempoEntrada = tempoEntrada
    
    def setUltimoAcesso(self, tempo):
        self.ultimoAcesso = tempo
    
    def setTempoEntrada(self, tempo):
        self.tempoEntrada = tempo

class Memoria:
    def __init__(self, tamMem, tamPag):
        self.tamMem = tamMem # tamanho da memória principal
        self.numPag = tamMem//tamPag
        self.numElem = 0
        self.memoria = [Pagina(-1, 0, 0)] * (self.numPag) # vetor de páginas, cada posição guarda o PID de um processo ou 0, indicando que está vazio

    def getTamMem(self):
        return self.tamMem
    
    def addPagina(self, index):
        '''Adiciona o indice na primeira pagina vazia que achar'''
        global tempo
        for i in range(0, self.numPag):
            if (self.memoria[i].index == -1):
                self.memoria[i] = Pagina(index, 0, tempo)
                return 1
        return -1
    
    def removePagina(self, indice):
        self.memoria[indice] = Pagina(-1, 0, 0)

    def buscaPagina(self, index):
        for i in range(0, self.numPag):
            # print(f"Busca Iteração {i}: {self.memoria[i].index}, buscando por {index}")
            if (self.memoria[i].index == index):
                print("ACHEI")
                return i
                
        return -1
    
    def orderFifo(self):
        self.memoria = sorted(self.memoria, key=lambda x: x.tempoEntrada)

class GerenciadorDeMemoria():
    '''Objeto gerenciador é utilizado diretamente pelo escalonador, não sendo acessível pela interface e descomplicando a sincronização'''
    def __init__(self, memPol, tamMem, tamPag, percAloc, acessosPorCiclo):
        self.memoriaFIFO = Memoria(tamMem, tamPag)
        self.memoriaMRU = Memoria(tamMem, tamPag)
        self.memoriaNUF = Memoria(tamMem, tamPag)
        self.memoriaOtimo = Memoria(tamMem, tamPag)


        self.percAloc = percAloc # Lembrar de implementar mais tarde
        self.memPol = memPol
        self.acessosPorCiclo = acessosPorCiclo

        self.numTrocasFIFO = 0

    
    def getTamMem(self):
        return self.memoria.getTamMem()
    
    def requireMem(self, processo):
        '''Função Interface que é chamada pelo escalonador para requerir a memória do processo,
        roda todos os algoritmos e guarda as informações relevantes de benchmark. Sempre que esse processo é chamado, ele requere
        o tempo de CPU atual'''
        self.fifo(processo)
        self.MRU(processo)
        self.NUF(processo)
        self.Otimo(processo)

    
    def fifo(self, processo):
        '''First In First out, quando a memória está cheia, o primeiro processo que entrou deve sair'''
        global tempo
        acessos = processo.sequenciaMemoria
        tam = len(acessos)
        print(tam)

        for i in range(0, tam):
            self.memoriaFIFO.orderFifo()
            busca = self.memoriaFIFO.buscaPagina(acessos[i]) # Procura página desejada na memória
            # print(f"Busca: {busca}")
            if (busca == -1): # página não está na memória
                if (self.memoriaFIFO.numElem == self.memoriaFIFO.numPag):
                    self.memoriaFIFO.removePagina(0) # Troca a página 0 (Por propriedade de ordenação é a mais antiga) por uma Página vazia
                self.memoriaFIFO.addPagina(acessos[i]) # adiciona a pagina na memória
                self.memoriaFIFO.orderFifo()
                self.numTrocasFIFO += 1
            
            busca = self.memoriaFIFO.buscaPagina(acessos[i]) # atualizar a busca, caso tenha ocorrido troca de memória
            self.memoriaFIFO.memoria[busca].setUltimoAcesso(tempo)

            tempo += 1 # pseudo tempo


            # Pseudo código: processo faz uso do que precisar da memória aqui
        
        print(self.numTrocasFIFO)


    def MRU(self, processo):
        pass

    def NUF(self, processo):
        pass

    def Otimo(self, processo):
        pass