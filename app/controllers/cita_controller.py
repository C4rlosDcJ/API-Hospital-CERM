from flask import request, jsonify
from app.models.cita import Cita
from app.models.paciente import Paciente
from app.models.doctor import Doctor
from app.models.oximetro import Oximetro  # Asegurar importación del modelo
from app import db
from datetime import datetime

def get_citas():
    """Obtiene todas las citas"""
    citas = Cita.query.all()
    return jsonify([cita.to_dict() for cita in citas]), 200

def get_cita(cita_id):
    """Obtiene una cita específica por ID"""
    cita = Cita.query.get_or_404(cita_id)
    return jsonify(cita.to_dict()), 200

def search_citas():
    """Busca citas según parámetros específicos"""
    paciente_id = request.args.get('paciente_id', type=int)
    doctor_id = request.args.get('doctor_id', type=int)
    codigo = request.args.get('codigo', type=str)
    estatus = request.args.get('estatus', type=str)

    # Construir la consulta inicial
    query = Cita.query

    # Filtrar por paciente_id si se proporciona
    if paciente_id:
        query = query.filter(Cita.paciente_id == paciente_id)

    # Filtrar por doctor_id si se proporciona
    if doctor_id:
        query = query.filter(Cita.doctor_id == doctor_id)

    # Filtrar por código de cita si se proporciona
    if codigo:
        query = query.filter(Cita.codigo.like(f"%{codigo}%"))

    # Filtrar por estatus si se proporciona
    if estatus:
        query = query.filter(Cita.estatus == estatus)

    # Ejecutar la consulta
    citas = query.all()

    return jsonify([cita.to_dict() for cita in citas]), 200



def create_cita():
    """Crea una nueva cita"""
    data = request.get_json()
    print(f"Datos recibidos: {data}")

    # Validación de campos obligatorios
    required_fields = ['paciente_id', 'doctor_id', 'oximetro_id', 'fecha_hora']
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return jsonify({'message': f"Faltan campos: {', '.join(missing_fields)}"}), 400

    # Convertir IDs a enteros
    try:
        paciente_id = int(data['paciente_id'])
        doctor_id = int(data['doctor_id'])
        oximetro_id = int(data['oximetro_id'])
    except ValueError:
        return jsonify({'message': 'Los IDs deben ser enteros.'}), 400

    # Validar existencia de entidades relacionadas
    paciente = Paciente.query.get(paciente_id)
    doctor = Doctor.query.get(doctor_id)
    oximetro = Oximetro.query.get(oximetro_id)

    if not paciente or not doctor or not oximetro:
        return jsonify({'message': 'Paciente, doctor u oximetro no encontrado.'}), 400

    # Generar el código de la cita (CT- seguido de un número incremental)
    last_cita = Cita.query.order_by(Cita.id.desc()).first()
    last_code = last_cita.codigo if last_cita else 'CT-0'
    last_number = int(last_code.split('-')[1]) if last_cita else 0
    new_code = f"CT-{last_number + 1}"

    # Crear la cita
    cita = Cita(
        paciente_id=paciente_id,
        doctor_id=doctor_id,
        oximetro_id=oximetro_id,
        fecha_hora=data['fecha_hora'],
        estatus=data['estatus'],
        codigo=new_code,  # Asignar el código generado
        diagnostico=data.get('diagnostico', '')  # Si no se pasa diagnóstico, asignar vacío
    )
    
    db.session.add(cita)
    db.session.commit()

    # Responder con éxito
    return jsonify({'message': 'Cita creada exitosamente', 'codigo': new_code, 'diagnostico': cita.diagnostico}), 201


def update_cita(cita_id):
    """Actualiza una cita existente"""
    cita = Cita.query.get_or_404(cita_id)
    data = request.get_json()

    # Campos permitidos para actualización
    campos_actualizables = {
        'paciente_id': int,
        'doctor_id': int,
        'oximetro_id': int,
        'fecha_hora': lambda x: datetime.fromisoformat(x),
        'estatus': str,
        'diagnostico': str,
        'codigo': str
    }

    # Validar existencia de entidades relacionadas
    if 'paciente_id' in data:
        if not Paciente.query.get(data['paciente_id']):
            return jsonify({'message': 'Paciente no encontrado'}), 404

    if 'doctor_id' in data:
        if not Doctor.query.get(data['doctor_id']):
            return jsonify({'message': 'Doctor no encontrado'}), 404

    # Validar nuevo oxímetro si se actualiza
    if 'oximetro_id' in data:
        nuevo_oximetro = Oximetro.query.get(data['oximetro_id'])
        if not nuevo_oximetro:
            return jsonify({'message': 'Oxímetro no encontrado'}), 404
        if nuevo_oximetro.cita and nuevo_oximetro.cita.id != cita_id:
            return jsonify({'message': 'El oxímetro ya está asignado a otra cita'}), 400

    # Validar estatus
    if 'estatus' in data:
        if data['estatus'] not in {'programada', 'en_proceso', 'completada', 'cancelada'}:
            return jsonify({'message': 'Estatus no válido'}), 400

    # Aplicar actualizaciones
    for campo, tipo in campos_actualizables.items():
        if campo in data:
            try:
                if campo == 'fecha_hora':
                    valor = tipo(data[campo])
                else:
                    valor = tipo(data[campo])
                setattr(cita, campo, valor)
            except (ValueError, TypeError) as e:
                return jsonify({'message': f'Formato inválido para {campo}: {str(e)}'}), 400

    try:
        db.session.commit()
        return jsonify(cita.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error al actualizar la cita: {str(e)}'}), 500

def delete_cita(cita_id):
    """Elimina una cita"""
    cita = Cita.query.get_or_404(cita_id)
    try:
        db.session.delete(cita)
        db.session.commit()
        return jsonify({'message': 'Cita eliminada correctamente'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error al eliminar la cita: {str(e)}'}), 500