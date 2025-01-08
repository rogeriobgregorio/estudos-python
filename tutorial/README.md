

### Tutorial Completo: Criando uma API REST com Python, Flask e SQLAlchemy

Neste tutorial, criaremos uma API REST usando **Python**, **Flask** e o ORM **SQLAlchemy** (amplamente utilizado com Flask). A API permitirá gerenciar entidades com diferentes tipos de relacionamentos e incluirá autenticação e autorização com **JWT** (JSON Web Tokens).

---

### 1. **Configuração do Ambiente**
1. **Crie um ambiente virtual**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # No Windows: venv\Scripts\activate
   ```

2. **Instale as dependências**:
   ```bash
   pip install flask flask-sqlalchemy flask-migrate flask-jwt-extended marshmallow
   ```

---

### 2. **Estrutura do Projeto**
Organize o projeto da seguinte forma:

```
api/
├── app/
│   ├── __init__.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── post.py
│   │   ├── tag.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth_routes.py
│   │   ├── post_routes.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── user_schema.py
│   │   ├── post_schema.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── jwt_utils.py
│   ├── config.py
│   ├── extensions.py
│   └── exceptions.py
├── migrations/
├── .env
└── run.py
```

---

### 3. **Configuração do Flask**

#### `api/run.py`
```python
from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
```

#### `api/app/__init__.py`
```python
from flask import Flask
from app.extensions import db, migrate, jwt
from app.config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Inicializando extensões
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # Registrando rotas
    from app.routes.auth_routes import auth_bp
    from app.routes.post_routes import post_bp

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(post_bp, url_prefix="/posts")

    return app
```

#### `api/app/config.py`
```python
import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///db.sqlite3")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "jwt_secret_key")
```

#### `api/app/extensions.py`
```python
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
```

---

### 4. **Modelos e Relacionamentos**

#### `api/app/models/user.py`
```python
from app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
```

#### `api/app/models/post.py`
```python
from app.extensions import db

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    user = db.relationship("User", backref=db.backref("posts", lazy=True))
```

#### `api/app/models/tag.py`
```python
from app.extensions import db

post_tag = db.Table(
    'post_tag',
    db.Column('post_id', db.Integer, db.ForeignKey('post.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True),
)

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    posts = db.relationship("Post", secondary=post_tag, back_populates="tags")
```

---

### 5. **Rotas e Autenticação**

#### `api/app/routes/auth_routes.py`
```python
from flask import Blueprint, request, jsonify
from app.models.user import User
from app.extensions import db
from flask_jwt_extended import create_access_token

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"error": "Email already registered"}), 400
    
    user = User(
        username=data["username"],
        email=data["email"]
    )
    user.set_password(data["password"])
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User registered successfully"}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data["email"]).first()
    if user and user.check_password(data["password"]):
        access_token = create_access_token(identity=user.id)
        return jsonify({"access_token": access_token}), 200
    return jsonify({"error": "Invalid credentials"}), 401
```

#### `api/app/routes/post_routes.py`
```python
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.post import Post
from app.models.user import User
from app.extensions import db

post_bp = Blueprint('posts', __name__)

@post_bp.route('/', methods=['POST'])
@jwt_required()
def create_post():
    data = request.get_json()
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return jsonify({"error": "User not found"}), 404

    post = Post(
        title=data["title"],
        content=data["content"],
        user_id=user.id
    )
    db.session.add(post)
    db.session.commit()
    return jsonify({"message": "Post created successfully"}), 201

@post_bp.route('/', methods=['GET'])
@jwt_required()
def get_posts():
    posts = Post.query.all()
    return jsonify([{"id": post.id, "title": post.title} for post in posts])
```

---

### 6. **Marshmallow para Serialização**

Instale o Marshmallow:
```bash
pip install marshmallow
```

Adicione schemas para serializar dados (`app/schemas`).

---

### 7. **Tratamento de Exceções**

Crie um módulo `exceptions.py` para tratar erros globalmente e personalize retornos de erro.

---

### 8. **Migrações**

1. Inicialize o banco:
   ```bash
   flask db init
   ```

2. Gere migrações:
   ```bash
   flask db migrate -m "Initial migration"
   ```

3. Aplique migrações:
   ```bash
   flask db upgrade
   ```

---

### 9. **Testando a API**

Use **Postman** ou **cURL** para testar os endpoints.

**Exemplo**:
```bash
curl -X POST http://127.0.0.1:5000/auth/register -H "Content-Type: application/json" -d '{"username": "john", "email": "john@example.com", "password": "1234"}'
```

---

Pronto! Você criou uma API REST com Flask, SQLAlchemy e autenticação JWT, seguindo boas práticas.