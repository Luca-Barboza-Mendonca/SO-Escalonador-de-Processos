def makeInput():
    
    file = open("input.txt", 'r')
    tmp = file.readline()
    if tmp == '':
        return file
    tmp = tmp.split('|')

    str = ''

    for i in range(0, len(tmp)):
        str += tmp[i] + " "

    log = open('log.txt', 'w')
    log.write(str)
    log.close()

    numDisp = int(tmp[7])

    for i in range(0, numDisp):
        file.readline()

    return file