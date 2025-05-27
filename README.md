# Teste Técnico
Repositório para organizar código e documentação do teste técnico de Engenharia de Dados para projeto no ceia.

O pipeline sege a seguinte forma:
- extração de metadados (título e descrição) e de transcrição de um vídeo do youtube dado uma URL
- processo de limpeza (remoção de acentos, caracteres especiais e normalização em minpusculas)
- processo de remoção de _stopwords_
- output em formato json

## Configurar Ambiente

### 1. Clonar repositório git
Clone o repositório do github para uma pasta local no seu computador
```
git clone https://github.com/CEIA-Koru/dados_sinteticos.git
```

### 2. Configurar Ambiente Virtual
É recomendado o uso de um ambiente virtual python para evitar conflitos de dependências de bibliotecas com outros projetos. Na mesma pasta em que foi clonado o repositório (a pasta `.venv` fica de fora da pasta do repositório), execute: 

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

OBS: assume-se que já tenha python3.9+ e pip instalados na máquina

### 3. Instalar Dependências
Com o ambiente virtual ativado, instale as dependências do projeto com o comando:
``` bash
pip install -r ./teste-tecnico/requirement.txt
```

### 4. Criar arquivo .env
Dentro da pasta `./teste-tecnico`, crie um arquivo chamado `.env` e configure sua chave API do youtube da seguinte forma:
```
YOUTUBE_API_KEY=<sua-cahve-aqui>
```

### 5. Executar main.py
```
python .\teste-tecnico\main.py
```

## Formato da saída

