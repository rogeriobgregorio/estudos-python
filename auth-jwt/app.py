from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from config import Config

# Inicializar a aplicação e as extensões
app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
jwt = JWTManager(app)

# Importar as rotas e modelos
from routes.auth_routes import *
from routes.user_routes import *

# Criar banco e adicionar usuário ADMIN padrão
@app.before_first_request
def create_tables():
    db.create_all()
    if not User.query.filter_by(email='admin@example.com').first():
        admin = User(name='Admin', email='admin@example.com', password=generate_password_hash('admin123'), role='ADMIN')
        db.session.add(admin)
        db.session.commit()

if __name__ == '__main__':
    app.run(debug=True)
    