# Pipeline de Extração de Dados do YouTube - Teste Técnico
Repositório para organizar código e documentação do teste técnico de Engenharia de Dados para projeto no ceia.

O pipeline segue a seguinte forma:
- extração de metadados (título e descrição) e de transcrição de um vídeo do youtube dado uma URL
- processo de limpeza (remoção de acentos, caracteres especiais e normalização em minúsculas)
- processo de remoção de _stopwords_
- output em formato json

## Configurar Ambiente

Pré-requisitos:
- python3.9+ instalado
- pip instalado
- git instalado

### 1. Clonar repositório git
Clone o repositório do github para uma pasta local no seu computador
```bash
git clone https://github.com/Giodzz/teste-tecnico.git
cd ./teste-tecnico
```
A partir de agora, os comandos são exemplificados considerando que o terminal está dentro da pasta do repositório

### 2. Configurar Ambiente Virtual
É recomendado o uso de um ambiente virtual python para evitar conflitos de dependências de bibliotecas com outros projetos. Então, execute: 

**Windows**
``` bash
# criar ambiente virtual
python -m venv .venv

# ativar ambiente virtual
.venv\Scripts\activate
```

**Linux ou MAC**
``` bash
# criar ambiente virtual
python3 -m venv .venv

# ativar ambiente virtual
source .venv/bin/activate
```

### 3. Instalar Dependências
Com o ambiente virtual ativado, instale as dependências do projeto com o comando:
``` bash
pip install -r ./requirements.txt
```

### 4. Criar arquivo .env
Crie um arquivo chamado `.env` e configure sua chave API do youtube da seguinte forma:
```
YOUTUBE_API_KEY=<sua-chave-aqui>
```

### 5. Executar main.py
```
python ./main.py
```

## Formato da saída
O script produzirá uma saída JSON estruturada da seguinte forma: 
``` json
{
    "metadata": {
        "title": "titulo",
        "description": "descricao"
    },
    "transcript": [
        {
            "start": 0.0,
            "text": "video de boas-vindas"
        },
        {
            "start": 1.26,
            "text": "exemplo de conteudo"
        },
        ...
    ]
}
```

## Ferramentas Utilizadas

- **Coleta de Dados**
    - `google-api-python-client` (para YouTube Data API v3): Extração de metadados (título, descrição).
    - `youtube-transcript-api`: Obtenção de transcrições.

- **Limpeza e Pré-processamento**
    - `re` (módulo Python): Remoção de caracteres especiais.
    - `unicodedata` (módulo Python): Normalização e remoção de acentos.
    - `nltk`: Tokenização e remoção de stopwords.

- **Armazenamento (Simulado)**
    - `json` (módulo Python): Estruturação e formatação dos dados em JSON (em memória).

- **Gerenciamento de Ambiente e Configuração**
    - `python-dotenv`: Gerenciamento de chaves API.
    - `logging` (módulo Python): Registro de logs do pipeline.