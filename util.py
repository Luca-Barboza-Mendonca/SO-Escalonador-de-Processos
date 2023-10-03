def makeInput():
    
    file = open("input.txt", 'r')
    tmp = file.readline()
    if tmp == '':
        return file
    tmp = tmp.split('|')

    str = ''

    for i in range(0, len(tmp)):
        str += tmp[i] + " "

    log = open('log.txt', 'a')
    log.write(str)
    log.close()

    numDisp = int(tmp[7])

    for i in range(0, numDisp):
        file.readline()

    return file

def writeLog(text):
    log = open('log.txt', 'a')
    log.write(text + "\n")
    log.close()

def incrementarTempo(quant):
    f = open("tempo.txt", "r+")
    tempo = f.readline()
    f.close()
    f = open("tempo.txt", "w")
    tempo = int(tempo) + quant
    f.write(str(tempo))
    f.close

def lerTempo():
    f = open("tempo.txt", "r")
    t = f.readline()
    t = int(t)
    f.close()
    return t


