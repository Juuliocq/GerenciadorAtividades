# -*- coding: utf-8 -*-
"""
Created on Sat Sep 10 08:16:10 2022

@author: julio
"""

from banco.ConectaBase import ConectaBase
from model.Materia import Materia

class MateriaDao:
    
    __conexao = None
    
    def __init__(self):
        self.__conexao = ConectaBase()
        
    def cadastraMateria(self, materia: Materia):
        sql = ("INSERT INTO materia(descricao, professor) VALUES('" +
               materia.getDescricao() + "', '" +
               materia.getProfessor() + "')")

        return self.__conexao.insere_altera_exclui(sql)

    def consultaMaterias(self, filtro: str):
        sql = "SELECT id, descricao, professor from materia"

        if filtro:
            sql += " WHERE descricao LIKE '%" + filtro + "%' OR professor LIKE '%" + filtro + "%'"

        result = self.__conexao.retorna_lista(sql)

        return result

    def consultaMateria(self, idM: int):
        sql = "SELECT id, descricao, professor FROM materia WHERE id = " + str(idM)

        result = self.__conexao.retorna_linha(sql)

        return result

    def alteraMateria(self, materia: Materia):
        sql = ("UPDATE materia SET " +
               "descricao = '" + materia.getDescricao() + "', " +
               "professor = '" + materia.getProfessor() + "'" +
               " WHERE id = " + str(materia.getId()))

        self.__conexao.insere_altera_exclui(sql)

    def excluiMateria(self, materia: Materia):
        sql = "DELETE FROM materia WHERE id = " + str(materia.getId())

        self.__conexao.insere_altera_exclui(sql)

    def retorna_descricao_materia_igual_incluir(self, materia: Materia):
        sql = "SELECT id FROM materia WHERE descricao = '" + materia.getDescricao() + "'";

        result = self.__conexao.retorna_lista(sql)

        return result

    def retorna_descricao_materia_igual_alterar(self, materia: Materia):
        sql = "SELECT id FROM materia WHERE descricao = '" + materia.getDescricao() + "' AND id <> " + str(materia.getId());

        result = self.__conexao.retorna_lista(sql)

        return result