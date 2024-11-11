"""
Este script é serve apenas para fazer o download do punkt_tab do NLTK para que a API funcione devidamente. 
Ignorar se não for necessário. 
"""

import ssl
import nltk
import os

# Ignorar verificação de certificado SSL
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

# Defina o caminho correto onde o NLTK armazenará os dados
nltk_data_path = './venv/lib'  # Ajuste esse caminho conforme necessário
if not os.path.exists(nltk_data_path):
    os.makedirs(nltk_data_path)  # Cria o diretório, se não existir

# Adicionar o caminho ao NLTK
nltk.data.path.append(nltk_data_path)

# Baixar o pacote 'punkt' no caminho correto
nltk.download('punkt_tab', download_dir=nltk_data_path)
