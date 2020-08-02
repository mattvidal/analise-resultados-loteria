import time
import requests
import pandas as pd
from bs4 import BeautifulSoup
import json
import os
import sys
import zipfile
from pathlib import Path
from Produto import *

class Scraping():

    def __init__(self, item, endereco=None):
        super().__init__()

        self.item = item

        #Verifica se a pasta existe. Senão existir, ele cria sozinho.
        output_dir = Path('Dados')

        output_dir.mkdir(parents=True, exist_ok=True)

        if endereco is None:
            endereco = os.path.basename(self.item.url_zip.split("?")[0])

        try:
            #Download do arquivo, o escrevendo em disco e substituindo caso exista.
            resposta = requests.get(self.item.url_zip)
            if resposta.status_code == requests.codes.OK:
                with open(endereco, 'wb') as novo_arquivo:
                        novo_arquivo.write(resposta.content)
                print("Download de " + self.item.produto + " realizado com sucesso!")
            else:
                print("Erro no download")
                resposta.raise_for_status()
        except:
            print("Ocorreu um erro ao baixar o arquivo " + self.item.produto)

    def iniciar(self):
        
        self.__extrairZip(self.item.nome_zip, self.item.nome_html)
        string = self.__inserirHtmlVar(self.item.nome_html)
        df = self.__tratarHTML(string)
        self.__salvarCSV(df, self.item.produto)

        
    def __extrairZip(self, nome_zip, nome_html):

        try:
            # Busca o arquivo zip, extrai o HTML necessário e fecha o arquivo.
            arquivo = zipfile.ZipFile(nome_zip)
            arquivo.extract(nome_html)
            arquivo.close()
            
        except:
            print("Ocorreu um erro ao extrair o arquivo " + nome_zip)
            sys.exit()

        #remove o zip
        self.__removerArquivos([nome_zip])

    def __inserirHtmlVar(self, nome_html):
        
        try:
            #Lê o HTML, insere em uma variável e a retorna
            ref_arquivo = open(nome_html,"r")
            string_arquivo = ref_arquivo.read()
            ref_arquivo.close()
            
            #remove o htm
            self.__removerArquivos([nome_html])
        except:
            print("Ocorreu um erro ao inserir o html de nome " + nome_html + " na variável para manipulação")
            sys.exit()

        return string_arquivo

    def __tratarHTML(self, string):
        
        try:
            #Faz o parsing do arquivo para HTML e o transforma em uma estrutura python e a retorna.
            soup = BeautifulSoup(string, 'html.parser')
            tabela = soup.find(name='table')
            
            #lê o html e transforma novamente em string
            #use .head(NUMERO_QUALQUER) para buscar somente os primeiros NUMERO_QUALQUER resultados
            #pd.read_html(str(tabela))[0].head(10)
        except:
            print("Ocorreu um erro tratar html")
            sys.exit()
            
        return pd.read_html(str(tabela))[0]

    def __removerArquivos(self, arquivos):

        try:
            for arquivo in arquivos:
                os.remove(arquivo)
                
        except:
            print("Ocorreu um erro ao remover o arquivo " + arquivo)
            sys.exit()

    def __salvarCSV(self, df, nome):

        try:
            df.to_csv('Dados/' + nome + '.csv', sep=';', encoding='utf-8', index=False)
            print("O arquivo " + nome + " foi salvo no formato CSV com sucesso!")
        except:
            print("Ocorreu um erro ao salvar o arquivo " + nome + " no formato CSV")
            sys.exit()

def BaixaArquivos():

    lista_produtos = []

    lista_produtos.append(Produto("mega_sena", "http://www1.caixa.gov.br/loterias/_arquivos/loterias/D_megase.zip", "D_megase.zip", "d_mega.htm"))
    lista_produtos.append(Produto("lotofacil", "http://www1.caixa.gov.br/loterias/_arquivos/loterias/D_lotfac.zip", "D_lotfac.zip", "d_lotfac.htm"))
    lista_produtos.append(Produto("quina", "http://www1.caixa.gov.br/loterias/_arquivos/loterias/D_quina.zip", "D_quina.zip", "d_quina.htm"))
    lista_produtos.append(Produto("lotomania", "http://www1.caixa.gov.br/loterias/_arquivos/loterias/D_lotoma.zip", "D_lotoma.zip", "d_lotman.htm"))
    lista_produtos.append(Produto("timemania", "http://www1.caixa.gov.br/loterias/_arquivos/loterias/D_timema.zip", "D_timema.zip", "d_timema.htm"))
    lista_produtos.append(Produto("dupla_sena", "http://www1.caixa.gov.br/loterias/_arquivos/loterias/d_dplsen.zip", "d_dplsen.zip", "d_dplsen.htm"))

    for item in lista_produtos:

        scrap = Scraping(item)

        scrap.iniciar()
        
BaixaArquivos()