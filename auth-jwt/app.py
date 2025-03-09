from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from config import Config
from flask_cors import CORS 
import logging

# Importa os Blueprints
from routes.auth_routes import auth_bp
from routes.user_routes import user_bp

logging.basicConfig(level=logging.DEBUG)

# Inicializa a aplicação e as extensões
app = Flask(__name__)
app.config['DEBUG'] = True
app.config['ENV'] = 'development'
app.config.from_object(Config)

# Configuração do CORS
CORS(app, resources={r"/*": {
    "origins": "*",  # Permite todos os domínios
    "methods": ["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],  # Permite todos os métodos HTTP
    "allow_headers": "*",  # Permite todos os cabeçalhos
    "supports_credentials": True  # Permite credenciais
}})

# Inicializa o banco de dados com configuração de pool
db = SQLAlchemy(app, engine_options=Config.SQLALCHEMY_ENGINE_OPTIONS)
jwt = JWTManager(app)
migrate = Migrate(app, db)

# Registra os Blueprints
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(user_bp, url_prefix='/api')

@app.route('/')
def index():
    return 'Bem-vindo à aplicação!'

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True) 
    