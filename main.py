from copy import deepcopy
from sortedcontainers import SortedKeyList


class Processo:
    '''Registro que guarda todas as informações de um processo'''
    def __init__(self,nome, PID,tempoRestante, prioridade, UID, memoria):
        self.nome = nome
        self.PID = PID
        self.tempoRestante = tempoRestante
        self.prioridade = prioridade
        self.UID = UID
        self.memoria = memoria
        self.tempoRecebido = 0

a  = SortedKeyList(key=lambda x: x.tempoRecebido)

b = Processo("b", 1, 2, 3, 4, 5)
c = Processo("c", 1, 2, 3, 4, 5)
d = Processo("d", 1, 2, 3, 4, 5)

a.add(b)
a.add(c)
a.add(d)

e = deepcopy(a[0])
print(e)