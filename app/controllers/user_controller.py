from flask import request, jsonify
from app.models.user import User
from app import db

def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users]), 200


def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_dict()), 200

def create_user():
    data = request.get_json()
    user = User(
        name=data['name'],
        email=data['email'],
        password=data['password'],
        role=data.get('role', 'paciente')
    )
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_dict()), 201

def update_user(user_id):
    user = User.query.get_or_404(user_id)
    data = request.get_json()
    user.name = data.get('name', user.name)
    user.email = data.get('email', user.email)
    user.password = data.get('password', user.password)
    user.role = data.get('role', user.role)
    db.session.commit()
    return jsonify(user.to_dict()), 200

def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted'}), 200