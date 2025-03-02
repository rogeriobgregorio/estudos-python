import os
from datetime import timedelta
from dotenv import load_dotenv

# Carregar as variáveis de ambiente do arquivo .env
load_dotenv()

class Config:
    # Usando o "os" para garantir que a pasta 'instance' exista e o caminho seja construído corretamente
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))  # Diretorio base
    INSTANCE_FOLDER = os.path.join(BASE_DIR, 'instance')
    
    # Certifica que a pasta 'instance' existe
    if not os.path.exists(INSTANCE_FOLDER):
        os.makedirs(INSTANCE_FOLDER)
    
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(INSTANCE_FOLDER, "users.db")}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Acesso a chave secreta de forma segura
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'fallback_secret_key')  # Valor de fallback se não encontrar no .env
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    
    DEBUG = True
    FLASK_ENV = "development"  # Modo de ambiente do Flask
