from flask import request, jsonify
from app.models.doctor import Doctor
from app import db

def get_doctores():
    doctores = Doctor.query.all()
    return jsonify([doctor.to_dict() for doctor in doctores]), 200

def get_doctor(doctor_id):
    doctor = Doctor.query.get_or_404(doctor_id)
    return jsonify(doctor.to_dict()), 200

def create_doctor():
    data = request.get_json()
    doctor = Doctor(
        user_id=data['user_id'],
        nombre=data['nombre'],
        especialidad=data['especialidad']
    )
    db.session.add(doctor)
    db.session.commit()
    return jsonify(doctor.to_dict()), 201

def update_doctor(doctor_id):
    doctor = Doctor.query.get_or_404(doctor_id)
    data = request.get_json()
    doctor.nombre = data.get('nombre', doctor.nombre)
    doctor.especialidad = data.get('especialidad', doctor.especialidad)
    db.session.commit()
    return jsonify(doctor.to_dict()), 200

def delete_doctor(doctor_id):
    doctor = Doctor.query.get_or_404(doctor_id)
    db.session.delete(doctor)
    db.session.commit()
    return jsonify({'message': 'Doctor deleted'}), 200