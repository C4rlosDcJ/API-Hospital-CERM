from flask import request, jsonify
from app.models.sensor import Sensor
from app import db

def get_sensores():
    sensores = Sensor.query.all()
    return jsonify([sensor.to_dict() for sensor in sensores]), 200

def get_sensor(sensor_id):
    sensor = Sensor.query.get_or_404(sensor_id)
    return jsonify(sensor.to_dict()), 200

def create_sensor():
    data = request.get_json()
    sensor = Sensor(
        brazo_robotico_id=data['brazo_robotico_id'],
        tipo=data['tipo'],
        unidad_medida=data.get('unidad_medida')
    )
    db.session.add(sensor)
    db.session.commit()
    return jsonify(sensor.to_dict()), 201

def update_sensor(sensor_id):
    sensor = Sensor.query.get_or_404(sensor_id)
    data = request.get_json()
    sensor.tipo = data.get('tipo', sensor.tipo)
    sensor.unidad_medida = data.get('unidad_medida', sensor.unidad_medida)
    db.session.commit()
    return jsonify(sensor.to_dict()), 200

def delete_sensor(sensor_id):
    sensor = Sensor.query.get_or_404(sensor_id)
    db.session.delete(sensor)
    db.session.commit()
    return jsonify({'message': 'Sensor deleted'}), 200