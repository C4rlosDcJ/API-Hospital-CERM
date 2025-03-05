from flask import request, jsonify
from app.models.cita import Cita
from app import db

def get_citas():
    citas = Cita.query.all()
    return jsonify([cita.to_dict() for cita in citas]), 200

def get_cita(cita_id):
    cita = Cita.query.get_or_404(cita_id)
    return jsonify(cita.to_dict()), 200

def create_cita():
    data = request.get_json()
    
    # Asegurarse de que se incluya `doctor_id` en la solicitud
    if 'doctor_id' not in data:
        return jsonify({'message': 'doctor_id is required'}), 400

    cita = Cita(
        paciente_id=data['paciente_id'],
        doctor_id=data['doctor_id'],  # Agregado el `doctor_id`
        fecha_hora=data['fecha_hora'],
        estatus=data.get('estatus', 'En proceso'),
        descripcion=data.get('descripcion'),
        codigo=data.get('codigo')
    )
    
    db.session.add(cita)
    db.session.commit()
    return jsonify(cita.to_dict()), 201

def update_cita(cita_id):
    cita = Cita.query.get_or_404(cita_id)
    data = request.get_json()

    # Actualizar los campos, asegurando que `doctor_id` también sea actualizado si está presente
    cita.paciente_id = data.get('paciente_id', cita.paciente_id)
    cita.doctor_id = data.get('doctor_id', cita.doctor_id)  # Actualización de `doctor_id`
    cita.fecha_hora = data.get('fecha_hora', cita.fecha_hora)
    cita.estatus = data.get('estatus', cita.estatus)
    cita.descripcion = data.get('descripcion', cita.descripcion)
    cita.codigo = data.get('codigo', cita.codigo)
    
    db.session.commit()
    return jsonify(cita.to_dict()), 200

def delete_cita(cita_id):
    cita = Cita.query.get_or_404(cita_id)
    db.session.delete(cita)
    db.session.commit()
    return jsonify({'message': 'Cita deleted'}), 200
