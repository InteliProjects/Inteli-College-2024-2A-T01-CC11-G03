import ollama

resp = ollama.embeddings(
  model='llama3.1',
  prompt='Como faço para cancelar a compra e rastrear',
)

print(len(resp['embedding']))