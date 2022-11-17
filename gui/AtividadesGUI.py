import os
from datetime import date

from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import QRect, QModelIndex, QDate, QSortFilterProxyModel
from PyQt5.QtWidgets import QPushButton, QLineEdit, QTableView, QLabel, QComboBox, QDateEdit, QListView, QMessageBox

from config.Configs import FILES_DIR
from enumeracao.SituacaoAtividade import SituacaoAtividade
from model.Atividade import Atividade
from model.Materia import Materia
from service.ArquivoService import ArquivoService
from service.AtividadeService import AtividadeService
from service.MateriaService import MateriaService


class UiForm(QtWidgets.QMainWindow):
    lista_atividades = None
    atividade_service = None
    materia_service = None
    atividade = None
    arquivo_temporario = None
    arquivo_service = None

    def __init__(self, parent):
        super(UiForm, self).__init__(parent)
        self.parent_frame = parent

        self.parent_frame.btnAtividades.setEnabled(False)
        self.materia_service = MateriaService()
        self.atividade_service = AtividadeService()
        self.arquivo_service = ArquivoService()

        self.setup_ui()
        self.consultar(False)

    def setup_ui(self):
        self.setObjectName("materias")
        self.resize(695, 569)

        self.lblDescricao = QLabel(self)
        self.lblDescricao.setObjectName(u"lblDescricao")
        self.lblDescricao.setGeometry(QRect(450, 10, 47, 13))

        self.list_view = QTableView(self)
        self.list_view.setGeometry(QRect(5, 10, 431, 521))
        self.list_view.setObjectName("listView")
        self.list_view.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.list_view.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.list_view.verticalHeader().hide()
        self.list_view.setSortingEnabled(True)

        self.txt_descricao = QLineEdit(self)
        self.txt_descricao.setObjectName(u"txtDescricao")
        self.txt_descricao.setEnabled(False)
        self.txt_descricao.setGeometry(QRect(450, 30, 231, 20))

        self.lbl_materia = QLabel(self)
        self.lbl_materia.setObjectName(u"lblMateria")
        self.lbl_materia.setGeometry(QRect(450, 70, 47, 13))

        self.btn_incluir = QPushButton(self)
        self.btn_incluir.setObjectName(u"btnIncluir")
        self.btn_incluir.setGeometry(QRect(450, 400, 231, 23))
        self.btn_incluir.clicked.connect(self.incluir)

        self.btn_salvar = QPushButton(self)
        self.btn_salvar.setObjectName(u"btnSalvar")
        self.btn_salvar.setGeometry(QRect(570, 430, 111, 23))
        self.btn_salvar.clicked.connect(self.salvar)
        self.btn_salvar.setEnabled(False)

        self.btn_alterar = QPushButton(self)
        self.btn_alterar.setObjectName(u"btnAlterar")
        self.btn_alterar.setGeometry(QRect(450, 430, 111, 23))
        self.btn_alterar.clicked.connect(self.alterar)
        self.btn_alterar.setEnabled(False)

        self.btn_excluir = QPushButton(self)
        self.btn_excluir.setObjectName(u"btnExcluir")
        self.btn_excluir.setGeometry(QRect(450, 460, 231, 23))
        self.btn_excluir.clicked.connect(self.excluir)
        self.btn_excluir.setEnabled(False)

        self.btn_cancelar = QPushButton(self)
        self.btn_cancelar.setObjectName(u"btnCancelar")
        self.btn_cancelar.setGeometry(QRect(450, 509, 231, 23))
        self.btn_cancelar.clicked.connect(self.cancelar)
        self.btn_cancelar.setEnabled(False)

        self.txt_consultar = QLineEdit(self)
        self.txt_consultar.setObjectName(u"txtConsultar")
        self.txt_consultar.setGeometry(QRect(10, 540, 342, 20))

        self.btn_consultar = QPushButton(self)
        self.btn_consultar.setObjectName(u"btnConsultar")
        self.btn_consultar.setGeometry(QRect(360, 539, 82, 23))
        self.btn_consultar.clicked.connect(self.consultar_botao)

        self.cbo_materia = QComboBox(self)
        self.cbo_materia.setObjectName(u"cboMateria")
        self.cbo_materia.setGeometry(QRect(450, 90, 231, 22))
        self.cbo_materia.setEnabled(False)

        self.date_entrega = QDateEdit(self)
        self.date_entrega.setObjectName(u"dateEntrega")
        self.date_entrega.setGeometry(QRect(450, 150, 81, 22))
        self.date_entrega.setEnabled(False)
        self.reset_data()

        self.lbl_data_entrega = QLabel(self)
        self.lbl_data_entrega.setObjectName(u"lblDataEntrega")
        self.lbl_data_entrega.setGeometry(QRect(450, 130, 91, 16))

        self.lbl_situacao = QLabel(self)
        self.lbl_situacao.setObjectName(u"lblSituacao")
        self.lbl_situacao.setGeometry(QRect(450, 190, 47, 13))

        self.cbo_situacao = QComboBox(self)
        self.cbo_situacao.setObjectName(u"cboSituacao")
        self.cbo_situacao.setGeometry(QRect(450, 210, 231, 22))
        self.cbo_situacao.setEnabled(False)

        self.lbl_arquivo = QLabel(self)
        self.lbl_arquivo.setObjectName(u"lblArquivo")
        self.lbl_arquivo.setGeometry(QRect(451, 250, 41, 16))

        self.lbl_nome_arquivo = QLabel(self)
        self.lbl_nome_arquivo.setObjectName(u"lblNomeArquivo")
        self.lbl_nome_arquivo.setGeometry(QRect(500, 252, 500, 13))

        self.btn_incluir_arquivo = QPushButton(self)
        self.btn_incluir_arquivo.setObjectName(u"btnIncluirArquivo")
        self.btn_incluir_arquivo.clicked.connect(self.get_arquivo)
        self.btn_incluir_arquivo.setGeometry(QRect(450, 270, 61, 23))
        self.btn_incluir_arquivo.setEnabled(False)

        self.btn_visualizar_arquivo = QPushButton(self)
        self.btn_visualizar_arquivo.setObjectName(u"btnVisualizarArquivo")
        self.btn_visualizar_arquivo.setGeometry(QRect(530, 270, 71, 23))
        self.btn_visualizar_arquivo.clicked.connect(self.abrir_arquivo)
        self.btn_visualizar_arquivo.setEnabled(False)

        self.btn_baixar_arquivo = QPushButton(self)
        self.btn_baixar_arquivo.setObjectName(u"btnBaixarArquivo")
        self.btn_baixar_arquivo.setGeometry(QRect(620, 270, 61, 23))
        self.btn_baixar_arquivo.clicked.connect(self.baixar_arquivo)
        self.btn_baixar_arquivo.setEnabled(False)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

        self.show()

        self.carregar_combo_situacao_atividade()
        self.carregar_combo_materia()

    def reset_data(self):
        hoje = date.today().strftime("%d/%m/%Y")
        self.date_entrega.setDate(QDate.fromString(hoje, "dd/MM/yyyy"))

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate

        self.setWindowTitle(_translate("Atividades", u"Atividades", None))
        self.lblDescricao.setText(_translate("Form", u"Descrição", None))
        self.lbl_materia.setText(_translate("Form", u"Matéria", None))
        self.btn_incluir.setText(_translate("Form", u"Incluir", None))
        self.btn_salvar.setText(_translate("Form", u"Salvar", None))
        self.btn_alterar.setText(_translate("Form", u"Alterar", None))
        self.btn_excluir.setText(_translate("Form", u"Excluir", None))
        self.btn_cancelar.setText(_translate("Form", u"Cancelar", None))
        self.btn_consultar.setText(_translate("Form", u"Consultar", None))
        self.lbl_data_entrega.setText(_translate("Form", u"Data Entrega", None))
        self.lbl_situacao.setText(_translate("Form", u"Situação", None))
        self.lbl_arquivo.setText(_translate("Form", u"Arquivo: ", None))
        self.btn_incluir_arquivo.setText(_translate("Form", u"Incluir", None))
        self.btn_visualizar_arquivo.setText(_translate("Form", u"Visualizar", None))
        self.btn_baixar_arquivo.setText(_translate("Form", u"Baixar", None))
        self.lbl_nome_arquivo.setText("")

    def get_arquivo(self):
        caminho = QtWidgets.QFileDialog.getOpenFileName(self, 'Incluir Arquivo', QtCore.QDir.currentPath(), '*.pdf')
        nomeArquivo = caminho[0].split("/")
        indexNomeArquivo = nomeArquivo[len(nomeArquivo) - 1]

        self.lbl_nome_arquivo.setText(indexNomeArquivo)
        self.arquivo_temporario = caminho[0]

    def abrir_arquivo(self):

        if self.arquivo_temporario:
            os.startfile(self.arquivo_temporario)
        elif self.atividade.getArquivo():
            os.startfile(FILES_DIR + "/" + self.atividade.getArquivo())
        else:
            self.show_mensagem("Arquivo não cadastrado!", QMessageBox.Warning)

    def baixar_arquivo(self):
        caminho_selecionado = str(QtWidgets.QFileDialog.getExistingDirectory(self, 'Baixar Arquivo'))

        if not caminho_selecionado:
            return

        try:
            arquivo = self.arquivo_temporario if self.arquivo_temporario else FILES_DIR + "/" + self.atividade.getArquivo()

            if arquivo:
                self.arquivo_service.copia_arquivo(caminho_selecionado, arquivo)
                self.show_mensagem("Baixado com sucesso!", QMessageBox.Information)

        except Exception as ex:
            self.show_mensagem("Erro ao baixar arquivo!", QMessageBox.Critical)

    def carregar_combo_situacao_atividade(self):
        for situacao in SituacaoAtividade:
            self.cbo_situacao.addItem(situacao.value[1], situacao.value[0])

        self.cbo_situacao.setCurrentIndex(self.cbo_situacao.findData(SituacaoAtividade.NAO_ENTREGUE.value[0]))

    def carregar_combo_materia(self):
        try:
            materias = self.materia_service.consultaMaterias("")
        except:
            self.show_mensagem("Nenhuma matéria cadastrada! Cadastre uma matéria!", QMessageBox.Information)
            self.close()
            return

        for materia in materias:
            self.cbo_materia.addItem(materia[1], materia[0])

    def consultar_botao(self):
        self.consultar(True)

    def consultar(self, verifica_consulta_vazia: bool):
        filtros = self.txt_consultar.text()

        try:
            self.lista_atividades = self.atividade_service.consulta_atividades(filtros)

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
        modelDados = TableModelAtividade(self.lista_atividades)
        modeloOrdenado = QSortFilterProxyModel()
        modeloOrdenado.setSourceModel(modelDados)
        self.list_view.setModel(modeloOrdenado)

        self.list_view.setColumnHidden(0, True)
        self.list_view.setColumnHidden(1, True)
        self.list_view.setColumnHidden(2, True)
        self.list_view.setColumnHidden(3, True)

        self.list_view.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

    def salvar(self):

        try:
            self.valida_descricao_vazia()
        except ValueError as ve_ex:

            mensagem = ve_ex.args[0]
            self.show_mensagem(mensagem, QMessageBox.Critical)
            return

        self.atividade.setDescricao(self.txt_descricao.text())
        self.atividade.setDataEntrega(self.date_entrega.date().toString("dd/MM/yyyy"))
        self.atividade.setSituacao(SituacaoAtividade.getById(self.cbo_situacao.currentData()))

        if self.arquivo_temporario:
            self.atividade.setArquivo(self.arquivo_temporario)

        materia = Materia.criaMateriaComId(self.cbo_materia.currentData(), "", "")
        self.atividade.setMateria(materia)

        try:
            if self.atividade.getId() is None:
                self.salvar_incluir()
            else:
                self.salvar_alterar()

        except ValueError as ve_ex:
            mensagem = ve_ex.args[0]
            self.show_mensagem(mensagem, QMessageBox.Critical)
            return

        self.txt_descricao.setText("")
        self.reset_data()
        self.habilita_consulta()

        self.txt_descricao.setEnabled(False)
        self.date_entrega.setEnabled(False)
        self.btn_baixar_arquivo.setEnabled(False)
        self.btn_incluir_arquivo.setEnabled(False)
        self.btn_visualizar_arquivo.setEnabled(False)
        self.cbo_materia.setEnabled(False)
        self.cbo_situacao.setEnabled(False)
        self.btn_salvar.setEnabled(False)
        self.btn_cancelar.setEnabled(False)

        self.btn_incluir.setEnabled(True)

        self.arquivo_temporario = ""
        self.list_view.viewport().installEventFilter(self)

    def salvar_incluir(self):
        tem_descricao_repetida = self.atividade_service.valida_descricao_igual_incluir(self.atividade)

        if tem_descricao_repetida:
            return True

        self.atividade_service.cadastra_atividade(self.atividade)

    def salvar_alterar(self):
        self.atividade_service.valida_descricao_igual_alterar(self.atividade)

        self.atividade_service.altera_atividade(self.atividade)

        mensagem = "A atividade {} foi alterada com sucesso!".format(self.atividade.getDescricao())
        self.show_mensagem(mensagem, QMessageBox.Information)

        return False

    def incluir(self):
        self.list_view.viewport().removeEventFilter(self)
        self.desabilita_consulta()

        self.btn_alterar.setEnabled(False)
        self.btn_excluir.setEnabled(False)
        self.btn_incluir.setEnabled(False)
        self.lbl_nome_arquivo.setText("Não cadastrado.")

        self.txt_descricao.setEnabled(True)
        self.btn_salvar.setEnabled(True)
        self.btn_cancelar.setEnabled(True)
        self.btn_incluir_arquivo.setEnabled(True)
        self.btn_visualizar_arquivo.setEnabled(True)
        self.btn_baixar_arquivo.setEnabled(True)
        self.cbo_materia.setEnabled(True)
        self.date_entrega.setEnabled(True)
        self.cbo_situacao.setEnabled(True)

        self.atividade = Atividade(None, None, None, None, None)

    def alterar(self):
        self.list_view.viewport().removeEventFilter(self)
        self.txt_descricao.setEnabled(True)
        self.cbo_materia.setEnabled(True)
        self.date_entrega.setEnabled(True)
        self.cbo_situacao.setEnabled(True)
        self.btn_visualizar_arquivo.setEnabled(True)
        self.btn_incluir_arquivo.setEnabled(True)
        self.btn_baixar_arquivo.setEnabled(True)
        self.btn_salvar.setEnabled(True)
        self.btn_cancelar.setEnabled(True)

        self.btn_incluir.setEnabled(False)
        self.btn_alterar.setEnabled(False)
        self.btn_excluir.setEnabled(False)
        self.desabilita_consulta()

        index = self.list_view.currentIndex()
        id_atividade = self.list_view.model().index(index.row(), 0).data()
        nome_arquivo = self.list_view.model().index(index.row(), 1).data()
        id_situacao = self.list_view.model().index(index.row(), 3).data()
        descricao_atividade = self.list_view.model().index(index.row(), 4).data()
        data_entrega = self.list_view.model().index(index.row(), 7).data()

        id_materia = self.list_view.model().index(index.row(), 2).data()
        descricao_materia = self.list_view.model().index(index.row(), 4).data()

        self.txt_descricao.setText(descricao_atividade)

        if not nome_arquivo:
            self.lbl_nome_arquivo.setText("Não cadastrado.")
        else:
            self.lbl_nome_arquivo.setText(nome_arquivo)

        self.date_entrega.setDate(QDate.fromString(data_entrega, "dd/MM/yyyy"))

        self.cbo_materia.setCurrentIndex(self.cbo_materia.findData(id_materia))
        self.cbo_situacao.setCurrentIndex(self.cbo_situacao.findData(id_situacao))

        materia = Materia.criaMateriaComId(id_materia, descricao_materia, "")
        situacao = SituacaoAtividade.getById(id_situacao)

        self.atividade = Atividade.criaAtividadeComId(id_atividade, descricao_atividade,
                                                      data_entrega, materia, situacao, nome_arquivo)

    def cancelar(self):
        mensagem = "Deseja realmente cancelar a operação? Todas as alterações serão perdidas!"
        titulo = "Deseja cancelar?"
        deseja_cancelar = self.show_mensagem_confirma(mensagem, titulo)

        if deseja_cancelar == QMessageBox.Yes:
            self.list_view.viewport().installEventFilter(self)
            self.habilita_consulta()

            self.lbl_nome_arquivo.setText("")
            self.txt_descricao.setText("")
            self.arquivo_temporario = ""

            self.txt_descricao.setEnabled(False)
            self.btn_salvar.setEnabled(False)
            self.btn_incluir.setEnabled(True)
            self.btn_cancelar.setEnabled(False)
            self.cbo_materia.setEnabled(False)
            self.date_entrega.setEnabled(False)
            self.cbo_situacao.setEnabled(False)
            self.btn_visualizar_arquivo.setEnabled(False)
            self.btn_incluir_arquivo.setEnabled(False)
            self.btn_baixar_arquivo.setEnabled(False)
            self.list_view.clearSelection()

            self.reset_data()

    def eventFilter(self, obj, event):
        if obj is self.list_view.viewport():
            if event.type() == QtCore.QEvent.MouseButtonPress:
                if event.button() == QtCore.Qt.LeftButton and event.button():
                    self.btn_alterar.setEnabled(True)
                    self.btn_excluir.setEnabled(True)

            if event.type() == QtCore.QEvent.MouseButtonDblClick:
                self.alterar()

        if obj is self.txt_consultar:
            if event.type() == QtCore.QEvent.KeyPress:
                if event.key() == QtCore.Qt.Key_Enter or event.key() == QtCore.Qt.Key_Return:
                    self.consultar(True)

        return super().eventFilter(obj, event)

    def closeEvent(self, event):
        self.parent_frame.btnAtividades.setEnabled(True)

    def show_mensagem(self, mensagem: str, icone):
        msg_box = QMessageBox()
        msg_box.setIcon(icone)
        msg_box.setText(mensagem)
        msg_box.setWindowFlag(QtCore.Qt.FramelessWindowHint)

        msg_box.exec_()

    def valida_descricao_vazia(self):
        if not self.txt_descricao.text().strip():
            raise ValueError("A descrição não pode ser vazia!")

    def excluir(self):
        index = self.list_view.currentIndex()
        id_atividade = self.list_view.model().index(index.row(), 0).data()
        descricao_atividade = self.list_view.model().index(index.row(), 4).data()

        self.atividade = Atividade.criaAtividadeComId(id_atividade, descricao_atividade, None, None, None, None)

        mensagem = "Deseja realmente excluir a atividade " + self.atividade.getDescricao() + "?"
        titulo = "Deseja excluir?"
        deseja_excluir = self.show_mensagem_confirma(mensagem, titulo)

        if deseja_excluir == QMessageBox.No:
            return

        try:
            self.atividade_service.exclui_atividade(self.atividade)
        except ValueError as ve_ex:
            mensagem = ve_ex.args[0]
            self.show_mensagem(mensagem, QMessageBox.Information)
            return

        #self.desabilita_txts()

        mensagem = "A atividade {} foi excluida com sucesso!".format(self.atividade.getDescricao())
        self.show_mensagem(mensagem, QMessageBox.Information)

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

    def desabilita_consulta(self):
        self.btn_consultar.setEnabled(False)
        self.txt_consultar.setEnabled(False)

    def habilita_consulta(self):
        self.btn_consultar.setEnabled(True)
        self.txt_consultar.setEnabled(True)


class TableModelAtividade(QtCore.QAbstractTableModel):
    def __init__(self, data):
        self.columns = ["id", "arquivo", "id materia", "id_situacao", "Descrição", "Matéria", "Situação", "Data Entrega"]
        super(TableModelAtividade, self).__init__()

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
