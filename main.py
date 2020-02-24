from webscraping import *

url_zip = "http://www1.caixa.gov.br/loterias/_arquivos/loterias/D_megase.zip"
nome_zip = 'D_megase.zip'
nome_html = 'd_mega.htm'

web = Scraping(url_zip)

web.extrairZip(nome_zip, nome_html)

string = web.inserirHtmlVar(nome_html)

conteudo = web.tratarHTML(string) 

dicionario = {}

dicionario['jogos'] = conteudo.to_dict('records')

web.transformarDictToJSON(dicionario, 'mega_sena.json')

arquivos = [nome_html, nome_zip]

web.removerArquivos([nome_html, nome_zip])




