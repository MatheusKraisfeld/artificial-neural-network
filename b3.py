import csv
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow import keras

class Layout:
    "Classe contendo o posicionamento de cada dado presente na serie historica da B3"
    # Header
    header = '00' # Tipo de registro header possui valor fixo iniciando com 00
    posNomeDoArquivoHeader = [2, 15] # Fixo COTAHIST.AAAA
    posCodigoDaOrigemHeader = [15, 23] # Fixo BOVESPA
    posDataDaGeracaoHeader = [23, 31] # Formato AAAAMMDD
    posReservaHeader = [31, 245] # Espaco preenchido com brancos

    # Trailer 
    trailer = '99' # Tipo de registro trailer possui valor fixo iniciando com 99
    posNomeDoArquivoTrailer = [2, 15] # Fixo COTAHIST.AAAA
    posCodigoDaOrigemTrailer = [15, 23] # Fixo BOVESPA
    posDataDaGeracaoTrailer = [23, 31] # Formato AAAAMMDD
    posTotalRegistros = [31, 42] # Total de registros incluindo header e trailer
    posReservaTrailer = [42, 245] # Espaco preenchido com brancos

    # Cotacoes historicas por papel-mercado
    posTIPREG = [0, 2] # Tipo de registro
    posDataPregao = [2, 10] # Data do pregao
    posCODBDI = [10, 12] # Codigo BDI
    posCODNEG = [12, 24] # Codigo de negociacao do papel
    posTPMERC = [24, 27] # Tipo de mercado
    posNOMRES = [27, 39] # Nome resumido da empresa emissora do papel
    posESPECI = [39, 49] # Especificado do papel
    posPRAZOT = [49, 52] # Prazo em dias do mercado a termo
    posMODREF = [52, 56] # Moeda de referencia
    posPREABE = [56, 69] # Preco de abertura do papel-mercado no pregao
    posPREMAX = [69, 82] # Preco maximo do papel-mercado no pregao
    posPREMIN = [82, 95] # Preco minimo do papel-mercado no pregao
    posPREMED = [95, 108] # Preco medio do papel-mercado no pregao
    posPREULT = [108, 121] # Preco do ultimo negocio do papel-mercado no pregao
    posPREOFC = [121, 134] # Preco da melhor oferta de compra do papel-mercado
    posPREOFV = [134, 147] # Preco da melhor oferta de venda do papel-mercado
    posTOTNEG = [147, 152] # Numero de negocios efetuados com o papel-mercado no pregao
    posQUATOT = [152, 170] # Quantidade de titulos negociados neste papel-mercado
    posVOLTOT = [170, 188] # Volume de titulos negociados neste papel-mercado
    posPREEXE = [188, 201] # Preco de exercicio para o mercado de opcoes ou valor do contrato para o mercado de termo secundario
    posINDOPC = [201, 202] # Indicador de correcao de precos de exercicios ou valores de contrato para os mercados de opcoes ou termo secundario
    posDATVEN = [202, 210] # Data do vencimento para os mercados de opcoes ou termo secundario
    posFATCOT = [210, 217] # Fator de cotacao do papel
    posPTOEXE = [217, 230] # Preco de exercicio em pontos para opcoes referenciadas em dolar ou valor de contrato em pontos para termo secundario
    posCODISI = [230, 242] # Codigo do papel no sistema ISIN ou codigo interno do papel
    posDISMES = [242, 245] # Numero de distribuicao do papel

# header 00
# trailer 99
# valor dos ativos 01

datasPregao = []
CODBDI = []
CODNEG = []
TPMERC = []
NOMRES = []
ESPECI = []
PRAZOT = []
MODREF = []
PREABE = []
PREMAX = []
PREMIN = []
PREMED = []
PREULT = []
PREOFC = []
PREOFV = []
TOTNEG = []
QUATOT = []
VOLTOT = []
PREEXE = []
INDOPC = []
DATVEN = []
FATCOT = []
PTOEXE = []
CODISI = []
DISMES = []

# arquivo txt contendo a serie historica disponivel em:
# http://www.b3.com.br/pt_br/market-data-e-indices/servicos-de-dados/market-data/historico/mercado-a-vista/series-historicas/
with open("../COTAHIST_A2020.txt") as file: 
    for line in file:
        # desconsidera header e trailer
        if line[Layout.posTIPREG[0]:Layout.posTIPREG[1]] != Layout.header and line[Layout.posTIPREG[0]:Layout.posTIPREG[1]] != Layout.trailer:
            # para salvar qualquer outro dado da serie, basta seguir o modelo abaixo 
            if 'AAPL34 ' in line[Layout.posCODNEG[0]:Layout.posCODNEG[1]]:
                datasPregao.append(line[Layout.posDataPregao[0]:Layout.posDataPregao[1]])
                NOMRES.append(line[Layout.posNOMRES[0]:Layout.posNOMRES[1]])
                PREABE.append(line[Layout.posPREABE[0]:Layout.posPREABE[1]])
                PREULT.append(line[Layout.posPREULT[0]:Layout.posPREULT[1]])
            
with open('apple-stocks-2020.csv', 'w', newline='') as file:
    fieldnames = ['data', 'preco de abertura', 'preco do ultimo negocio']
    writer = csv.DictWriter(file, fieldnames=fieldnames)

    writer.writeheader()
    for i in range(0, len(datasPregao)):
        writer.writerow({'data': datasPregao[i], 'preco de abertura': PREABE[i], 'preco do ultimo negocio': PREULT[i]})

# Load CSV data into a dataframe
dataframe = pd.read_csv('apple-stocks-2020.csv', index_col = 'data')
# Add to predict column (adjusted close) and shift it. This is our output
dataframe['output'] = dataframe.adjusted_close.shift(-1)
# Remove NaN on the final sample (because we don't have tomorrow's output)
dataframe = dataframe.dropna()