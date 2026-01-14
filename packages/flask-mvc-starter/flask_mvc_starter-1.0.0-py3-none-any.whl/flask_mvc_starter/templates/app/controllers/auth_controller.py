from flask_restful import Resource
from flask import request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token
from app.models import db, User
from app.utils.validators import validate_email, validate_password


class RegisterResource(Resource):
    def post(self):
        data = request.get_json()
        
        if not data:
            return {'message': 'No input data provided'}, 400
        
        email = data.get('email', '').strip()
        password = data.get('password', '')
        
        if not email or not password:
            return {'message': 'Email and password are required'}, 400
        
        if not validate_email(email):
            return {'message': 'Invalid email format'}, 400
        
        if not validate_password(password):
            return {'message': 'Password must be at least 6 characters'}, 400
        
        if User.query.filter_by(email=email).first():
            return {'message': 'User already exists'}, 400
        
        password_hash = generate_password_hash(password)
        user = User(email=email, password_hash=password_hash)
        db.session.add(user)
        db.session.commit()
        
        return {
            'message': 'User registered successfully',
            'user_id': user.id,
            'email': user.email
        }, 201


class LoginResource(Resource):
    def post(self):
        data = request.get_json()
        
        if not data:
            return {'message': 'No input data provided'}, 400
        
        email = data.get('email', '').strip()
        password = data.get('password', '')
        
        if not email or not password:
            return {'message': 'Email and password are required'}, 400
        
        user = User.query.filter_by(email=email).first()
        
        if not user or not check_password_hash(user.password_hash, password):
            return {'message': 'Invalid credentials'}, 401
        
        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)
        
        return {
            'access_token': access_token,
            'refresh_token': refresh_token,
            'user_id': user.id,
            'email': user.email
        }, 200
