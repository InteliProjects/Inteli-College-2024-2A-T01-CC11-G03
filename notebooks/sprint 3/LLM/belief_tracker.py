"""
Implementação do belief tracker para nossa pipeline de LLM. O intuito é armazenar o estado atual do chat a fim de que seja possível
entender a intenção para cada pergunta e as respostas anteriores do modelo. 

Referências:
Nikola Mrkšić, Diarmuid Ó Séaghdha, Tsung-Hsien Wen, Blaise Thomson, and Steve Young. 2017.
Neural Belief Tracker: Data-Driven Dialogue State Tracking. In Proceedings of the 55th Annual 
Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), 
pages 1777–1788, Vancouver, Canada. Association for Computational Linguistics.

Hayet Brabra, Marcos Baez, Boualem Benatallah, Walid Gaaloul, Sara Bouguelia, et al.. 
Dialogue management in conversational systems: a review of approaches, challenges, and opportunities. 
IEEE Transactions on Cognitive and Developmental Systems, 2022, 14 (3), pp.783-798.
ff10.1109/TCDS.2021.3086565ff. ffhal-03626466
"""

import unittest

class BeliefTracker:
  def __init__(self):
    self.intent = None # Intenção da pergunta que será guardada a cada interção 
    self.entities = {} # Entidades extraídas através do modelo de NER 
    self.history = [] # Lista que armazena o histórico de perguntas do usuário 

  def update_state(self, intent, entities, user_input, response=None):
    # Atualiza o estado do diálogo com intenção, entidades, a pergunta do usuário e opcionalmente a resposta.
    self.intent = intent
    self.entities.update(entities)
    
    interaction = {"pergunta": user_input}
    if response:
      interaction["resposta"] = response
    
    self.history.append(interaction)

# Implementação dos testes unitários
class TestBeliefTracker(unittest.TestCase):
  def setUp(self):
    self.dialogue_state = BeliefTracker()
         
  def test_initial_state(self):
    # Verifica o estado inicial da classe
    self.assertIsNone(self.dialogue_state.intent)
    self.assertEqual(self.dialogue_state.entities, {})
    self.assertEqual(self.dialogue_state.history, [])
    
  def test_update_state_without_response(self):
    # Testa a atualização do estado sem resposta
    self.dialogue_state.update_state("consultar_cotacao", {"currency": "USD"}, "Qual a cotação do dólar?")
    self.assertEqual(self.dialogue_state.intent, "consultar_cotacao")
    self.assertEqual(self.dialogue_state.entities, {"currency": "USD"})
    self.assertEqual(len(self.dialogue_state.history), 1)
    self.assertEqual(self.dialogue_state.history[0], {"pergunta": "Qual a cotação do dólar?"})
    
  def test_update_state_with_response(self):
    # Testa a atualização do estado com resposta incluída
    self.dialogue_state.update_state("consultar_cotacao", {"currency": "USD"}, "Qual a cotação do dólar?", "A cotação atual é 5.25.")
    self.assertEqual(self.dialogue_state.intent, "consultar_cotacao")
    self.assertEqual(self.dialogue_state.entities, {"currency": "USD"})
    self.assertEqual(len(self.dialogue_state.history), 1)
    self.assertEqual(self.dialogue_state.history[0], {"pergunta": "Qual a cotação do dólar?", "resposta": "A cotação atual é 5.25."})

  def test_multiple_updates(self):
    # Testa múltiplas atualizações do estado
    self.dialogue_state.update_state("remessa", {}, "Como faço uma remessa?", "Você pode fazer uma remessa pelo app.")
    self.dialogue_state.update_state("tempo_envio", {}, "Quanto tempo leva?", "O tempo é de 1 a 2 dias úteis.")
    self.assertEqual(len(self.dialogue_state.history), 2)
    self.assertEqual(self.dialogue_state.history[0], {"pergunta": "Como faço uma remessa?", "resposta": "Você pode fazer uma remessa pelo app."})
    self.assertEqual(self.dialogue_state.history[1], {"pergunta": "Quanto tempo leva?", "resposta": "O tempo é de 1 a 2 dias úteis."})

# Executar os testes
if __name__ == '__main__':
  unittest.main()