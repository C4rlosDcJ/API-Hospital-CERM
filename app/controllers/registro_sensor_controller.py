from flask import request, jsonify
from app.models.registro_sensor import RegistroSensor
from app import db

def get_registros_sensores():
    registros = RegistroSensor.query.all()
    return jsonify([registro.to_dict() for registro in registros]), 200

def get_registro_sensor(registro_id):
    registro = RegistroSensor.query.get_or_404(registro_id)
    return jsonify(registro.to_dict()), 200

def create_registro_sensor():
    data = request.get_json()
    registro = RegistroSensor(
        sensor_id=data['sensor_id'],
        valor=data['valor'],
        fecha_hora=data['fecha_hora']
    )
    db.session.add(registro)
    db.session.commit()
    return jsonify(registro.to_dict()), 201

def update_registro_sensor(registro_id):
    registro = RegistroSensor.query.get_or_404(registro_id)
    data = request.get_json()
    registro.valor = data.get('valor', registro.valor)
    registro.fecha_hora = data.get('fecha_hora', registro.fecha_hora)
    db.session.commit()
    return jsonify(registro.to_dict()), 200

def delete_registro_sensor(registro_id):
    registro = RegistroSensor.query.get_or_404(registro_id)
    db.session.delete(registro)
    db.session.commit()
    return jsonify({'message': 'Registro Sensor deleted'}), 200