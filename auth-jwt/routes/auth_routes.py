from flask import request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from app import app, db
from models.user import User
from schemas.user_schema import UserSchema

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    errors = UserSchema.validate(data)
    if errors:
        return jsonify(errors), 400
    
    hashed_password = generate_password_hash(data['password'])
    new_user = User(name=data['name'], email=data['email'], password=hashed_password, role=data.get('role', 'CLIENT'))
    db.session.add(new_user)
    db.session.commit()
    return UserSchema.jsonify(new_user), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    
    if user and check_password_hash(user.password, data['password']):
        access_token = create_access_token(identity={'id': user.id, 'role': user.role})
        return jsonify(access_token=access_token), 200
    
    return jsonify({'message': 'Invalid credentials'}), 401