from escalonador import *

class Interface(QMainWindow):
    '''Classe de Interface utilizando o Framework PyQt5 para criar uma interface de usuário simples, assim como implementar capacidades de paralelismo
    no funcionamento do input de usuário. O código abaixo define apenas o funcionamento da interface, e não tem parte na lógica do escalonador.'''
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Escalonador")
        self.setGeometry(10,10,800,280)

        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setFont(QFont("Arial", 16))

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        central_widget.setLayout(layout)
        
        self.thread = Escalonador("input.txt", True) # mudar o segundo param. para desailitar sleep
        self.thread.text_changed.connect(self.label.setText)
        self.thread.start()

        self.textbox = QLineEdit(self)
        self.textbox.move(265, 20)
        self.textbox.resize(280,40)

        self.button = QPushButton('Adicionar processo', self)
        self.button.move(20,80)
        self.button.clicked.connect(self.on_click)
        layout.addWidget(self.button)
    
    def on_click(self):
        textboxValue = self.textbox.text()
        addProcesso(textboxValue)
        self.textbox.setText("")
        # código antigo
        # file = open("userinput.txt", "a")
        # file.write(textboxValue + "\n")


def main():
    file = open("output.txt", "w")
    file.write("")
    file.close()

    app = QApplication([])
    window = Interface()
    window.show()

    sys.exit(app.exec())

if __name__ == '__main__':
    main()