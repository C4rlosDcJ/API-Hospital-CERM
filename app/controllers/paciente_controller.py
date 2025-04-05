from flask import request, jsonify
from app.models.paciente import Paciente
from app.models.user import User  # Asegurar importación del modelo User
from app import db

def get_pacientes():
    """Obtiene todos los pacientes"""
    pacientes = Paciente.query.all()
    return jsonify([paciente.to_dict() for paciente in pacientes]), 200

def get_paciente(paciente_id):
    """Obtiene un paciente específico por ID"""
    paciente = Paciente.query.get_or_404(paciente_id)
    return jsonify(paciente.to_dict()), 200

def create_paciente():
    """Crea un nuevo paciente"""
    data = request.get_json()

    # Validación de campos obligatorios
    required_fields = ['user_id', 'nombre']
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return jsonify({'message': f"Faltan campos: {', '.join(missing_fields)}"}), 400

    # Validar existencia del usuario asociado
    if not User.query.get(data['user_id']):
        return jsonify({'message': 'Usuario no encontrado'}), 404

    # Validar grupo sanguíneo
    grupo_sanguineo = data.get('grupo_sanguineo')
    if grupo_sanguineo and grupo_sanguineo not in ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']:
        return jsonify({'message': 'Grupo sanguíneo no válido'}), 400

    # Validar tipos de datos numéricos
    try:
        paciente = Paciente(
            user_id=data['user_id'],
            nombre=data['nombre'],
            edad=int(data['edad']) if 'edad' in data else None,
            grupo_sanguineo=grupo_sanguineo,
            historial_medico=data.get('historial_medico'),
            contacto_emergencia=data.get('contacto_emergencia'),
            peso=float(data['peso']) if 'peso' in data else None,
            altura=float(data['altura']) if 'altura' in data else None
        )
    except (ValueError, TypeError) as e:
        return jsonify({'message': f'Error en tipos de datos: {str(e)}'}), 400

    try:
        db.session.add(paciente)
        db.session.commit()
        return jsonify(paciente.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error al crear el paciente: {str(e)}'}), 500

def update_paciente(paciente_id):
    """Actualiza un paciente existente"""
    paciente = Paciente.query.get_or_404(paciente_id)
    data = request.get_json()

    campos_actualizables = {
        'user_id': int,
        'nombre': str,
        'edad': int,
        'grupo_sanguineo': str,
        'historial_medico': str,
        'contacto_emergencia': str,
        'peso': float,
        'altura': float
    }

    # Validar usuario si se actualiza
    if 'user_id' in data and not User.query.get(data['user_id']):
        return jsonify({'message': 'Usuario no encontrado'}), 404

    # Validar grupo sanguíneo
    if 'grupo_sanguineo' in data and data['grupo_sanguineo'] not in ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']:
        return jsonify({'message': 'Grupo sanguíneo no válido'}), 400

    # Aplicar actualizaciones con validación de tipos
    for campo, tipo in campos_actualizables.items():
        if campo in data:
            try:
                if data[campo] is None:  # Permitir null para campos opcionales
                    setattr(paciente, campo, None)
                else:
                    setattr(paciente, campo, tipo(data[campo]))
            except (ValueError, TypeError) as e:
                return jsonify({'message': f'Formato inválido para {campo}: {str(e)}'}), 400

    try:
        db.session.commit()
        return jsonify(paciente.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error al actualizar el paciente: {str(e)}'}), 500

def delete_paciente(paciente_id):
    """Elimina un paciente"""
    paciente = Paciente.query.get_or_404(paciente_id)
    
    try:
        # Verificar si tiene citas asociadas
        if paciente.citas:
            return jsonify({'message': 'No se puede eliminar, tiene citas asociadas'}), 400
            
        db.session.delete(paciente)
        db.session.commit()
        return jsonify({'message': 'Paciente eliminado correctamente'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error al eliminar el paciente: {str(e)}'}), 500