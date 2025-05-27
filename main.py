import os
from dotenv import load_dotenv
import logging
import json
from src.data_extraction import (
    get_video_id_from_url,
    get_youtube_service,
    get_metadata,
    get_transcript
)
from src.data_processing import text_pipeline

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


def extrair_dados(video_url: str | None) -> dict | None:
    
    if not video_url:
        logger.warning('Tentativa de extrair dados de vídeo de uma URL vazia')
        return None

    service = get_youtube_service()
    if not service:
        logger.error("Falha ao obter o serviço do YouTube. Não é possível continuar a extração.")
        return None

    metadata = get_metadata(service, video_url)
    if not metadata:
        logger.warning(f"Metadados não puderam ser extraídos para {video_url}. Usando valores vazios.")
        metadata = {'title': '', 'description': ''}
        
    transcript = get_transcript(video_url)
    if not transcript:
        logger.warning(f"Transcrição não pôde ser extraída para {video_url}. Usando lista vazia.")
        transcript = []

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
        video_url = input('URL do vídeo ["sair" para sair]: ').strip()
        if 'sair' in video_url.casefold():
            logger.info('Finalizando o programa...')
            break

        if not video_url: # string vazia
            logger.warning("Nenhuma URL fornecida. Por favor, insira uma URL ou 'sair'.")
            continue

        dados_processados = extrair_dados(video_url)
        if dados_processados:
            json_output_string = json.dumps(dados_processados, indent=4, ensure_ascii=False)

            logger.info("Dados processados e convertidos para JSON com sucesso.")
            print("\n--- SAÍDA JSON GERADA ---")
            print(json_output_string) # Imprime a string JSON (simulando armazenamento em memória)
            print("--- FIM DA SAÍDA JSON ---\n")
    
    logger.info("--- Pipeline de Extração de Vídeos do YouTube Finalizado ---")