from escalonador import *

tempoFIFO = 0
tempoMRU = 0
tempoNUF = 0
tempoOtimo = 0

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
    
    def addPagina(self, index, tempo):
        '''Adiciona o indice na primeira pagina vazia que achar'''
        for i in range(0, self.numPag):
            if (self.memoria[i].index == -1):
                self.memoria[i] = Pagina(index, 0, tempo)
                self.numElem += 1
                return 1
        return -1
    
    def removePagina(self, indice):
        self.memoria[indice] = Pagina(-1, 0, 0)
        self.numElem -= 1

    def buscaPagina(self, index):
        for i in range(0, self.numPag):
            # print(f"Busca Iteração {i}: {self.memoria[i].index}, buscando por {index}")
            if (self.memoria[i].index == index):
                return i
                
        return -1
    
    def orderFifo(self):
        self.memoria = sorted(self.memoria, key=lambda x: x.tempoEntrada)
    
    def orderMRU(self):
        # tempo é uma variável que cresce, então o menos recentemente usado terá menor tempo de último acesso
        self.memoria = sorted(self.memoria, key=lambda x: x.ultimoAcesso)

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
        self.numTrocasMRU = 0
        self.numTrocasNUF = 0
        self.numTrocasOtimo = 0

    
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
        global tempoFIFO
        acessos = processo.sequenciaMemoria
        tam = len(acessos)
        # print(tam)

        for i in range(0, tam):
            self.memoriaFIFO.orderFifo()
            busca = self.memoriaFIFO.buscaPagina(acessos[i]) # Procura página desejada na memória
            # print(f"Busca: {busca}")
            if (busca == -1): # página não está na memória
                if (self.memoriaFIFO.numElem == self.memoriaFIFO.numPag):
                    self.memoriaFIFO.removePagina(0) # Troca a página 0 (Por propriedade de ordenação é a mais antiga) por uma Página vazia
                self.memoriaFIFO.addPagina(acessos[i], tempoFIFO) # adiciona a pagina na memória
                self.memoriaFIFO.orderFifo()
                self.numTrocasFIFO += 1
            
            busca = self.memoriaFIFO.buscaPagina(acessos[i]) # atualizar a busca, caso tenha ocorrido troca de memória
            self.memoriaFIFO.memoria[busca].setUltimoAcesso(tempoFIFO)

            tempoFIFO += 1 # pseudo tempo


            # Pseudo código: processo faz uso do que precisar da memória aqui
        
        print(f"Trocas FIFO: {self.numTrocasFIFO}")


    def MRU(self, processo):
        global tempoMRU
        acessos = processo.sequenciaMemoria
        tam = len(acessos)

        for i in range(0, tam):
            self.memoriaMRU.orderMRU()
            busca = self.memoriaMRU.buscaPagina(acessos[i])

            if (busca == -1):
                if (self.memoriaMRU.numElem == self.memoriaMRU.numPag):
                    self.memoriaMRU.removePagina(0) # remove a página 0, assumindo ordem correta do vetor

                self.memoriaMRU.addPagina(acessos[i], tempoMRU)
                self.memoriaMRU.orderMRU()
                self.numTrocasMRU += 1
            
            busca = self.memoriaMRU.buscaPagina(acessos[i])
            self.memoriaMRU.memoria[busca].setUltimoAcesso(tempoMRU)

            tempoMRU += 1
        
        print(f"Trocas MRU: {self.numTrocasMRU}")

    def NUF(self, processo):
        pass

    def Otimo(self, processo):
        pass