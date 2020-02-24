import time
import requests
import pandas as pd
from bs4 import BeautifulSoup
import json
import os
import zipfile

class Scraping():

    def __init__(self, url, endereco=None):
        super().__init__()

        if endereco is None:
            endereco = os.path.basename(url.split("?")[0])

        #Download do arquivo, o escrevendo em disco e substituindo caso exista.
        resposta = requests.get(url)
        if resposta.status_code == requests.codes.OK:
            with open(endereco, 'wb') as novo_arquivo:
                    novo_arquivo.write(resposta.content)
            print("Download finalizado!")
        else:
            print("Erro no download")
            resposta.raise_for_status()

    def extrairZip(self, nome_zip, nome_html):

        # Busca o arquivo zip, extrai o HTML necessário e fecha o arquivo.
        arquivo = zipfile.ZipFile(nome_zip)
        arquivo.extract(nome_html)
        arquivo.close()

    def inserirHtmlVar(self, nome_html):
        
        #Lê o HTML, insere em uma variável e a retorna
        ref_arquivo = open(nome_html,"r")
        string_arquivo = ref_arquivo.read()
        ref_arquivo.close()

        return string_arquivo

    def tratarHTML(self, string):
        
        #Faz o parsing do arquivo para HTML e o transforma em uma estrutura python e a retorna.
        soup = BeautifulSoup(string, 'html.parser')
        tabela = soup.find(name='table')

        #lê o html e transforma novamente em string
        #use .head(NUMERO_QUALQUER) para buscar somente os primeiros NUMERO_QUALQUER resultados
        #pd.read_html(str(tabela))[0].head(10)
        return pd.read_html(str(tabela))[0]

    def transformarDictToJSON(self, dicionario, nome_json):

        json_file = json.dumps(dicionario)
        fp = open(nome_json, 'w')
        fp.write(json_file)
        fp.close

    def removerArquivos(self, arquivos):

        for arquivo in arquivos:
            os.remove(arquivo)
