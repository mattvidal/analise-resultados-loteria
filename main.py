from Scraping import *

lista_produtos = []

lista_produtos.append(Produto("mega_sena", "http://www1.caixa.gov.br/loterias/_arquivos/loterias/D_megase.zip", "D_megase.zip", "d_mega.htm"))
lista_produtos.append(Produto("lotofacil", "http://www1.caixa.gov.br/loterias/_arquivos/loterias/D_megase.zip", "D_lotfac.zip", "d_mega.htm"))
lista_produtos.append(Produto("quina", "http://www1.caixa.gov.br/loterias/_arquivos/loterias/D_megase.zip", "D_megase.zip", "d_mega.htm"))
lista_produtos.append(Produto("lotomania", "http://www1.caixa.gov.br/loterias/_arquivos/loterias/D_megase.zip", "D_megase.zip", "d_mega.htm"))
lista_produtos.append(Produto("timemania", "http://www1.caixa.gov.br/loterias/_arquivos/loterias/D_megase.zip", "D_megase.zip", "d_mega.htm"))
lista_produtos.append(Produto("dupla_sena", "http://www1.caixa.gov.br/loterias/_arquivos/loterias/D_megase.zip", "D_megase.zip", "d_mega.htm"))
lista_produtos.append(Produto("dia_de_sorte", "http://www1.caixa.gov.br/loterias/_arquivos/loterias/D_megase.zip", "D_megase.zip", "d_mega.htm"))

# BaixaArquivos()



for produto in lista_produtos:
    print(produto.produto)
