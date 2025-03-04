from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import app, db
from models.user import User
from schemas.user_schema import UserSchema, users_schema
from werkzeug.security import generate_password_hash

user_bp = Blueprint('user', __name__)  # Cria o Blueprint

def check_user_permission(user, identity, required_role):
    if identity['role'] != required_role and identity['id'] != user.id:
        return jsonify({'message': 'Unauthorized'}), 403
    return None  

@user_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    identity = get_jwt_identity()
    user = User.query.get(identity['id'])
    return UserSchema.jsonify(user)

@user_bp.route('/users', methods=['GET'])
@jwt_required()
def get_users():
    identity = get_jwt_identity()
    if identity['role'] != 'ADMIN':
        return jsonify({'message': 'Unauthorized'}), 403
    
    users = User.query.all()
    return users_schema.jsonify(users)

@user_bp.route('/users/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    identity = get_jwt_identity()
    user = User.query.get(user_id)
    
    permission_error = check_user_permission(user, identity, 'ADMIN')
    if permission_error:
        return permission_error
    
    data = request.get_json()
    user.name = data.get('name', user.name)
    user.email = data.get('email', user.email)
    if 'password' in data:
        user.password = generate_password_hash(data['password'])
    
    db.session.commit()
    return UserSchema.jsonify(user)

@user_bp.route('/users/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    identity = get_jwt_identity()
    user = User.query.get(user_id)
    
    permission_error = check_user_permission(user, identity, 'ADMIN')
    if permission_error:
        return permission_error
    
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted'}), 200
