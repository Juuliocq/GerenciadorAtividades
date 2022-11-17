# -*- coding: utf-8 -*-
"""
Created on Sat Sep 10 08:18:21 2022

@author: julio
"""
from enumeracao.SituacaoAtividade import SituacaoAtividade
from model.Materia import Materia


class Atividade:
    
    __id_atividade = None
    __descricao = ""
    __data_entrega = ""
    __materia = None
    __situacao_atividade = None
    __arquivo = ""
    
    def __init__(self, descricao: str, data_entrega: str, materia: Materia, situacao: SituacaoAtividade, arquivo: str):
        self.__descricao = descricao
        self.__data_entrega = data_entrega
        self.__materia = materia
        self.__situacao_atividade = situacao
        self.__arquivo = arquivo
        
    @classmethod
    def criaAtividadeComId(cls, idA: int, descricao: str, dataEntrega: str, materia: Materia, situacao: SituacaoAtividade, arquivo: str):
        atividade = cls(descricao, dataEntrega, materia, situacao, arquivo)
        atividade.setId(idA)
        
        return atividade
        
    def setId(self, idM: int):
        self.__id_atividade = idM
        
    def getId(self):
        return self.__id_atividade

    def setDescricao(self, descricao: str):
        self.__descricao = descricao
        
    def getDescricao(self):
        return self.__descricao

    def setDataEntrega(self, data: str):
        self.__data_entrega = data
    
    def getDataEntrega(self):
        return self.__data_entrega

    def setMateria(self, materia: Materia):
        self.__materia = materia
    
    def getMateria(self):
        return self.__materia

    def getIdMateria(self):
        return self.__materia.getId()

    def setSituacao(self, situacao: SituacaoAtividade):
        self.__situacao_atividade = situacao

    def getSituacao(self):
        return self.__situacao_atividade

    def getIdSituacao(self):
        return self.__situacao_atividade.value[0]

    def setArquivo(self, arquivo: str):
        self.__arquivo = arquivo

    def getArquivo(self):
        return self.__arquivo
        