from banco.ConectaBase import ConectaBase


class LogDao:
    __conexao = None

    def __init__(self):
        self.__conexao = ConectaBase()

    def cadastraLog(self, descricao: str, id_referencia: int):
        sql = ("INSERT INTO log(descricao, id_referencia, datahora) VALUES('" +
               descricao + "', '" +
               str(id_referencia) + "', datetime())")

        self.__conexao.insere_altera_exclui(sql)