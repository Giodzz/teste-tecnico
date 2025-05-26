import os
import logging
from dotenv import load_dotenv
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from youtube_transcript_api import YouTubeTranscriptApi


def get_video_id(video_url: str) -> str:
    '''
    Extrai o id do vídeo considerando a url completa
    
    param
        video_url: url completa do vídeo

    return
        video_id: sequencia de caracteres identificador do vídeo (id do vídeo)
    '''
    ini = video_url.find('v=') + 2
    fin = video_url.find('&') if '&' in video_url else len(video_url)
    video_id = video_url[ini:fin]
    return video_id


def get_youtube_service() -> object | None:
    '''
    Constroi e retorna um objeto de serviço API do youtube
    Retorna None, se a chave API não estiver configurada ou se acontecer algum erro
    '''

    api_key = os.getenv('YOUTUBE_API_KEY')
    if not api_key:
        print("A variável de ambiente YOUTUBE_API_KEY não está configurada.")
        return None
    
    try:
        service = build('youtube', 'v3', developerKey=api_key)
        print('Serviço da API do Youtube foi inicializado com sucesso')
        return service
    
    except Exception as e:
        print(f'Erro ao inicializar o serviço da API do Youtube: {e}')
        return None


def get_metadata(service: object, video_url: str) -> dict:
    '''
    Extrai metadados (título e descrição, por padrão) de um vídeo do Youtube usando Youtube Data API v3

    param
        service: o objeto de serviço da API do Youtube inicializado
        video_url: url completa do vídeo do Youtube

    return
    '''

    if not service:
        print('Serviço da API do Youtube não está disponível para buscar metadados.')
        return {'title': None, 'description': None}

    try:
        video_id = get_video_id(video_url)

        request = service.videos().list(
            part='snippet',
            id=video_id
        )
        response = request.execute()

        if response['items']:
            snippet = response['items'][0]['snippet']
            metadata = {
                'title': snippet.get('title'),
                'description': snippet.get('description'),
            }
            print(f'Metadados extraídos com sucesso para o vídeo id: {video_id}')
            return metadata
        else:
            print(f'Nenhum item encontrado para vídeo id: {video_id}')
            return {"title": None, "description": None}

    except HttpError as e:
        print(f"Erro HTTP ao extrair metadados do vídeo ID {video_id} via API: {e}")
        return {"title": None, "description": None}
    
    except Exception as e:
        print(f"Erro inesperado ao extrair metadados do vídeo ID {video_id} via API: {e}")
        return {"title": None, "description": None}


def get_transcript(video_url: str) -> object: 
    
    try:
        video_id = get_video_id(video_url)
        fetched_transcript = YouTubeTranscriptApi().fetch(video_id, languages=('pt', 'en')).to_raw_data() # já no formato json
        formatted_transcript = [{'start': snippet.get('start'), 'text': snippet.get('text')} for snippet in fetched_transcript]
        return formatted_transcript
    
    except Exception as e:
        return None

if __name__ == '__main__':
    # Carregar variáveis de ambiente
    load_dotenv('./.env')

    video_url = 'https://www.youtube.com/watch?v=N6kdD_x3v1g&ab_channel=InvestidorSardinhalRaulSena'
    metadata = get_metadata(get_youtube_service(), video_url)
    print(metadata)
    transcript = get_transcript(video_url)
    for snippet in transcript:
        print(snippet)
        break

