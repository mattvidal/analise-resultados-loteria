import time
import requests
import pandas as pd
from bs4 import BeautifulSoup
import json
import os
import zipfile
from pathlib import Path
from Produto import *

class Scraping():

    def __init__(self, url, endereco=None):
        super().__init__()

        #Verifica se a pasta existe. Senão existir, ele cria sozinho.
        output_dir = Path('Dados')

        output_dir.mkdir(parents=True, exist_ok=True)

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

        #remove o zip
        self.removerArquivos([nome_zip])

    def inserirHtmlVar(self, nome_html):
        
        #Lê o HTML, insere em uma variável e a retorna
        ref_arquivo = open(nome_html,"r")
        string_arquivo = ref_arquivo.read()
        ref_arquivo.close()

        #remove o htm
        self.removerArquivos([nome_html])

        return string_arquivo

    def tratarHTML(self, string):
        
        #Faz o parsing do arquivo para HTML e o transforma em uma estrutura python e a retorna.
        soup = BeautifulSoup(string, 'html.parser')
        tabela = soup.find(name='table')

        #lê o html e transforma novamente em string
        #use .head(NUMERO_QUALQUER) para buscar somente os primeiros NUMERO_QUALQUER resultados
        #pd.read_html(str(tabela))[0].head(10)
        return pd.read_html(str(tabela))[0]

    def removerArquivos(self, arquivos):

        for arquivo in arquivos:
            os.remove(arquivo)

def BaixaArquivos():

    lista_produtos = []

    lista_produtos.append(Produto("mega_sena", "http://www1.caixa.gov.br/loterias/_arquivos/loterias/D_megase.zip", "D_megase.zip", "d_mega.htm"))
    lista_produtos.append(Produto("lotofacil", "http://www1.caixa.gov.br/loterias/_arquivos/loterias/D_lotfac.zip", "D_lotfac.zip", "d_lotfac.htm"))
    lista_produtos.append(Produto("quina", "http://www1.caixa.gov.br/loterias/_arquivos/loterias/D_quina.zip", "D_quina.zip", "d_quina.htm"))
    lista_produtos.append(Produto("lotomania", "http://www1.caixa.gov.br/loterias/_arquivos/loterias/D_lotoma.zip", "D_lotoma.zip", "d_lotman.htm"))
    lista_produtos.append(Produto("timemania", "http://www1.caixa.gov.br/loterias/_arquivos/loterias/D_timema.zip", "D_timema.zip", "d_timema.htm"))
    lista_produtos.append(Produto("dupla_sena", "http://www1.caixa.gov.br/loterias/_arquivos/loterias/d_dplsen.zip", "d_dplsen.zip", "d_dplsen.htm"))

    for lista in lista_produtos:

        web = Scraping(lista.url_zip)

        web.extrairZip(lista.nome_zip, lista.nome_html)

        string = web.inserirHtmlVar(lista.nome_html)

        conteudo = web.tratarHTML(string) 

        conteudo.to_csv('Dados/' + lista.produto + '.csv', sep=';', encoding='utf-8', index=False)
    
BaixaArquivos()