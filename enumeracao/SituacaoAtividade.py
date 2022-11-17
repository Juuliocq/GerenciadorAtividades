from enum import Enum


class SituacaoAtividade(Enum):

    NAO_ENTREGUE = (1, "NÃO ENTREGUE")
    ENTREGUE = (2, "ENTREGUE")
    CANCELADA = (3, "CANCELADA")

    def getById(id_situacao):
        for situacao in SituacaoAtividade:
            if id_situacao == situacao.value[0]:
                return situacao

        return None
