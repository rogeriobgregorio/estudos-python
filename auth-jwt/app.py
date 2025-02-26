from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from config import Config
from flask_cors import CORS 
from models.user import User
from werkzeug.security import generate_password_hash
import logging

logging.basicConfig(level=logging.DEBUG)

# Inicializa a aplicação e as extensões
app = Flask(__name__)
app.config['DEBUG'] = True
app.config['ENV'] = 'development'
app.config.from_object(Config)

# Configuração do CORS
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

db = SQLAlchemy(app)
jwt = JWTManager(app)

migrate = Migrate(app, db)

# Importa as rotas e modelos
from routes.auth_routes import *
from routes.user_routes import *

@app.route('/')
def index():
    return 'Bem-vindo à aplicação!'

# Cria o banco e adiciona o usuário ADMIN padrão
@app.before_first_request
def create_tables():
    if not User.query.filter_by(email='admin@email.com').first():
        admin = User(
            name='Admin', 
            email='admin@email.com', 
            password=generate_password_hash('admin123'), 
            role='ADMIN'
        )
        db.session.add(admin)
        db.session.commit()

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True) 
    