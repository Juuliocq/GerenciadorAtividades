# -*- coding: utf-8 -*-
"""
Created on Sat Sep 10 08:18:21 2022

@author: julio
"""

class Materia:
    
    __idMateria = None
    __descricao = ""
    __professor = ""
    
    def __init__(self, descricao: str, professor: str):
        self.__descricao = descricao
        self.__professor = professor
        
    @classmethod
    def criaMateriaComId(cls, idM: int, descricao: str, professor: str):
        materia = cls(descricao, professor)
        materia.setId(idM)
        
        return materia
        
    def setId(self, idM: int):
        self.__idMateria = idM

    def setDescricao(self, descricao: str):
        self.__descricao = descricao

    def setProfessor(self, professor: str):
        self.__professor = professor

    def setDescricaoEProfessor(self, descricao: str, professor: str):
        self.__descricao = descricao
        self.__professor = professor

    def getId(self):
        return self.__idMateria
        
    def getDescricao(self):
        return self.__descricao
    
    def getProfessor(self):
        return self.__professor
        
        