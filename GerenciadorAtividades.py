from PyQt5 import QtCore, QtGui, QtWidgets
from gui.MateriasGUI import UiForm as Materias
from gui.AtividadesGUI import UiForm as Atividades
import banco.ConectaBase as conn

class Ui_mainWindow(QtWidgets.QMainWindow):

    __telaMateria = None
    __telaAtividade = None

    def __init__(self, parent=None):
        super(Ui_mainWindow, self).__init__(parent)
        self.setupUi()

    def setupUi(self):
        self.setObjectName("mainWindow")
        self.resize(475, 110)

        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")

        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 461, 51))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")

        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.btnMaterias = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.btnMaterias.clicked.connect(self.chamaTelaMaterias)
        self.btnMaterias.setObjectName("btnMaterias")
        self.horizontalLayout.addWidget(self.btnMaterias)

        self.btnAtividades = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.btnAtividades.clicked.connect(self.chamaTelaAtividades)
        self.btnAtividades.setObjectName("btnAtividades")
        self.horizontalLayout.addWidget(self.btnAtividades)

        self.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 475, 21))
        self.menubar.setObjectName("menubar")

        self.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("mainWindow", "Gerenciador de Atividades"))
        self.btnMaterias.setText(_translate("mainWindow", "Materias"))
        self.btnAtividades.setText(_translate("mainWindow", "Atividades"))

    def chamaTelaMaterias(self):
        self.__telaMateria = Materias(self)
        self.__telaMateria.show()

    def chamaTelaAtividades(self):
        self.__telaAtividade = Atividades(self)

def main():
    import sys
    import os

    dir_path = '%s\\GerenciadorAtividade\\files' % os.environ['APPDATA']
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    conn.ConectaBase().cria_estrutura_banco()
    app = QtWidgets.QApplication(sys.argv)
    icon = QtGui.QIcon()
    icon.addFile(u"resources/logo.png")
    app.setWindowIcon(icon)
    mainWindow = Ui_mainWindow()
    mainWindow.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
