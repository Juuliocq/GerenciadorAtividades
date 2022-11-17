import os
import glob
import shutil
from config.Configs import FILES_DIR

class ArquivoService:

    def deleta_arquivo(self, nome_arquivo: str):
        nome_arquivo = nome_arquivo[0] if isinstance(nome_arquivo, tuple) else nome_arquivo

        caminho = FILES_DIR + "\\" + nome_arquivo
        os.remove(caminho)

    def copia_arquivo(self, caminho_a_ser_copiado: str, arquivo):
        for f in glob.glob(arquivo):
            shutil.copy(f, caminho_a_ser_copiado)

    def insere_arquivo(self, caminho_arquivo):
        for f in glob.glob(caminho_arquivo):
            shutil.copy(f, FILES_DIR)

    def abrir_arquivo(self, caminho: str):
        os.startfile(caminho)

