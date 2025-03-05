from flask import request, jsonify
from app.models.historial_inyeccion import HistorialInyeccion
from app import db

def get_historial_inyecciones():
    historiales = HistorialInyeccion.query.all()
    return jsonify([historial.to_dict() for historial in historiales]), 200

def get_historial_inyeccion(historial_id):
    historial = HistorialInyeccion.query.get_or_404(historial_id)
    return jsonify(historial.to_dict()), 200

def create_historial_inyeccion():
    data = request.get_json()
    historial = HistorialInyeccion(
        paciente_id=data['paciente_id'],
        operacion_id=data['operacion_id'],
        observaciones=data.get('observaciones')
    )
    db.session.add(historial)
    db.session.commit()
    return jsonify(historial.to_dict()), 201

def update_historial_inyeccion(historial_id):
    historial = HistorialInyeccion.query.get_or_404(historial_id)
    data = request.get_json()
    historial.observaciones = data.get('observaciones', historial.observaciones)
    db.session.commit()
    return jsonify(historial.to_dict()), 200

def delete_historial_inyeccion(historial_id):
    historial = HistorialInyeccion.query.get_or_404(historial_id)
    db.session.delete(historial)
    db.session.commit()
    return jsonify({'message': 'Historial Inyeccion deleted'}), 200