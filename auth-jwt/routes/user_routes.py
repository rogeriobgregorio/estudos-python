from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import app, db
from models.user import User
from schemas.user_schema import UserSchema, users_schema
from werkzeug.security import generate_password_hash

@app.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    identity = get_jwt_identity()
    user = User.query.get(identity['id'])
    return UserSchema.jsonify(user)

@app.route('/users', methods=['GET'])
@jwt_required()
def get_users():
    identity = get_jwt_identity()
    if identity['role'] != 'ADMIN':
        return jsonify({'message': 'Unauthorized'}), 403
    
    users = User.query.all()
    return users_schema.jsonify(users)

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
    return UserSchema.jsonify(user)

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
