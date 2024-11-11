### Sprint 5 - Implementação de Filtros para Tratamento de Segurança

#### Desafio:
O objetivo desta Sprint foi implementar filtros de entrada e/ou saída para garantir aspectos de segurança, especialmente relacionados à prevenção de conteúdo ofensivo, como *hate speech*, uso de jailbreak ou perguntas de concorrentes. Essa solução visa proteger a interação com o modelo de linguagem de eventuais abusos ou uso inadequado da API.

#### Solução:
Para abordar este desafio, utilizamos a **API da OpenAI** para classificar se a mensagem de entrada do usuário contém conteúdo ofensivo. O filtro é aplicado antes do processamento da entrada pelo modelo *fine-tuned* Llama3.2 8B. A classificação é feita através de um prompt específico, conforme mostrado abaixo:

##### Prompt Enviado para Classificação:
``` 
Você é um classificador de conteúdo. A seguinte mensagem é ofensiva? (seja com conteúdo racista, xenofóbico, misógino, etc.) Responda com 'Sim' ou 'Não': {mensagem}
```

Com base na resposta da OpenAI (Sim ou Não), o fluxo de controle segue de acordo com as seguintes regras:

- **Se a resposta for 'Sim'**: A entrada do usuário é considerada ofensiva, e uma mensagem padrão é retornada ao usuário:
  
  **Mensagem Padrão**:
  ```
  A mensagem não será respondida devido ao conteúdo ofensivo.
  ```

- **Se a resposta for 'Não'**: A entrada é considerada segura, e o fluxo normal de execução do modelo *fine-tuned* Llama3.2 8B continua.

#### Código de Implementação:
O código da solução está localizado no arquivo **[app.py](./app.py)**. Neste arquivo, são definidos o fluxo de verificação da entrada do usuário, a chamada para a API de classificação da OpenAI, e o encaminhamento para o modelo ajustado, caso o conteúdo seja considerado seguro.