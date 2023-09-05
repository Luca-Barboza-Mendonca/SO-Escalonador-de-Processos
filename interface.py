from PyQt5 import QtCore
import sys
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QListWidget
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QPushButton, QLabel, QVBoxLayout, QWidget, QListWidgetItem
from escalonador import *


class Interface(QMainWindow):
    '''Classe de Interface utilizando o Framework PyQt5 para criar uma interface de usuário simples, assim como implementar capacidades de paralelismo
    no funcionamento do input de usuário. O código abaixo define apenas o funcionamento da interface, e não tem parte na lógica do escalonador.'''
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Escalonador")
        self.setGeometry(100,100,1000,780)

        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setFont(QFont("Arial", 16))

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        central_widget.setLayout(layout)
        


        self.textbox = QLineEdit(self)
        self.textbox.move(350, 20)
        self.textbox.resize(280,40)

        self.listwidget = QListWidget()
        
        self.listwidget.setMaximumWidth(1000)
        self.listwidget.setMaximumHeight(500)
        layout.addWidget(self.listwidget)

        self.button = QPushButton('Adicionar processo', self)
        self.button.move(20,80)
        self.button.clicked.connect(self.on_click)
        layout.addWidget(self.button)

        self.threadEscalonador = Escalonador("input.txt", False) # mudar o segundo param. para desailitar sleep
        self.threadEscalonador.text_changed.connect(self.label.setText)
        self.threadEscalonador.device_added.connect(self.insertItem)
        self.threadEscalonador.start()
    
    def on_click(self):
        textboxValue = self.textbox.text()
        addProcesso(textboxValue)
        self.textbox.setText("")
        # código antigo
        # file = open("userinput.txt", "a")
        # file.write(textboxValue + "\n")

    def insertItem(self, line):
        item = QListWidgetItem(line)

        self.listwidget.addItem(item)
        self.listwidget.repaint()

        self.listwidget.setCurrentItem(item)
    
    def setCurrentItem(self, index_to_set):
        # Set the current item to a specific index (e.g., index 1)

        if 0 <= index_to_set < self.listwidget.count():
            item_to_set = self.listwidget.item(index_to_set)
            self.listwidget.setCurrentItem(item_to_set)
    
    def updateItem(self, newText):
        selected_item = self.list_widget.currentItem()

        if selected_item:
            selected_item.setText(newText)

def main():
    file = open("output.txt", "w")
    file.write("")
    file.close()
    global window
    app = QApplication([])
    
    window = Interface()
    # for i in range(0, 100):
    #     window.insertItem(str(i))
    window.show()

    sys.exit(app.exec())

if __name__ == '__main__':
    main()