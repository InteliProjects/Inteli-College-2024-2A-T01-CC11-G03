<table>
<tr>
<td>
<a href= "https://www.btgpactual.com/"><img src="./artigo/imgs/brastel_remit_logo.png" alt="BTG Pactual" border="0" width="100%"></a>
</td>
<td><a href= "https://www.inteli.edu.br/"><img src="./logo-inteli.png" alt="Inteli - Instituto de Tecnologia e Liderança" border="0" width="30%"></a>
</td>
</tr>
</table>

# Projeto: Implementação de um Chatbot para melhorar o atendimento do SAC.

# EMPRESA: Brastel

# Grupo: MoshiMoshi Bot

# Integrantes:

* [Gabriel Carneiro]<gabriel.carneiro@sou.inteli.edu.br>
* [Gabriel Nhoncanse]<gabriel.nhoncanse@sou.inteli.edu.br>
* [João Alcaraz]<joao.alcaraz@sou.inteli.edu.br>
* [Pedro Munhoz]<pedro.rivero@sou.inteli.edu.br>
* [Pedro Romão]<pedro.dias@sou.inteli.edu.br>
* [Sarah Ribeiro]<sarah.ribeiro@sou.inteli.edu.br>
* [Yasmin Vitória]<yasmin.jesus@sou.inteli.edu.br>

# Descrição

A Brastel enfrenta desafios em seu serviço de atendimento ao cliente, onde a crescente demanda e a complexidade das interações tornam o suporte eficaz mais caro e difícil de gerenciar. A solução proposta neste projeto envolve o desenvolvimento de um chatbot baseado em inteligência artificial generativa, capaz de atender os clientes de forma eficiente, respondendo a demandas corriqueiras e transferindo a conversa para um atendente humano quando necessário. Essa abordagem visa melhorar a experiência do usuário, ao mesmo tempo em que otimiza os custos operacionais e reduz a necessidade de intervenção humana em atendimentos de questões recorrentes.   

# Configuração para desenvolvimento

Para configurar o ambiente de desenvolvimento e rodar o backend da aplicação, siga os seguintes passos:

1. **Abra o diretório do projeto:**
   - Navegue até a pasta *[app/backend](./app/backend/)*.

2. **Crie um ambiente virtual:**
   - Execute o comando a seguir para criar um ambiente virtual Python:
  
        ```bash
        python3 -m venv venv
        ```

    - Ative o ambiente virtual:
  
        ```bash
        source venv/bin/activate
        ```

3. **Instale as dependências do projeto**
   - Instale todas as dependências listadas no arquivo *requirements.txt*:

        ```bash
       pip install -r requirements.txt
        ```

4. **Configuração dos modelos de classificação:**
   - Para rodar o backend, é necessário ter os modelos de classificação no formato .keras e o modelo LLM no formato *.gguf*. Esses modelos não foram submetidos ao repositório devido a restrições de privacidade.

5. **Configuração da API OpenAI:**
    - Certifique-se de ter uma API funcional da OpenAI para aplicar os filtros de conteúdo ofensivo, conforme a necessidade do projeto.

6. **Executar a aplicação:**
   - Com o ambiente configurado, rode a aplicação utilizando o Uvicorn:

        ```bash
       uvicorn app:app --reload
        ```

# Slides

Os slides apresentados ao longo do projeto estão presentes na pasta [/slides](slides).

# Artigo

Os arquivos do artigo estão na pasta [/artigo](/artigo).

O conteúdo deste artigo foi elaborado como parte das atividades de aprendizado dos alunos, mas precisa ser revisto e modificado caso haja a intenção de submetê-lo para uma eventual publicação.

# Tags

* Sprint 5: https://github.com/Inteli-College/2024-2A-T01-CC11-G03/releases/tag/SPRINT_5 <br>
  * [Artigo Final](./artigo/)
  * [Apresentação Final](./slides/sprint%205/Apresentação%20FInal.pdf)
  * [Implementação Final](./notebooks/sprint%205/5%20-%20LLM/)
  * [Implementação do Desafio](./app/backend/desafio.md) junto ao [backend](./app/backend/) 
* Sprint 4: https://github.com/Inteli-College/2024-2A-T01-CC11-G03/releases/tag/SPRINT_4<br>
  * Artigo: Artigo com Avaliação de Modelo LLM
  * Implementação de Modelo LLM
* Sprint 3: https://github.com/Inteli-College/2024-2A-T01-CC11-G03/releases/tag/SPRINT_3<br>
  * Artigo: Avaliação de Modelo RNN com LSTM e Data Augmentation
  * Implementação de Modelo RNN com LSTM
  * Implementação de Data Augmentation
* Sprint 2: https://github.com/Inteli-College/2024-2A-T01-CC11-G03/releases/tag/SPRINT_2<br>
  * Artigo com Avaliação de Modelos de Classificação de Texto
  * Implementação de Modelo Baseline (BoW com NB)
  * Implementação de Modelo com Rede Neural e Word2Vec pré-treinado
* Sprint 1: https://github.com/Inteli-College/2024-2A-T01-CC11-G03/releases/tag/SPRINT_1
  * Draft do Artigo
  * Pipeline de Processamento e Base de Dados

# Licença

[Application 4.0 International](https://creativecommons.org/licenses/by/4.0/?ref=chooser-v1)<br>
<a><img src="./artigo/imgs/cc.png" alt="CC" border="0" width="20%"></a><br>
<a><img src="./artigo/imgs/pessoa.png" border="0" width="20%"></a><br>
