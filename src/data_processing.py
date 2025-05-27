import logging
import re
import unicodedata
import nltk

# logger para este módulo
logger = logging.getLogger(__name__)


# Download de recursos da biblioteca nltk
try:
    nltk.data.find('tokenizers/punkt')
except:
    logger.info("Baixando recurso 'punkt' do NLTK...")
    nltk.download('punkt')

try:
    nltk.data.find('tokenizers/punkt_tab')
except:
    logger.info("Baixando recurso 'punkt' do NLTK...")
    nltk.download('punkt_tab')

try:
    nltk.data.find('corpora/stopwords')
except:
    logger.info("Baixando recurso 'stopwords' do NLTK...")
    nltk.download('stopwords')

STOP_WORDS_PT = set(nltk.corpus.stopwords.words('portuguese'))



def remove_combining(texto: str | None) -> str:
    '''
    Remove caracteres combinantes

    Param
        texto: texto para remover caracteres combinantes

    Return
        texto após a remoção dos caracteres combinantes
    '''

    if not texto:
        logger.warning('Tentativa de limpar texto None. Retorna string vazia')
        return ''

    texto = unicodedata.normalize('NFKD', texto)  # separa em caracteres base e caracteres combinantes
    texto = ''.join(c for c in texto if not unicodedata.combining(c))  # remove caracteres combinantes
    return texto


def clean_text(texto: str | None) -> str:
    '''
    Limpeza do texto:
    1. Converter tudo para minúsculas
    2. Remove caracteres especiais (ou combinantes) --> mantém letras, números e espaços
    3. Normaliza múltiplos espaços em branco para único espaço

    Param
        texto: string a ser limpa

    Return
        texto limpo ou string vazia
    '''

    if not texto:
        logger.warning('Tentativa de limpar texto None. Retorna string vazia')
        return ''

    # Converter para minúsculas
    texto = texto.casefold()

    # Remover caracteres especiais e acentos
    texto = re.sub(r'[^a-zà-ú0-9\s]', '', texto, flags=re.IGNORECASE)  # mantém acentos
    texto = remove_combining(texto)

    # Normalizar multiplos espaços
    texto = re.sub(r'\s+', ' ', texto).strip()

    logger.info(f'Texto após limpeza: {texto[:100]}')
    return texto



def preprocess_text(texto: str | None) -> str:
    '''
    Pré-processa o texto:
    1. Tokeniza o texto em palavras.
    2. Remove stopwords.
    3. Reconstrói o texto a partir dos tokens restantes.
    
    Param
        texto: texto a passar pelo processo de remoção de stopwords

    Return
        texto sem stopwords ou string vazia
    '''

    if not texto:
        logger.warning('Tentativa de limpar texto None. Retorna string vazia')
        return ''
    
    # Tokenização (padronizado para português)
    tokens = nltk.tokenize.word_tokenize(texto, language='portuguese')

    # Remoçao de stopwords (padronizado para português)
    tokens = [token for token in tokens if token not in STOP_WORDS_PT and len(token) > 1]

    # Reconstrução do texto
    texto = ' '.join(tokens)

    logger.info(f'Texto após pré-processamento: {texto}')
    return texto


def text_pipeline(texto: str | None) -> str:
    '''
    Executa todo o pipelina de limpeza e pré-processamento de texto

    Param
        texto: string para passar pelo processo de limpeza e remoção de stopwords

    Return
        texto processado ou string vazia
    '''

    if not texto:
        logger.warning('Tentativa de limpar texto None. Retorna string vazia')
        return ''
    
    # limpeza do texto
    texto = clean_text(texto)
    
    # pré-processamento do texto
    texto = preprocess_text(texto)

    return texto



if __name__ == '__main__':
    
    textos_exemplo = [
        "Olá, MUNDO! Este é um TEXTO de@exemplo nº123 com acentuação, para ser processado. Ele contém algumas palavras como: 'de', 'para', 'com'.",
        "",
        None,
        "!@#$%^&*()",
    ]
    
    for texto in textos_exemplo:
        print(text_pipeline(texto))