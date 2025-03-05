from flask import request, jsonify
from app.models.paciente import Paciente
from app import db

def get_pacientes():
    pacientes = Paciente.query.all()
    return jsonify([paciente.to_dict() for paciente in pacientes]), 200

def get_paciente(paciente_id):
    paciente = Paciente.query.get_or_404(paciente_id)
    return jsonify(paciente.to_dict()), 200

def create_paciente():
    data = request.get_json()
    paciente = Paciente(
        user_id=data['user_id'],
        nombre=data['nombre'],
        edad=data.get('edad'),
        historial_medico=data.get('historial_medico')
    )
    db.session.add(paciente)
    db.session.commit()
    return jsonify(paciente.to_dict()), 201

def update_paciente(paciente_id):
    paciente = Paciente.query.get_or_404(paciente_id)
    data = request.get_json()
    paciente.nombre = data.get('nombre', paciente.nombre)
    paciente.edad = data.get('edad', paciente.edad)
    paciente.historial_medico = data.get('historial_medico', paciente.historial_medico)
    db.session.commit()
    return jsonify(paciente.to_dict()), 200

def delete_paciente(paciente_id):
    paciente = Paciente.query.get_or_404(paciente_id)
    db.session.delete(paciente)
    db.session.commit()
    return jsonify({'message': 'Paciente deleted'}), 200