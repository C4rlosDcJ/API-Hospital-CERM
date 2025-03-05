from flask import request, jsonify
from app.models.operacion import Operacion
from app import db

def get_operaciones():
    operaciones = Operacion.query.all()
    return jsonify([operacion.to_dict() for operacion in operaciones]), 200

def get_operacion(operacion_id):
    operacion = Operacion.query.get_or_404(operacion_id)
    return jsonify(operacion.to_dict()), 200

def create_operacion():
    data = request.get_json()
    operacion = Operacion(
        brazo_robotico_id=data['brazo_robotico_id'],
        paciente_id=data['paciente_id'],
        tipo=data.get('tipo', 'inyeccion'),
        estado=data.get('estado', 'pendiente'),
        fecha_hora=data['fecha_hora'],
        observaciones=data.get('observaciones')
    )
    db.session.add(operacion)
    db.session.commit()
    return jsonify(operacion.to_dict()), 201

def update_operacion(operacion_id):
    operacion = Operacion.query.get_or_404(operacion_id)
    data = request.get_json()
    operacion.tipo = data.get('tipo', operacion.tipo)
    operacion.estado = data.get('estado', operacion.estado)
    operacion.fecha_hora = data.get('fecha_hora', operacion.fecha_hora)
    operacion.observaciones = data.get('observaciones', operacion.observaciones)
    db.session.commit()
    return jsonify(operacion.to_dict()), 200

def delete_operacion(operacion_id):
    operacion = Operacion.query.get_or_404(operacion_id)
    db.session.delete(operacion)
    db.session.commit()
    return jsonify({'message': 'Operacion deleted'}), 200