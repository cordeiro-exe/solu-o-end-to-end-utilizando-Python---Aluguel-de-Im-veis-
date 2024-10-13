# construir a API ---> Flask
from flask import Flask, request
# Lib para carregar modelo
import joblib
# lib banco de dados
import sqlite3
# lib para datas
from datetime import datetime


# Jupyter (conexao) --> API (Flask)

aplicativo  = Flask(__name__)

# carregar modelo
modelo = joblib.load('modelo_floresta_aleatorio_v1.0.0.pkl')



# funçao para receber API
@aplicativo.route('/api_preditivo/<area>;<rooms>;<bathroom>;<parking_spaces>;<floor>;<animal>;<furniture>;<hoa>;<property_tax>', methods=['GET'])
def funcao_01(area,rooms,bathroom,parking_spaces,floor,animal,furniture,hoa,property_tax):

    # Data e hora de inicio
    data_inicio = datetime.now()

    # recebendo os inputs da API

    lista = [ 
        float(area), float(rooms),float(bathroom),float(parking_spaces), float(floor), float(animal), float(furniture), float(hoa), float(property_tax)

    ]

    # Tentar a previsao

    try:
        # Predict
        previsao = modelo.predict([lista] )
        # inserir valor de previsao
        lista.append(str(previsao))

        # concatenando a lista
        input = ''
        for valor in lista:
            input = input + str(valor)

        data_fim = datetime.now()
        processamento = data_fim - data_inicio

        # Criar a conexao com o banco
        conexao_banco = sqlite3.connect('banco_dados_API.db')
        cursor = conexao_banco.cursor()

        query_inserindo_dados = f'''
            INSERT INTO Log_API (Inputs, Inicio, Fim, Processamento)
            VALUES ( '{ input }', '{data_inicio}', '{data_fim}', '{processamento}')
        '''
        # Executando a query
        cursor.execute (query_inserindo_dados)
        conexao_banco.commit()

        #Fechando conexao do banco de dados

        cursor.close()

        # Retorno do modelo
        return{ 'valor_aluguel': str(previsao) }

    except:
        return{'Aviso':'Deu algum erro!'}

if __name__ == '__main__':
    aplicativo.run( debug=True )