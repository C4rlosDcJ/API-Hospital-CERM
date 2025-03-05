from flask import request, jsonify
from app.models.brazo_robotico import BrazoRobotico
from app import db

def get_brazos_roboticos():
    brazos = BrazoRobotico.query.all()
    return jsonify([brazo.to_dict() for brazo in brazos]), 200

def get_brazo_robotico(brazo_id):
    brazo = BrazoRobotico.query.get_or_404(brazo_id)
    return jsonify(brazo.to_dict()), 200

def create_brazo_robotico():
    data = request.get_json()
    brazo = BrazoRobotico(
        modelo=data['modelo'],
        fabricante=data['fabricante'],
        user_id=data.get('user_id')
    )
    db.session.add(brazo)
    db.session.commit()
    return jsonify(brazo.to_dict()), 201

def update_brazo_robotico(brazo_id):
    brazo = BrazoRobotico.query.get_or_404(brazo_id)
    data = request.get_json()
    brazo.modelo = data.get('modelo', brazo.modelo)
    brazo.fabricante = data.get('fabricante', brazo.fabricante)
    brazo.user_id = data.get('user_id', brazo.user_id)
    db.session.commit()
    return jsonify(brazo.to_dict()), 200

def delete_brazo_robotico(brazo_id):
    brazo = BrazoRobotico.query.get_or_404(brazo_id)
    db.session.delete(brazo)
    db.session.commit()
    return jsonify({'message': 'Brazo Robotico deleted'}), 200