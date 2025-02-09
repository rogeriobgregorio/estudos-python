from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from marshmallow import Schema, fields, validate
from datetime import timedelta

# Inicialização da aplicação Flask
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['JWT_SECRET_KEY'] = 'supersecretkey'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)

db = SQLAlchemy(app)
jwt = JWTManager(app)

# Modelo de Usuário
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(10), nullable=False, default='CLIENT')

# Esquema para validação e serialização com Marshmallow
class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=2))
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True)
    role = fields.Str(validate=validate.OneOf(['ADMIN', 'CLIENT']))

user_schema = UserSchema()
users_schema = UserSchema(many=True)

# Rota para cadastro de usuário
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    errors = user_schema.validate(data)
    if errors:
        return jsonify(errors), 400
    
    hashed_password = generate_password_hash(data['password'])
    new_user = User(name=data['name'], email=data['email'], password=hashed_password, role=data.get('role', 'CLIENT'))
    db.session.add(new_user)
    db.session.commit()
    return user_schema.jsonify(new_user), 201

# Rota de login
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    
    if user and check_password_hash(user.password, data['password']):
        access_token = create_access_token(identity={'id': user.id, 'role': user.role})
        return jsonify(access_token=access_token), 200
    
    return jsonify({'message': 'Invalid credentials'}), 401

# Rota para obter informações do usuário logado
@app.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    identity = get_jwt_identity()
    user = User.query.get(identity['id'])
    return user_schema.jsonify(user)

# Rota para listar todos os usuários (somente ADMIN)
@app.route('/users', methods=['GET'])
@jwt_required()
def get_users():
    identity = get_jwt_identity()
    if identity['role'] != 'ADMIN':
        return jsonify({'message': 'Unauthorized'}), 403
    
    users = User.query.all()
    return users_schema.jsonify(users)

# Rota para atualizar usuário
@app.route('/users/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    identity = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user or (identity['role'] != 'ADMIN' and identity['id'] != user.id):
        return jsonify({'message': 'Unauthorized'}), 403
    
    data = request.get_json()
    user.name = data.get('name', user.name)
    user.email = data.get('email', user.email)
    if 'password' in data:
        user.password = generate_password_hash(data['password'])
    
    db.session.commit()
    return user_schema.jsonify(user)

# Rota para deletar usuário
@app.route('/users/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    identity = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user or (identity['role'] != 'ADMIN' and identity['id'] != user.id):
        return jsonify({'message': 'Unauthorized'}), 403
    
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted'}), 200

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
