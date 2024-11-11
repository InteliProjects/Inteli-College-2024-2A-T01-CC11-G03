from gensim.models import Word2Vec
import numpy as np
import pandas as pd
import spacy
import nltk
nltk.download('punkt_tab')
from nltk.tokenize import word_tokenize

chats_clients = pd.read_csv('./data/augmented_data.csv')
chats_clients.head()
chats_clients.fillna('erro ao processar a pergunta', inplace=True)
nlp_pt = spacy.load("pt_core_news_sm")

# Tokenizando as colunas
chats_clients['Pergunta_tokens'] = chats_clients['Pergunta'].apply(lambda x: word_tokenize(x.lower()))

# Unindo as listas de tokens de Pergunta e Resposta para o modelo processar a lista
sentences_CBOW = chats_clients['Pergunta_tokens'].tolist()

# Utilizando o modelo Word2Vec
model_cbow = Word2Vec(sentences_CBOW, vector_size=100, window=5, min_count=1, sg=0)  #sg=0 para CBOW
# Função para gerar o embedding médio de uma frase
def get_sentence_embedding(tokens, model):
    word_vectors = [model.wv[token] for token in tokens if token in model.wv]
    if len(word_vectors) > 0:
        return np.mean(word_vectors, axis=0)
    else:
        return np.zeros(model.vector_size)
    

def tokenize(input):
    return word_tokenize(input.lower())

def embedd(tokens):
    return get_sentence_embedding(tokens, model_cbow)

def generate_embedding(input):
    tokens = tokenize(input)
    return embedd(tokens)
