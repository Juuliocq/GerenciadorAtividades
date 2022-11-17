from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import QRect, QSortFilterProxyModel
from PyQt5.QtWidgets import QPushButton, QMessageBox, QLineEdit, QTableView, QLabel

from model.Materia import Materia
from service.MateriaService import MateriaService




class UiForm(QtWidgets.QMainWindow):
    lista_materias = None
    materia_service = None
    materia = None

    def __init__(self, parent):
        super(UiForm, self).__init__(parent)
        self.parent_frame = parent

        self.parent_frame.btnMaterias.setEnabled(False)
        self.materia_service = MateriaService()
        self.setup_ui()
        self.consultar(False)

    def setup_ui(self):
        self.setObjectName("materias")
        self.resize(695, 569)

        self.lbl_descricao = QtWidgets.QLabel(self)
        self.lbl_descricao.setGeometry(QRect(450, 10, 47, 13))
        self.lbl_descricao.setObjectName("lblDescricao")

        self.list_view = QTableView(self)
        self.list_view.setGeometry(QRect(5, 10, 431, 521))
        self.list_view.setObjectName("listView")
        self.list_view.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.list_view.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.list_view.verticalHeader().hide()
        self.list_view.setSortingEnabled(True)

        self.txt_descricao = QLineEdit(self)
        self.txt_descricao.setEnabled(False)
        self.txt_descricao.setGeometry(QRect(450, 30, 231, 20))
        self.txt_descricao.setObjectName("txtDescricao")

        self.txt_professor = QLineEdit(self)
        self.txt_professor.setEnabled(False)
        self.txt_professor.setGeometry(QRect(450, 100, 231, 20))
        self.txt_professor.setObjectName("txtProfessor")

        self.lbl_professor = QtWidgets.QLabel(self)
        self.lbl_professor.setGeometry(QRect(450, 80, 47, 13))
        self.lbl_professor.setObjectName("lblProfessor")

        self.btn_incluir = QPushButton(self)
        self.btn_incluir.setObjectName(u"btnIncluir")
        self.btn_incluir.setGeometry(QRect(450, 150, 231, 23))
        self.btn_incluir.clicked.connect(self.incluir)

        self.btn_salvar = QPushButton(self)
        self.btn_salvar.setObjectName(u"btnSalvar")
        self.btn_salvar.setGeometry(QRect(570, 200, 111, 23))
        self.btn_salvar.setEnabled(False)
        self.btn_salvar.clicked.connect(self.salvar)

        self.btn_alterar = QPushButton(self)
        self.btn_alterar.setObjectName(u"btnAlterar")
        self.btn_alterar.setGeometry(QRect(450, 200, 111, 23))
        self.btn_alterar.clicked.connect(self.alterar)
        self.btn_alterar.setEnabled(False)

        self.btn_excluir = QPushButton(self)
        self.btn_excluir.setObjectName(u"btnExcluir")
        self.btn_excluir.setGeometry(QRect(450, 250, 231, 23))
        self.btn_excluir.clicked.connect(self.excluir)
        self.btn_excluir.setEnabled(False)

        self.btn_cancelar = QPushButton(self)
        self.btn_cancelar.setObjectName(u"btnCancelar")
        self.btn_cancelar.setGeometry(QRect(450, 340, 231, 23))
        self.btn_cancelar.clicked.connect(self.cancelar)
        self.btn_cancelar.setEnabled(False)

        self.txtConsultar = QLineEdit(self)
        self.txtConsultar.setObjectName(u"txtConsultar")
        self.txtConsultar.setGeometry(QRect(12, 540, 341, 20))
        self.txtConsultar.installEventFilter(self)

        self.btnConsultar = QPushButton(self)
        self.btnConsultar.setObjectName(u"btnConsultar")
        self.btnConsultar.setGeometry(QRect(360, 540, 75, 23))
        self.btnConsultar.clicked.connect(self.consultar_botao)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Form", "Matérias"))
        self.lbl_descricao.setText(_translate("Form", "Descrição"))
        self.lbl_professor.setText(_translate("Form", "Professor"))
        self.btn_incluir.setText(_translate("Form", u"Incluir", None))
        self.btn_salvar.setText(_translate("Form", u"Salvar", None))
        self.btn_alterar.setText(_translate("Form", u"Alterar", None))
        self.btn_excluir.setText(_translate("Form", u"Excluir", None))
        self.btn_cancelar.setText(_translate("Form", u"Cancelar", None))
        self.btnConsultar.setText(_translate("Form", u"Consultar", None))

    def consultar_botao(self):
        self.consultar(True)

    def consultar(self, verifica_consulta_vazia: bool):
        filtros = self.txtConsultar.text()

        try:
            self.lista_materias = self.materia_service.consultaMaterias(filtros)
        except ValueError as ve_ex:
            self.btn_alterar.setEnabled(False)
            self.btn_excluir.setEnabled(False)
            self.btn_salvar.setEnabled(False)
            self.btn_incluir.setEnabled(True)
            self.list_view.viewport().removeEventFilter(self)
            self.list_view.setModel(None)

            if verifica_consulta_vazia:
                mensagem = ve_ex.args[0]
                self.show_mensagem(mensagem, QMessageBox.Warning)

            return

        self.popula_lista()

    def popula_lista(self):

        self.list_view.viewport().installEventFilter(self)
        modelDados = TableModelMateria(self.lista_materias)
        modeloOrdenado = QSortFilterProxyModel()
        modeloOrdenado.setSourceModel(modelDados)
        self.list_view.setModel(modeloOrdenado)

        self.list_view.setColumnHidden(0, True)
        self.list_view.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

    def salvar(self):

        try:
            self.valida_descricao_vazia()
        except ValueError as ve_ex:

            mensagem = ve_ex.args[0]
            self.show_mensagem(mensagem, QMessageBox.Critical)
            return

        self.materia.setDescricaoEProfessor(self.txt_descricao.text(), self.txt_professor.text())

        try:
            if self.materia.getId() is None:
                self.salvar_incluir()
            else:
                self.salvar_alterar()

        except ValueError as ve_ex:
            mensagem = ve_ex.args[0]
            self.show_mensagem(mensagem, QMessageBox.Critical)
            return

        self.reseta_txts()
        self.desabilita_txts()
        self.habilita_consulta()
        self.habilita_botoes()
        self.btn_salvar.setEnabled(False)
        self.btn_cancelar.setEnabled(False)
        self.list_view.viewport().installEventFilter(self)

    def salvar_incluir(self):
        tem_descricao_repetida = self.materia_service.valida_descricao_igual_incluir(self.materia)

        if tem_descricao_repetida:
            return True

        self.materia_service.cadastraMateria(self.materia)

    def salvar_alterar(self):
        self.materia_service.valida_descricao_igual_alterar(self.materia)

        self.materia_service.alteraMateria(self.materia)

        mensagem = "A matéria {} foi alterada com sucesso!".format(self.materia.getDescricao())
        self.show_mensagem(mensagem, QMessageBox.Information)

        return False

    def incluir(self):
        self.list_view.viewport().removeEventFilter(self)
        self.habilita_txts()
        self.desabilita_botoes()
        self.btn_salvar.setEnabled(True)
        self.btn_cancelar.setEnabled(True)
        self.desabilita_consulta()

        self.materia = Materia(None, None)

    def alterar(self):
        self.list_view.viewport().removeEventFilter(self)
        self.habilita_txts()
        self.desabilita_botoes()
        self.btn_salvar.setEnabled(True)
        self.btn_cancelar.setEnabled(True)
        self.desabilita_consulta()

        index = self.list_view.currentIndex()
        id_materia = self.list_view.model().index(index.row(), 0).data()
        descricao_materia = self.list_view.model().index(index.row(), 1).data()
        professor_materia = self.list_view.model().index(index.row(), 2).data()

        self.txt_professor.setText(professor_materia)
        self.txt_descricao.setText(descricao_materia)

        self.materia = Materia.criaMateriaComId(id_materia, None, None)

    def excluir(self):
        index = self.list_view.currentIndex()
        id_materia = self.list_view.model().index(index.row(), 0).data()
        descricao_materia = self.list_view.model().index(index.row(), 1).data()

        self.materia = Materia.criaMateriaComId(id_materia, descricao_materia, None)

        mensagem = "Deseja realmente excluir a matéria " + self.materia.getDescricao() + "?\nTodas as atividades relacionadas também serão excluidas!"
        titulo = "Deseja excluir?"
        deseja_excluir = self.show_mensagem_confirma(mensagem, titulo)

        if deseja_excluir == QMessageBox.No:
            return

        try:
            self.materia_service.excluiMateria(self.materia)
        except ValueError as ve_ex:
            mensagem = ve_ex.args[0]
            self.show_mensagem(mensagem, QMessageBox.Information)
            return

        self.desabilita_txts()

        mensagem = "A matéria {} foi excluida com sucesso!".format(self.materia.getDescricao())
        self.show_mensagem(mensagem, QMessageBox.Information)

    def cancelar(self):
        mensagem = "Deseja realmente cancelar a operação? Todas as alterações serão perdidas!"
        titulo = "Deseja cancelar?"
        deseja_cancelar = self.show_mensagem_confirma(mensagem, titulo)

        if deseja_cancelar == QMessageBox.Yes:
            self.list_view.viewport().installEventFilter(self)
            self.reseta_txts()
            self.desabilita_botoes()
            self.habilita_consulta()
            self.btn_salvar.setEnabled(False)
            self.btn_incluir.setEnabled(True)
            self.btn_cancelar.setEnabled(False)
            self.list_view.clearSelection()

    def valida_consulta_vazia(self):
        if len(self.lista_materias) <= 0:
            self.btn_alterar.setEnabled(False)
            self.btn_excluir.setEnabled(False)
            self.btn_salvar.setEnabled(False)
            self.btn_incluir.setEnabled(True)
            self.list_view.viewport().removeEventFilter(self)
            self.lista_materias = None

            mensagem = "Nenhum registro encontrado!"
            self.show_mensagem(mensagem, QMessageBox.Warning)
            self.list_view.setModel(self.lista_materias)
            return

    def show_mensagem_confirma(self, mensagem: str, titulo: str):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Question)
        msg_box.setText(mensagem)
        msg_box.setWindowTitle(titulo)
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        botao_sim = msg_box.button(QMessageBox.Yes)
        botao_nao = msg_box.button(QMessageBox.No)
        botao_sim.setText("Sim")
        botao_nao.setText("Cancelar")

        return msg_box.exec()

    def show_mensagem(self, mensagem: str, icone):
        msg_box = QMessageBox()
        msg_box.setIcon(icone)
        msg_box.setText(mensagem)
        msg_box.setWindowFlag(QtCore.Qt.FramelessWindowHint)

        msg_box.exec_()

    def valida_descricao_vazia(self):
        if not self.txt_descricao.text().strip():
            raise ValueError("A descrição não pode ser vazia!")

    def habilita_consulta(self):
        self.btnConsultar.setEnabled(True)
        self.txtConsultar.setEnabled(True)

    def desabilita_consulta(self):
        self.btnConsultar.setEnabled(False)
        self.txtConsultar.setEnabled(False)

    def habilita_txts(self):
        self.txt_professor.setEnabled(True)
        self.txt_descricao.setEnabled(True)

    def desabilita_txts(self):
        self.txt_professor.setEnabled(False)
        self.txt_descricao.setEnabled(False)

    def reseta_txts(self):
        self.txt_professor.setText("")
        self.txt_descricao.setText("")
        self.desabilita_txts()

    def habilita_botoes(self):
        self.btn_alterar.setEnabled(True)
        self.btn_incluir.setEnabled(True)
        self.btn_excluir.setEnabled(True)

    def desabilita_botoes(self):
        self.btn_alterar.setEnabled(False)
        self.btn_incluir.setEnabled(False)
        self.btn_excluir.setEnabled(False)

    def desabilita_botoes_alterar_excluir(self):
        self.btn_alterar.setEnabled(False)
        self.btn_excluir.setEnabled(False)

    def closeEvent(self, event):
        self.parent_frame.btnMaterias.setEnabled(True)

    def eventFilter(self, obj, event):
        if obj is self.list_view.viewport():
            if event.type() == QtCore.QEvent.MouseButtonPress:
                if event.button() == QtCore.Qt.LeftButton and event.button():
                    self.btn_alterar.setEnabled(True)
                    self.btn_excluir.setEnabled(True)

            if event.type() == QtCore.QEvent.MouseButtonDblClick:
                self.alterar()

        if obj is self.txtConsultar:
            if event.type() == QtCore.QEvent.KeyPress:
                if event.key() == QtCore.Qt.Key_Enter or event.key() == QtCore.Qt.Key_Return:
                    self.consultar(True)

        return super().eventFilter(obj, event)


class TableModelMateria(QtCore.QAbstractTableModel):
    def __init__(self, data):
        self.columns = ["", "Descrição", "Professor"]
        super(TableModelMateria, self).__init__()

        self._data = data

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if role == QtCore.Qt.DisplayRole:
            return self._data[index.row()][index.column()]

    def rowCount(self, index):
        return len(self._data)

    def columnCount(self, index):
        return len(self._data[0])

    def headerData(self, section, orientation, role):
        if role != QtCore.Qt.DisplayRole:
            return None
        if orientation == QtCore.Qt.Horizontal:
            return self.columns[section]
        else:
            return "{}".format(section)
