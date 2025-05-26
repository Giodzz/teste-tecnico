import os
from dotenv import load_dotenv
import logging

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
main_logger = logging.getLogger(__name__)

# Carregar variáveis de ambiente
project_root_dir = os.path.dirname(os.path.abspath(__file__))
dotenv_path = os.path.join(project_root_dir, '.env')
load_dotenv(dotenv_path)

# acessar variável de ambiente
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")


