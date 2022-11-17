# -*- coding: utf-8 -*-
"""
Created on Sat Sep 10 08:16:10 2022

@author: julio
"""

from banco.ConectaBase import ConectaBase
from model.Atividade import Atividade


class AtividadeDao:
    __conexao = None

    def __init__(self):
        self.__conexao = ConectaBase()

    def cadastraAtividade(self, atividade: Atividade):
        sql = ("INSERT INTO atividade(descricao, dataentrega, id_materia, id_situacaoatividade, arquivo) VALUES('" +
               atividade.getDescricao() + "', '" +
               atividade.getDataEntrega() + "', " +
               str(atividade.getIdMateria()) + ", " +
               str(atividade.getIdSituacao()) + ", '" +
               atividade.getArquivo() + "')")

        return self.__conexao.insere_altera_exclui(sql)

    def consultaAtividades(self, filtro: str):
        sql = ("SELECT a.id, arquivo, id_materia, id_situacaoatividade, a.descricao, m.descricao, sa.descricao, dataentrega FROM atividade a " +
               "INNER JOIN materia m ON a.id_materia = m.id " +
               "INNER JOIN situacaoatividade sa ON sa.id = a.id_situacaoatividade")

        #if filtro:
            #sql += " WHERE descricao LIKE '%" + filtro + "%' OR professor LIKE '%" + filtro + "%'"

        result = self.__conexao.retorna_lista(sql)

        return result

    def consultaAtividade(self, idA: int):
        sql = "SELECT id, descricao, dataentrega, id_materia, id_situacaoatividade, arquivo FROM atividade WHERE id = " + str(idA)

        result = self.__conexao.retorna_linha(sql)

        return result

    def consulta_atividade_by_id_materia(self, id_materia: int):
        sql = "SELECT id FROM atividade WHERE id_materia = " + str(id_materia)

        result = self.__conexao.retorna_linha(sql)

        return result

    def alteraAtividade(self, atividade: Atividade):
        atividade.setArquivo('' if atividade.getArquivo() is None else atividade.getArquivo())

        sql = ("UPDATE atividade SET " +
               "descricao = '" + atividade.getDescricao() + "', " +
               "dataentrega = '" + atividade.getDataEntrega() + "', " +
               "id_materia = " + str(atividade.getIdMateria()) + ", " +
               "id_situacaoatividade = " + str(atividade.getIdSituacao()) + ", " +
                "arquivo = '" + atividade.getArquivo() + "' " +
               "WHERE id = " + str(atividade.getId()))

        self.__conexao.insere_altera_exclui(sql)

    def get_arquivo(self, atividade: Atividade):
        sql = "SELECT arquivo FROM atividade WHERE id = " + str(atividade.getId())

        return self.__conexao.retorna_linha(sql)

    def get_dataentrega(self, atividade: Atividade):
        sql = "SELECT dataentrega FROM atividade WHERE id = " + str(atividade.getId())

        return self.__conexao.retorna_linha(sql)

    def exclui_atividade(self, atividade: Atividade):
        sql = "DELETE FROM atividade WHERE id = " + str(atividade.getId())

        self.__conexao.insere_altera_exclui(sql)

    def retorna_descricao_atividade_igual_incluir(self, atividade: Atividade):
        sql = "SELECT id FROM atividade WHERE descricao = '" + atividade.getDescricao() + "'";

        result = self.__conexao.retorna_lista(sql)

        return result

    def retorna_descricao_atividade_igual_alterar(self, atividade: Atividade):
        sql = "SELECT id FROM atividade WHERE descricao = '" + atividade.getDescricao() + "' AND id <> " + str(atividade.getId())

        result = self.__conexao.retorna_lista(sql)

        return result
