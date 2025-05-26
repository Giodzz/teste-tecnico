import os
from dotenv import load_dotenv
import logging
import json
from src.data_extraction import *
from src.data_processing import *

# Configurar o logging
logging.basicConfig(
    level=logging.INFO,  # nível mínimo de severidade
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # formato da mensagem de log
    handlers=[
        logging.StreamHandler()  # enviar logs para o console 
        # logging.FileHandler("app.log") # salvar em arquivo
    ]
)

# logger do arquivo atual (main.py)
logger = logging.getLogger(__name__)

# Carregar variáveis de ambiente
project_root_dir = os.path.dirname(os.path.abspath(__file__))
dotenv_path = os.path.join(project_root_dir, '.env')
load_dotenv(dotenv_path)

# acessar variável de ambiente
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")


def extrair_formatar_dados(video_url: str | None) -> object | None:
    
    if not video_url:
        logger.warning('Tentativa de extrair dados de vídeo de uma URL vazia')
        return None

    service = get_youtube_service()
    metadata = get_metadata(service, video_url)
    transcript = get_transcript(video_url)

    for k, v in metadata.items():
        metadata[k] = text_pipeline(v)
    
    for dicio in transcript:
        for k, v in dicio.items():
            if isinstance(v, str):
                dicio[k] = text_pipeline(v)

    return {
        'metadata': metadata,
        'transcript': transcript
    }
    

if __name__ == '__main__':
    
    while True:
        video_url = input('URL do vídeo ["sair" para sair]: ')
        if 'sair' in video_url.casefold().strip():
            break

        extrair_formatar_dados(video_url)