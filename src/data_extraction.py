import os
import logging
from dotenv import load_dotenv
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from youtube_transcript_api import YouTubeTranscriptApi


def get_video_id_from_url(video_url: str) -> str | None:
    '''
    Extrai o id do vídeo de uma url comum do Youtube.

    Tipos de url:
    - http://www.youtube.com/watch?v=VIDEO_ID&... -> mais comum na barra de pesquisa
    - http://www.youtube.com/watch?v=VIDEO_ID -> versão curta
    - http://youtube.com/v/VIDEO_ID?... -> versão mais antiga
    - http://youtu.be/VIDEO_ID?... -> link de compartilhamento
    - http://www.youtube.com/embed/VIDEO_ID?...  -> vídeos encapsulados em outros sites
    
    param
        video_url: url comum do vídeo

    return
        video_id: string que representa o id do vídeo
    '''

    if not video_url:
        return None

    video_id = None
    if 'watch?v=' in video_url:
        video_id = video_url.split('watch?v=')[1].split('&')[0]
    elif "youtu.be/" in video_url:
        video_id = video_url.split("youtu.be/")[1].split("?")[0]
    elif "embed/" in video_url:
        video_id = video_url.split("embed/")[1].split("?")[0]
    elif "/v/" in video_url:    
         video_id = video_url.split("/v/")[1].split("?")[0]

    if video_id:
        print(f'Vídeo id "{video_id}" extraído com sucesso da url {video_url}')
        return video_id
    else:
        print(f'Não foi possível extrair um vídeo id válido da url: {video_url}')
        return None


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
        video_id = get_video_id_from_url(video_url)

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


def get_transcript(video_url: str) -> list: 
    '''
    Extrai a transcrição de um vídeo do Youtube usando youtube_transcript_api

    args
        video_url: url completa do vídeo do Youtube

    returns
        formatted_transcript: transcrição do vídeo já no formato esperado
    '''
    try:
        video_id = get_video_id_from_url(video_url)
        fetched_transcript = YouTubeTranscriptApi().fetch(video_id, languages=('pt', 'en')).to_raw_data() # já no formato json
        formatted_transcript = [{'start': snippet.get('start'), 'text': snippet.get('text')} for snippet in fetched_transcript]
        print(f'Transcrição extraída com sucesso para o vídeo id: {video_id}')
        return formatted_transcript
    
    except Exception as e:
        print(f'Não foi possível extrair a transcrição do vídeo id {video_id}: {e}')
        return []


if __name__ == '__main__':
    # Carregar variáveis de ambiente
    load_dotenv('./.env')

    video_url = 'https://www.youtube.com/watch?v=N6kdD_x3v1g'
    # metadata = get_metadata(get_youtube_service(), video_url)
    # print(metadata)
    # transcript = get_transcript(video_url)
    # for snippet in transcript:
    #     print(snippet)
    #     break
    print(get_video_id_from_url(video_url))

