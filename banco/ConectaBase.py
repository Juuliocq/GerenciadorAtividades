# -*- coding: utf-8 -*-
from sqlite3 import connect

from config.Configs import APP_DATA_DIR
from enumeracao.SituacaoAtividade import SituacaoAtividade


class ConectaBase():
    __cursor = None
    __connection = None
    __database = APP_DATA_DIR + "\gerenciadoratividade"

    def cria_estrutura_banco(self):
        sql_tabela_materia = ("CREATE TABLE IF NOT EXISTS materia(" +
                              "id INTEGER PRIMARY KEY, " +
                              "descricao TEXT NOT NULL, " +
                              "professor TEXT);")

        sql_tabela_atividade = ("CREATE TABLE IF NOT EXISTS atividade(" +
                                "id INTEGER PRIMARY KEY, " +
                                "descricao TEXT NOT NULL, " +
                                "dataentrega TEXT, "
                                "id_materia INTEGER NOT NULL, " +
                                "id_situacaoatividade INTEGER NOT NULL, " +
                                "arquivo TEXT, " +
                                "FOREIGN KEY(id_materia) REFERENCES materia(id), " +
                                "FOREIGN KEY(id_situacaoatividade) REFERENCES situacaoatividade(id))")

        sql_tabela_log = ("CREATE TABLE IF NOT EXISTS log(" +
                          "id INTEGER PRIMARY KEY, " +
                          "descricao TEXT NOT NULL, " +
                          "id_referencia INTEGER NOT NULL, "
                          "datahora TEXT NOT NULL)")

        sql_tabela_situacaoatividade = ("CREATE TABLE IF NOT EXISTS situacaoatividade(" +
                                        "id INTEGER PRIMARY KEY, " +
                                        "descricao TEXT NOT NULL)")

        sql_insert_situacaoatividade = ""

        for situacao in SituacaoAtividade:
            sql_insert_situacaoatividade += ("INSERT INTO situacaoatividade(" +
                                             "id, descricao) VALUES(" +
                                             str(situacao.value[0]) + ", '" +
                                             situacao.value[1] + "');")

        try:
            with connection(self.__database) as conn:

                if self.retorna_linha("SELECT name FROM sqlite_master WHERE type='table' AND name='situacaoatividade'") is None:
                    conn.cursor().execute(sql_tabela_situacaoatividade)
                    conn.cursor().executescript(sql_insert_situacaoatividade)

                conn.cursor().executescript(sql_tabela_materia)
                conn.cursor().execute(sql_tabela_atividade)
                conn.cursor().execute(sql_tabela_log)
        except:
            raise ConnectionError

    def retorna_lista(self, sql: str):
        try:
            with connection(self.__database) as conn:
                conn.cursor().execute(sql)
                lista_result = conn.cursor().fetchall()
        except:
            raise ConnectionError

        return lista_result

    def retorna_linha(self, sql: str):
        try:
            with connection(self.__database) as conn:
                conn.cursor().execute(sql)
                linha_result = conn.cursor().fetchone()
        except:
            raise ConnectionError

        return linha_result

    def insere_altera_exclui(self, sql: str):
        try:
            with connection(self.__database) as conn:
                conn.cursor().execute(sql)
                conn.commit()

                return conn.cursor().lastrowid
        except:
            raise ConnectionError


class connection(object):
    __conn = None
    __cursor = None

    def __init__(self, path):
        self.path = path

    def __enter__(self):
        self.__conn = connect(self.path)
        self.__cursor = self.__conn.cursor()
        self.__cursor.execute("PRAGMA foreign_keys=1")
        return self

    def commit(self):
        self.__conn.commit()

    def cursor(self):
        return self.__cursor

    def __exit__(self, exc_class, exc, traceback):
        self.__cursor.close()
        self.__conn.close()
