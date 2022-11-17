# -*- coding: utf-8 -*-
from banco.LogDao import LogDao
from banco.MateriaDao import MateriaDao
from model.Atividade import Atividade
from model.Materia import Materia
from service.AtividadeService import AtividadeService


class MateriaService:

    __atividadeService = None
    __materiaDao = None
    __log_service = None
    
    def __init__(self):
        self.__materiaDao = MateriaDao()
        self.__atividadeService = AtividadeService()
        self.__log_dao = LogDao()
        
    def cadastraMateria(self, materia: Materia):
        id_materia = self.__materiaDao.cadastraMateria(materia)

        self.__log_dao.cadastraLog("INCLUSÃO DE MATÉRIA", id_materia)

    def consultaMaterias(self, filtro: str):
        lista_materias = self.__materiaDao.consultaMaterias(filtro)

        if len(lista_materias) < 1:
            raise ValueError("Nenhuma matéria encontrada!", "Erro")

        return lista_materias

    def consultaMateria(self, materia: Materia):
        materia = self.__materiaDao.consultaMateria(materia)

        return materia

    def alteraMateria(self, materia: Materia):
        self.__materiaDao.alteraMateria(materia)

        self.__log_dao.cadastraLog("ALTERAÇÃO DE MATÉRIA", materia.getId())

    def excluiMateria(self, materia: Materia):
        materia_validada = self.consultaMateria(materia.getId())

        if materia_validada is None:
            raise ValueError("Matéria já excluida!")

        atividades = self.__atividadeService.consulta_atividade_by_id_materia(materia.getId())

        if atividades is not None:
            for atividade in atividades:
                atividade = Atividade.criaAtividadeComId(atividade, None, None, None, None, None)
                self.__atividadeService.exclui_atividade(atividade)

        self.__materiaDao.excluiMateria(materia)

        self.__log_dao.cadastraLog("EXCLUSÃO DE MATÉRIA", materia.getId())

    def valida_descricao_igual_incluir(self, materia: Materia):
        is_igual = self.__materiaDao.retorna_descricao_materia_igual_incluir(materia)

        self.retorna_excecao_descricao_igual(is_igual)

    def valida_descricao_igual_alterar(self, materia: Materia):
        is_igual = self.__materiaDao.retorna_descricao_materia_igual_alterar(materia)

        self.retorna_excecao_descricao_igual(is_igual)

    def retorna_excecao_descricao_igual(self, is_igual: bool):

        if len(is_igual) > 0:
            raise ValueError("Não foi possível salvar! Essa matéria já existe!", "Descrição repetida!")

