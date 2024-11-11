from Embeddings.embeddings import generate_embedding
import tensorflow as tf
import numpy as np

model = tf.keras.models.load_model('model.keras')

input_data = generate_embedding("Minha remessa falhou e gostaria do meu dinheiro de volta").reshape(1, 1, 100)

predictions = model.predict(input_data)

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


predicted_class = np.argmax(predictions)

print(f"Predicted class: {intent_dict[predicted_class]}")