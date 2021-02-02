# TARS
**TARS -  Virtual Assistant**

Para rodar é necessário possuir o pyhton 3.6 instalado e configurado nas variáveis de ambiente.
Recomendação de usar o Anaconda para construir um ambiente em python 3.6 sem necessidade de baixar e configurá-lo manualmente:
https://www.anaconda.com/

Usando o Anaconda, verificar se o mesmo está nas variáveis de ambiente.

*Primeiro instalar o ambiente virtual:*

    conda create -n nome_ambiente python=3.6


*Depois vamos ativar o ambiente:*

    conda activate nome_ambiente
    
*Depois vamos instalar as dependências*

    pip install -r requeriments

*Caso apareça algum erro ao instalar o pyaudio*

    pipwin install pyaudio
    
    
Para executar, rodar o comando:

    python core.py

Obs: Por enquanto é necessário iniciar o assistente com o comando "**Awake**", pois "**TARS**" ainda não está sendo identificado corretamente.

## Legenda console:

 - **Diga ‘awake’ para iniciar** - Aguardando você falar awake, senão nenhum ação será realizada
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
