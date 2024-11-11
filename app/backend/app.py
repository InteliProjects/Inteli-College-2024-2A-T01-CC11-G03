from Embeddings.embeddings import generate_embedding
import tensorflow as tf
import numpy as np
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from llama_cpp import Llama  
from typing import Dict
from belief_tracker import BeliefTracker  
import logging

from langchain import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

from dotenv import load_dotenv
import os

# Configuração de logging
logging.basicConfig(level=logging.INFO)

# Dicionário de intenções
intent_dict = {
    0: "Acesso a conta",
    1: "Atualizacao de dados cadastrais",
    2: "Cadastro de beneficiario",
    3: "Cancelamento",
    4: "Como depositar",
    5: "Como depositar",
    6: "Como fazer remessa",
    7: "Como se inscrever",
    8: "Confirmacao de cambio/taxas",
    9: "Confirmacao de saldo",
    10: "Dificuldades com utilizacao do App",
    11: "Envio via Deposit Code",
    12: 'Pedido de envio via metodo "ByPhone"',
    13: "Problemas de remessa",
    14: "Problemas/Duvidas de atualizacao de dados cadastrais",
    15: "Problemas/Duvidas sobre deposito",
    16: "Problemas/Duvidas sobre remessas",
    17: "Reembolso",
    18: "Registro/Atualizacao de Documento",
    19: "Regras do servico",
    20: "Solicitacao de cartao de remessas",
    21: "Tempo de entrega do cartao",
    22: "Tempo de remessa",
    23: "Tempo para depositos refletirem no saldo",
    24: "Termos e condicoes do servico",
    25: "erro ao processar a pergunta"
}

# Configurando a chave de API da OpenAI
load_dotenv()

openaiapi_key = os.getenv("OPENAI_API_KEY")
llm = OpenAI(temperature=0.2, openai_api_key=openaiapi_key)

app = FastAPI()


model = tf.keras.models.load_model('model.keras')
model_llm = Llama(model_path="model_llm.gguf", quantization="bnb4bit", use_gpu=False) # O modelo em gguf não foi enviado para o git devido ao limite de espaço: https://huggingface.co/t01-g3/Llama.3.2-instruct-mod-11/tree/main (acesse com o email do grupo)

# Dicionário para armazenar os estados de diálogo por ID de sessão
dialogue_states: Dict[str, BeliefTracker] = {}

class InputData(BaseModel):
    text: str

# Função para verificar se a mensagem é ofensiva
def verificar_ofensividade(mensagem: str) -> bool:
    # Prompt para classificar se o conteúdo é ofensivo
    template = """Você é um classificador de conteúdo. A seguinte mensagem é ofensiva? (seja com conteúdo racista, xenofóbico, misogino e etc) 
    Responda com 'Sim' ou 'Não': {mensagem}"""

    prompt = PromptTemplate(input_variables=["mensagem"], template=template)
    chain = LLMChain(llm=llm, prompt=prompt)

    # Executando o LangChain para verificar a ofensividade
    resposta = chain.run(mensagem)
    
    # Log da resposta para verificar
    print(f"Classificação de Ofensividade: {resposta.strip()}")

    return resposta.strip().lower() == "sim"

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
def health_check():
    return {"status": "ok"}

# Função para buscar ou criar um novo BeliefTracker para um determinado ID
def get_or_create_dialogue_state(dialogue_id: str):
    if dialogue_id not in dialogue_states:
        # Criar um novo estado de diálogo se o ID não existir
        dialogue_states[dialogue_id] = BeliefTracker()
    return dialogue_states[dialogue_id]

# Função para construir o contexto acumulado a partir do histórico do BeliefTracker
def build_context_from_history(dialogue_state: BeliefTracker) -> str:
    context = ""
    for interaction in dialogue_state.history:
        # Concatenar perguntas e respostas anteriores no contexto
        context += f"{interaction['pergunta']}\n"
        if "resposta" in interaction:
            context += f"{interaction['resposta']}\n"
    return context.strip()

"""Rota para processamento de perguntas e contexto via Belief Tracker"""
@app.post("/predict/{dialogue_id}")
def get_response(dialogue_id: str, input_data: InputData):
     # Verificar se a mensagem é ofensiva
    if verificar_ofensividade(input_data.text):
        return {
            "llm_response": "A mensagem não será respondida devido ao conteúdo ofensivo."
        }
    
    # Recuperar ou criar o estado de diálogo para o ID fornecido
    dialogue_state = get_or_create_dialogue_state(dialogue_id)

    # Geração da predição usando o modelo Keras
    emb = generate_embedding(input_data.text).reshape(1, 1, 100)
    predictions = model.predict(emb)
    predicted_class = np.argmax(predictions)
    predicted_intent = intent_dict[predicted_class]
    
    # Construir o contexto acumulado a partir do histórico do diálogo
    history_context = build_context_from_history(dialogue_state)
    
    prompt = (f"Abaixo está uma instrução que descreve uma tarefa e uma pergunta relacionada. "
          f"Responda de maneira clara e objetiva, focando nos serviços, procedimentos e operações "
          f"oferecidos pela Brastel, sem repetir a pergunta ou adicionar informações irrelevantes.\n\n"
          f"# Contexto anterior da conversa: {history_context}\n" 
          f"# Instrução: {predicted_intent}\n"
          f"# Pergunta: {input_data.text}\n\n"
          f"Responda de forma concisa e com foco nas informações diretamente relacionadas à Brastel.")
    
    # Log do prompt para verificação
    logging.info(f"Prompt para o LLM: {prompt}")

    # Gerar a resposta utilizando o modelo Llama diretamente
    try:
        response = model_llm(prompt, max_tokens=256, top_k=50, top_p=0.95, temperature=0.2)
        llm_response = response['choices'][0]['text'] if 'choices' in response and response['choices'] else ""
    except Exception as e:
        logging.error(f"Erro ao gerar resposta do LLM: {e}")
        llm_response = "Erro ao processar a resposta."

    logging.info(f"Resposta do LLM: {llm_response}")

    # Atualizar o estado de diálogo com o contexto acumulado e a nova resposta
    full_context = history_context + f"\n{input_data.text}"  # Acumula contexto com a nova pergunta
    dialogue_state.update_state(predicted_intent, {}, full_context, llm_response)

    return {
        "id": dialogue_id,
        "prediction": predicted_intent,
        "llm_response": llm_response,
        "history": [{"contexto": full_context.strip(), "resposta": llm_response} if llm_response else {"contexto": full_context.strip()}]
    }

"""Rota para verificar o estado de diálogo do belief tracker"""
@app.get("/dialogue/{dialogue_id}")
def get_dialogue_state(dialogue_id: str):
    dialogue_state = dialogue_states.get(dialogue_id)
    if dialogue_state:
        history_with_context = []
        for interaction in dialogue_state.history:
            context_entry = {"contexto": interaction['pergunta']}
            if "resposta" in interaction:
                context_entry["resposta"] = interaction["resposta"]
            history_with_context.append(context_entry)
        return {"dialogue_id": dialogue_id, "history": history_with_context}
    else:
        return {"error": "Diálogo não encontrado"}, 404


"""Rota para processamento de perguntas sem contexto via Belief Tracker"""
@app.post("/predict")
def get_response(input_data: InputData):
     # Verificar se a mensagem é ofensiva
    if verificar_ofensividade(input_data.text):
        return {
            "llm_response": "A mensagem não será respondida devido ao conteúdo ofensivo."
        }
    
    # Geração da predição usando o modelo Keras
    emb = generate_embedding(input_data.text).reshape(1, 1, 100)
    predictions = model.predict(emb)
    predicted_class = np.argmax(predictions)
    predicted_intent = intent_dict[predicted_class]

    prompt = (f"Abaixo está uma instrução que descreve uma tarefa e uma pergunta relacionada. "
          f"Responda de maneira clara e objetiva, focando nos serviços, procedimentos e operações "
          f"oferecidos pela Brastel, sem repetir a pergunta ou adicionar informações irrelevantes.\n\n"
          f"# Instrução: {predicted_intent}\n"
          f"# Pergunta: {input_data.text}\n\n"
          f"Responda de forma concisa e com foco nas informações diretamente relacionadas à Brastel.")

    response = model_llm(prompt, max_tokens=256, top_k=50, top_p=0.95, temperature=0.5)
    return {"prediction": predicted_intent, "llm_response": response['choices'][0]['text']}