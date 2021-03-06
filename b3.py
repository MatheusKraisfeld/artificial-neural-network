# Just disables the warning, doesn't enable AVX/FMA
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import csv
import numpy as np
import pandas as pd
import tensorflow as tf
import sys
from matplotlib import pyplot
from tensorflow import keras
from sklearn import preprocessing
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout, Flatten
from numpy import concatenate

class Layout:
    
    "Classe contendo o posicionamento de cada dado presente na serie historica da B3"
    
    # header 00
    # trailer 99
    # valor dos ativos 01

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

# Split dataframe into dataframes of size 3
def split(df, chunkSize = 3):
    numberChunks = len(df) // chunkSize + 1
    return np.array_split(df, numberChunks, axis=0)

# Split with list comprehension
def otherSplit(df):
    n = 200000  #chunk row size
    list_df = [df[i:i+n] for i in range(0,df.shape[0],n)]
    return list_df

# Split dataframe by row 
def splitByRow(df):
    splits = [df.loc[[i]] for i in df.index]
    return splits

# Create model
def create_model(shapeX, shapeY):
    model = Sequential()
    model.add(Flatten(input_shape = (shapeX, shapeY)))
    model.add(Dense(20, activation='relu', input_dim=2))
    model.add(Dense(1))
    model.compile(optimizer = 'adam', loss='mse')
    return model

# Main
def main():
    flag = 2
    while True:
        #stock = input('Digite o nome do ativo que deseja analisar: ')
        stock = sys.argv[1]
        stock = stock.upper()
        #year = input('Digite o ano da base de dados que deseja analisar: ')
        year = sys.argv[2]
        #ep = tf.cast(z, tf.int64)
        datasPregao = []
        NOMRES = []
        PREABE = []
        PREULT = []
        VOLTOT = []
        PREMAX = []
        PREMIN = []
        # Txt file containing a time series available at:
        # http://www.b3.com.br/pt_br/market-data-e-indices/servicos-de-dados/market-data/historico/mercado-a-vista/series-historicas/
        with open('../COTAHIST_A' + year + '.txt') as file: 
            for line in file:
                # Skip header and trailer
                if line[Layout.posTIPREG[0]:Layout.posTIPREG[1]] != Layout.header and line[Layout.posTIPREG[0]:Layout.posTIPREG[1]] != Layout.trailer:
                    if stock+' ' in line[Layout.posCODNEG[0]:Layout.posCODNEG[1]]:
                        datasPregao.append(line[Layout.posDataPregao[0]:Layout.posDataPregao[1]])
                        #NOMRES.append(line[Layout.posNOMRES[0]:Layout.posNOMRES[1]])
                        PREABE.append(line[Layout.posPREABE[0]:Layout.posPREABE[1]])
                        PREULT.append(line[Layout.posPREULT[0]:Layout.posPREULT[1]])
                        #VOLTOT.append(line[Layout.posVOLTOT[0]:Layout.posVOLTOT[1]])
                        #PREMAX.append(line[Layout.posPREMAX[0]:Layout.posPREMAX[1]])
                        #PREMIN.append(line[Layout.posPREMIN[0]:Layout.posPREMIN[1]])

        with open(stock + '-stocks-' + year + '.csv', 'w', newline='') as file:
            #fieldnames = ['data', 'preco_abertura', 'preco_fechamento', 'volume_total', 'preco_minimo', 'preco_maximo']
            fieldnames = ['data', 'preco_abertura', 'preco_fechamento']
            writer = csv.DictWriter(file, fieldnames=fieldnames)

            writer.writeheader()
            for i in range(0, len(datasPregao)):
                writer.writerow({
                    'data': datasPregao[i], 
                    'preco_abertura': PREABE[i], 
                    'preco_fechamento': PREULT[i], 
                    #'volume_total': VOLTOT[i],
                    #'preco_minimo': PREMIN[i],
                    #'preco_maximo': PREMAX[i]
                    })

        # Load CSV data into a dataframe
        dataframe = pd.read_csv(stock + '-stocks-' + year + '.csv', index_col = 'data')
        # Add to predict column (closing price) and shift it. This is our output
        #dataframe['output'] = dataframe.preco_fechamento.rolling(10).mean()
        dataframe['output'] = dataframe.preco_fechamento.shift(-1)
        # Remove NaN on the final sample (because we don't have tomorrow's output)
        dataframe = dataframe.dropna()
        #dataframe = split(dataframe)

        # Rescale the input values between -1 and 1
        scaler = preprocessing.MinMaxScaler(feature_range=(-1, 1))
        rescaled = scaler.fit_transform(dataframe.values)

        # Split into training/testing
        training_ratio = 0.8 # training = 80% / testing = 20%
        training_testing_index = int(len(rescaled) * training_ratio)
        training_data = rescaled[:training_testing_index] # first element ~ training_testing_index
        testing_data = rescaled[training_testing_index:] # training_testing_index ~ last element

        # Split training into input/output. Output is the one we added to the end
        training_input_data = training_data[:, 0:-1] 
        training_output_data = training_data[:, -1]

        # Split testing into input/output. Output is the one we added to the end
        testing_input_data = testing_data[:, 0:-1]
        testing_output_data = testing_data[:, -1]

        # Reshape data for (Sample, Timesteps, Features)
        training_input_data = training_input_data.reshape(training_input_data.shape[0], 1, training_input_data.shape[1])
        testing_input_data = testing_input_data.reshape(testing_input_data.shape[0], 1, testing_input_data.shape[1])

        if flag == 2:
            tf.keras.backend.clear_session()
            model = create_model(training_input_data.shape[1], training_input_data.shape[2])

            # Fit model with history to check for overfitting
            history = model.fit(
                training_input_data,
                training_output_data,
                epochs = int(sys.argv[3]),
                validation_data=(testing_input_data, testing_output_data),
                shuffle=False
            )

            '''pyplot.plot(history.history['loss'], label='Training Loss')
            pyplot.plot(history.history['val_loss'], label='Testing Loss')
            #pyplot.legend()
            pyplot.xlabel('Days')
            pyplot.ylabel('Price')
            numEpochs = sys.argv[3]
            pyplot.title(stock+' '+year+' '+numEpochs+' epochs')
            pyplot.legend()
            #pyplot.show()
            #pyplot.savefig('./Figures/'+stock+'/'+numEpochs+'-epochs.png')'''

        n = int(sys.argv[4]) 
        entrada = testing_input_data[:n]
        saida = testing_output_data[:n]
        #raw_predictions = model.predict(entrada[:])
        for j in range(0, len(entrada)):
            if j == 0:
                raw_predictions = model.predict(entrada[:j+1])
            else:
                #print('Entrada[:j+1]: ', entrada[:j+1])
                #print('Entrada[:j+1][:,0]: ', entrada[:j+1][:,0])
                #entrada[j][:,0] = np.mean(entrada[:j+1][:,0])
                #print('Entrada[:j+1]: ', entrada[:j+1])
                #print('Entrada[:j+1][:,0]: ', entrada[:j+1][:,0])
                #print('Entrada[j][:,1]: ', entrada[j][:,1])
                #print('raw_predictions[j-1]', raw_predictions[j-1])
                entrada[j][:,1] = raw_predictions[j-1]
                raw_predictions = np.append(raw_predictions, model.predict(entrada[j:j+1]), axis=0)
         
        # Reshape testing input data back to 2d
        entrada = entrada.reshape((entrada.shape[0], entrada.shape[2]))
        saida = saida.reshape((len(saida), 1))
        # Invert scaling for prediction data
        unscaled_predictions = concatenate((entrada, raw_predictions), axis = 1)
        unscaled_predictions = scaler.inverse_transform(unscaled_predictions)
        unscaled_predictions = unscaled_predictions[:, -1]
        # Invert scaling for actual data
        unscaled_actual_data = concatenate((entrada, saida), axis = 1)
        unscaled_actual_data = scaler.inverse_transform(unscaled_actual_data)
        unscaled_actual_data = unscaled_actual_data[:, -1]
        # Plot prediction vs actual
        
        pyplot.plot(unscaled_actual_data, label='Actual Closing Price')
        pyplot.plot(unscaled_predictions, label='Predicted Closing Price')
        pyplot.xlabel('Days')
        pyplot.ylabel('Price')
        numEpochs = sys.argv[3]
        pyplot.title(stock+' '+year+' '+numEpochs+' epochs')
        pyplot.legend()
        #pyplot.show()
        pyplot.savefig('./Figures/'+stock+'/'+numEpochs+'-epochs.png')
        
        #flag = int(input('1 - novo teste\n2 - encerrar\n'))
        flag = 2
        if(flag == 2):
            break

if __name__ == "__main__":
    main()