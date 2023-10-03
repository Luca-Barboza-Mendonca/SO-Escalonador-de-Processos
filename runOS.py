import os

f = open("log.txt", "w")
f.write("")
f.close()

f = open("tempo.txt", "w")
f.write("0")
f.close()

f1 = open("input2.txt", "r")
txt = f1.read()
f1.close()
f2 = open("input.txt", "w")
f2.write(txt)
f2.close()

os.system("python interface.py")
