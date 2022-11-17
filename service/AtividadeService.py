# -*- coding: utf-8 -*-
"""
Created on Sat Sep 10 08:15:16 2022

@author: julio
"""
import os.path
from datetime import datetime, date

from banco.AtividadeDao import AtividadeDao
from banco.LogDao import LogDao
from enumeracao.SituacaoAtividade import SituacaoAtividade
from model.Atividade import Atividade
from service.ArquivoService import ArquivoService
from config.Configs import FILES_DIR


class AtividadeService:
    __atividadeDao = None
    __arquivo_service = None
    __log_service = None

    def __init__(self):
        self.__atividadeDao = AtividadeDao()
        self.__arquivo_service = ArquivoService()
        self.__log_dao = LogDao()

    def cadastra_atividade(self, atividade: Atividade):

        self.valida_data_entrega(atividade)

        if atividade.getArquivo():
            caminho_arquivo = atividade.getArquivo()
            lista_caminho_arquivo = caminho_arquivo.split("/")
            nome_arquivo = lista_caminho_arquivo[len(lista_caminho_arquivo) - 1]

            if os.path.exists(FILES_DIR + "/" + nome_arquivo):
                raise ValueError("Arquivo " + nome_arquivo + " já cadastrado. Mude o nome ou escolha outro arquivo!")

            self.__arquivo_service.insere_arquivo(caminho_arquivo)

            atividade.setArquivo(nome_arquivo)
        else:
            atividade.setArquivo("")

        id_atividade = self.__atividadeDao.cadastraAtividade(atividade)

        self.__log_dao.cadastraLog("INCLUSÃO DE ATIVIDADE", id_atividade)

    def altera_atividade(self, atividade: Atividade):

        self.valida_data_entrega(atividade)

        arquivo_previamente_incluso = None if len(self.get_arquivo(atividade)[0]) == 0 else self.get_arquivo(atividade)[0]
        atividade.setArquivo(None if not atividade.getArquivo() else atividade.getArquivo())
        insere_arquivo = False

        if not arquivo_previamente_incluso and atividade.getArquivo():
            insere_arquivo = True
        elif arquivo_previamente_incluso != atividade.getArquivo():
            insere_arquivo = True
            self.__arquivo_service.deleta_arquivo(arquivo_previamente_incluso)

        if insere_arquivo:
            caminho_arquivo = atividade.getArquivo()
            lista_caminho_arquivo = caminho_arquivo.split("/")
            nome_arquivo = lista_caminho_arquivo[len(lista_caminho_arquivo) - 1]

            if os.path.exists(FILES_DIR + "/" + nome_arquivo):
                raise ValueError("Arquivo " + nome_arquivo + " já cadastrado. Mude o nome ou escolha outro arquivo!")

            self.__arquivo_service.insere_arquivo(caminho_arquivo)
            atividade.setArquivo(nome_arquivo)

        self.__atividadeDao.alteraAtividade(atividade)

        self.__log_dao.cadastraLog("ALTERAÇÃO DE ATIVIDADE", atividade.getId())

    def exclui_atividade(self, atividade: Atividade):
        atividade_validada = self.consulta_atividade(atividade.getId())

        if atividade_validada is None:
            raise ValueError("Atividade já excluida!")

        arquivo = self.get_arquivo(atividade)

        if arquivo[0]:
            self.__arquivo_service.deleta_arquivo(arquivo)

        self.__atividadeDao.exclui_atividade(atividade)

        self.__log_dao.cadastraLog("EXCLUSÃO DE ATIVIDADE", atividade.getId())

    def consulta_atividade(self, atividade: Atividade):
        atividade = self.__atividadeDao.consultaAtividade(atividade)

        return atividade

    def consulta_atividade_by_id_materia(self, id_materia):
        atividade = self.__atividadeDao.consulta_atividade_by_id_materia(id_materia)

        return atividade

    def consulta_atividades(self, filtro: str):
        lista_atividades = self.__atividadeDao.consultaAtividades(filtro)

        if len(lista_atividades) < 1:
            raise ValueError("Nenhuma atividade encontrada!", "Erro")

        return lista_atividades

    def valida_descricao_igual_incluir(self, atividade: Atividade):
        is_igual = self.__atividadeDao.retorna_descricao_atividade_igual_incluir(atividade)

        self.retorna_excecao_descricao_igual(is_igual)

    def valida_descricao_igual_alterar(self, atividade: Atividade):
        is_igual = self.__atividadeDao.retorna_descricao_atividade_igual_alterar(atividade)

        self.retorna_excecao_descricao_igual(is_igual)

    def valida_data_entrega(self, atividade: Atividade):

        if atividade.getId() is not None:
            data_entrega_cadastrada = self.__atividadeDao.get_dataentrega(atividade)

            if ((atividade.getSituacao() == SituacaoAtividade.ENTREGUE or atividade.getSituacao() == SituacaoAtividade.CANCELADA)
                    and data_entrega_cadastrada[0] != atividade.getDataEntrega()):
                raise ValueError("Não é possível alterar a data entrega de uma atividade CANCELADA OU ENTREGUE!!")

        hoje = date.today()
        data_entrega = datetime.strptime(atividade.getDataEntrega(), "%d/%m/%Y")

        if data_entrega.date() < hoje:
            raise ValueError("Não é possível cadastrar com a data de entrega menor que hoje!")


    def get_arquivo(self, atividade: Atividade):
        return self.__atividadeDao.get_arquivo(atividade)

    def retorna_excecao_descricao_igual(self, is_igual: bool):

        if len(is_igual) > 0:
            raise ValueError("Não foi possível salvar! Essa matéria já existe!", "Descrição repetida!")
