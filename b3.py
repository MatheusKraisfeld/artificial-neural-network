import tensorflow as tf
from tensorflow import keras

#arq = open('COTAHIST_A2020.txt','r')

# header 00
# trailer 99
# valor dos ativos 01

#posDataPregao = [2, 10]
datasPregao = []
#posNomeResumido = [27, 39]
nomesResumidos = []
#posPrecoAbertura = [56, 69]
precosAbertura = []
#posPrecoFechamento = [108, 121]
precosFechamento = []

with open("COTAHIST_A2020.txt") as file:
    for line in file:
        if line[0:2] != '00' and line[0:2] != '99':
            datasPregao.append(line[2:10])
            nomesResumidos.append(line[27:39])
            precosAbertura.append(line[56:69])
            precosFechamento.append(line[108:121])

ativos = []
ativos.append(datasPregao)
ativos.append(nomesResumidos)
ativos.append(precosAbertura)
ativos.append(precosFechamento)

print('Data do pregao: ', ativos[0][1])
print('Nome resumido da empresa: ', ativos[1][1])
print('Preco de abertura: ', ativos[2][1])
print('Preco de fechamento: ', ativos[3][1])