from webscraping import *

url_zip = "http://www1.caixa.gov.br/loterias/_arquivos/loterias/D_megase.zip"

baixar_arquivo(url_zip)

mega_file = zipfile.ZipFile('D_megase.zip') #encontra o zip file
mega_file.extract('d_mega.htm') #extrai somente o html necessário
mega_file.close()

ref_arquivo = open("d_mega.htm","r") #lê esse html

string_arquivo = ref_arquivo.read() #insere o html numa variável

soup = BeautifulSoup(string_arquivo, 'html.parser') #faz o parsing do arquivo para html

table = soup.find(name='table') #transforma a table em uma estrutura python

dt_full = pd.read_html(str(table))[0] #lê o html e transforma novamente em string

dicionario = {}

dicionario['jogos'] = dt_full.to_dict('records')

print(dicionario['jogos'])




