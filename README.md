# TARS
**TARS -  Virtual Assistant**

Para rodar é necessário possuir o pyhton 3.9 instalado e configurado nas variáveis de ambiente.

*Primeiro instalar o ambiente virtual:*

    python -m venv "nome_do_ambiente"


*Depois vamos acessar o ambiente:*
**Windows**

    nome_do_ambiente\Scripts\activate

**Linux e Mac**

    source nome_do_ambiente\Scripts\activate

Para executar, rodar o comando:

    python main_2.py

Obs: Por enquanto é necessário iniciar o assistente com o comando "**R2**", pois "**TARS**" ainda não está sendo identificado corretamente.

## Legenda console:

 - **Diga ‘R2’ para iniciar** - Aguardando você falar R2, senão nenhum ação será realizada
 - **Aguardando comandos** - Assistente foi ativado e aguarda suas ordens.


**Interações disponíveis:**

 - Perguntas iniciando com: "**quem**", "**qual**", "**o que**", "**quando**", "**onde**", "**por que**", "**como**" serão direcionadas ao Google.
 - **"se apresente"** para uma curta apresentação.
 - **"que horas são"**
 - **"que dia é hoje"**
 - **"qual é o clima de agora"**
 - Operações matemáticas podem ser resolvidas iniciando o comando **"quanto é"**
 - "**abrir youtube**" e "**abrir facebook**" também estão disponíveis.
 - Para encerrar a aplicação, o comando é "**desligar**".
