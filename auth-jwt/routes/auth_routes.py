from flask import Blueprint, request, jsonify
from service.security import hash_password, check_password
from flask_jwt_extended import create_access_token
from app import app, db
from models.user import User
from schemas.user_schema import UserSchema

auth_bp = Blueprint('auth', __name__)  # Cria o Blueprint

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    schema = UserSchema()
    errors = schema.validate(data)
    if errors:
        return jsonify(errors), 400
    
    hashed_password = hash_password(data['password'])
    new_user = User(name=data['name'], email=data['email'], password=hashed_password, role=data.get('role', 'CLIENT'))
    db.session.add(new_user)
    db.session.commit()
    return UserSchema.jsonify(new_user), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    
    if user and check_password(user.password, data['password']):
        access_token = create_access_token(identity={'id': user.id, 'role': user.role})
        return jsonify(access_token=access_token), 200
    
    return jsonify({'message': 'Invalid credentials'}), 401