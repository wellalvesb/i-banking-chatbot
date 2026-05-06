from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import pandas as pd
import json

# contevectorizer e uma classe da biblioteca sklearn que transforma
# texto do vocabulario em vetores numericos
# MultinomialNB classifica os textos com base na frequencia das palavras.
# aprende com a contagem das palavras vetorizadas
# faz predições com base nas probabilidades aprendidas

# DADOS DE TREINAMENTO
# Ajustado para ler o arquivo local perguntas.csv
perguntas = pd.read_csv("perguntas.csv")

frases = perguntas["pergunta"].astype(str).tolist()
categoria = perguntas["categoria"].astype(str).tolist()

# vetorização e treinamento
vetorizador = CountVectorizer()
X = vetorizador.fit_transform(frases)

# vetorizador vai guardar um objeto que sera usado para transformar o texto em vetores
# X guarda o resultado da transformação das frases em vetores numericos.
# fit_transform e um metodo da classe CountVectorizer, ele aprende o vocabulario
modelo = MultinomialNB()
modelo.fit(X, categoria)

# Ajustado para o nome do arquivo definido anteriormente
try:
    with open("resposta.json", "r", encoding="utf-8") as arquivo:
        resposta = json.load(arquivo)
except FileNotFoundError:
    print("Erro: arquivo 'resposta.json' não encontrado!")
    resposta = {}

print('='*30)
print('CHATBOT OPERADOR DE CARTÃO DE CRÉDITO')
print("digite sua pergunta ou 'sair' para encerrar")
print('='*30)

while True:
    pergunta = input('\nVocê: ').lower()
    if pergunta == 'sair':
        print('Chatbot: Até logo!')
        break
    
    if not pergunta:
        continue
        
    pergunta_vetorizada = vetorizador.transform([pergunta])

    categoria_prevista = modelo.predict(pergunta_vetorizada)[0]

    probabilidades = modelo.predict_proba(pergunta_vetorizada)[0]
    
    # Get the index of the predicted category
    idx_categoria_prevista = modelo.classes_.tolist().index(categoria_prevista)
    maior_probabilidade = probabilidades[idx_categoria_prevista]

    if maior_probabilidade < 0.40:
        print("chatbot: desculpe, não entendi sua solicitação. Pode reformular a pergunta?")
    else:
        print("categoria identificada:", categoria_prevista)
        print("probabilidade:", round(maior_probabilidade * 100, 2), "%")
        
        # Busca a resposta baseada na categoria identificada
        resultado = resposta.get(categoria_prevista, "Desculpe, não encontrei uma resposta para esta categoria.")
        print('CHATBOT: ', resultado)
