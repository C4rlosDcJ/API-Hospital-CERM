from flask import Blueprint, request, jsonify, current_app
from app.controllers.registro_sensor_oximetro import SensorOximetroController
from collections import deque
import time
import logging
from datetime import datetime


from app.controllers import (
    get_users, get_user, create_user, update_user, delete_user,
    get_brazos_roboticos, get_brazo_robotico, create_brazo_robotico, 
    update_brazo_robotico, delete_brazo_robotico,
    get_pacientes, get_paciente, create_paciente, 
    update_paciente, delete_paciente,
    get_doctores, get_doctor, create_doctor, 
    update_doctor, delete_doctor,
    get_sensores, get_sensor, create_sensor, 
    update_sensor, delete_sensor,
    get_operaciones, get_operacion, create_operacion, 
    update_operacion, delete_operacion,
    get_registros_sensores, get_registro_sensor, 
    create_registro_sensor, update_registro_sensor, delete_registro_sensor,
    get_historial_inyecciones, get_historial_inyeccion, 
    create_historial_inyeccion, update_historial_inyeccion, delete_historial_inyeccion,
    get_citas, get_cita, create_cita, update_cita, delete_cita, search_citas
)

# Crear un Blueprint para las rutas
main_routes = Blueprint('main', __name__)


# ==================================================
# Rutas para Users
# ==================================================
@main_routes.route('/users', methods=['GET'])
def list_users():
    return get_users()

@main_routes.route('/users/<int:user_id>', methods=['GET'])
def show_user(user_id):
    return get_user(user_id)

@main_routes.route('/users', methods=['POST'])
def add_user():
    return create_user()

@main_routes.route('/users/<int:user_id>', methods=['PUT'])
def modify_user(user_id):
    return update_user(user_id)

@main_routes.route('/users/<int:user_id>', methods=['DELETE'])
def remove_user(user_id):
    return delete_user(user_id)

# ==================================================
# Rutas para Citas
# ==================================================
@main_routes.route('/citas', methods=['GET'])
def list_citas():
    return get_citas()

@main_routes.route('/citas/search', methods=['GET'])
def citas_search():
    return search_citas()

@main_routes.route('/citas/<int:cita_id>', methods=['GET'])
def show_cita(cita_id):
    return get_cita(cita_id)

@main_routes.route('/citas', methods=['POST'])
def add_cita():
    return create_cita()

@main_routes.route('/citas/<int:cita_id>', methods=['PUT'])
def modify_cita(cita_id):
    return update_cita(cita_id)

@main_routes.route('/citas/<int:cita_id>', methods=['DELETE'])
def remove_cita(cita_id):
    return delete_cita(cita_id)
# ==================================================
# Rutas para Brazos Robóticos
# ==================================================
@main_routes.route('/brazos-roboticos', methods=['GET'])
def list_brazos_roboticos():
    return get_brazos_roboticos()

@main_routes.route('/brazos-roboticos/<int:brazo_id>', methods=['GET'])
def show_brazo_robotico(brazo_id):
    return get_brazo_robotico(brazo_id)

@main_routes.route('/brazos-roboticos', methods=['POST'])
def add_brazo_robotico():
    return create_brazo_robotico()

@main_routes.route('/brazos-roboticos/<int:brazo_id>', methods=['PUT'])
def modify_brazo_robotico(brazo_id):
    return update_brazo_robotico(brazo_id)

@main_routes.route('/brazos-roboticos/<int:brazo_id>', methods=['DELETE'])
def remove_brazo_robotico(brazo_id):
    return delete_brazo_robotico(brazo_id)

# ==================================================
# Rutas para Pacientes
# ==================================================
@main_routes.route('/pacientes', methods=['GET'])
def list_pacientes():
    return get_pacientes()

@main_routes.route('/pacientes/<int:paciente_id>', methods=['GET'])
def show_paciente(paciente_id):
    return get_paciente(paciente_id)

@main_routes.route('/pacientes', methods=['POST'])
def add_paciente():
    return create_paciente()

@main_routes.route('/pacientes/<int:paciente_id>', methods=['PUT'])
def modify_paciente(paciente_id):
    return update_paciente(paciente_id)

@main_routes.route('/pacientes/<int:paciente_id>', methods=['DELETE'])
def remove_paciente(paciente_id):
    return delete_paciente(paciente_id)

# ==================================================
# Rutas para Doctores
# ==================================================
@main_routes.route('/doctores', methods=['GET'])
def list_doctores():
    return get_doctores()

@main_routes.route('/doctores/<int:doctor_id>', methods=['GET'])
def show_doctor(doctor_id):
    return get_doctor(doctor_id)

@main_routes.route('/doctores', methods=['POST'])
def add_doctor():
    return create_doctor()

@main_routes.route('/doctores/<int:doctor_id>', methods=['PUT'])
def modify_doctor(doctor_id):
    return update_doctor(doctor_id)

@main_routes.route('/doctores/<int:doctor_id>', methods=['DELETE'])
def remove_doctor(doctor_id):
    return delete_doctor(doctor_id)

# ==================================================
# Rutas para Sensores
# ==================================================
@main_routes.route('/sensores', methods=['GET'])
def list_sensores():
    return get_sensores()

@main_routes.route('/sensores/<int:sensor_id>', methods=['GET'])
def show_sensor(sensor_id):
    return get_sensor(sensor_id)

@main_routes.route('/sensores', methods=['POST'])
def add_sensor():
    return create_sensor()

@main_routes.route('/sensores/<int:sensor_id>', methods=['PUT'])
def modify_sensor(sensor_id):
    return update_sensor(sensor_id)

@main_routes.route('/sensores/<int:sensor_id>', methods=['DELETE'])
def remove_sensor(sensor_id):
    return delete_sensor(sensor_id)

# ==================================================
# Rutas para Operaciones
# ==================================================
@main_routes.route('/operaciones', methods=['GET'])
def list_operaciones():
    return get_operaciones()

@main_routes.route('/operaciones/<int:operacion_id>', methods=['GET'])
def show_operacion(operacion_id):
    return get_operacion(operacion_id)

@main_routes.route('/operaciones', methods=['POST'])
def add_operacion():
    return create_operacion()

@main_routes.route('/operaciones/<int:operacion_id>', methods=['PUT'])
def modify_operacion(operacion_id):
    return update_operacion(operacion_id)

@main_routes.route('/operaciones/<int:operacion_id>', methods=['DELETE'])
def remove_operacion(operacion_id):
    return delete_operacion(operacion_id)

# ==================================================
# Rutas para Registros de Sensores
# ==================================================
@main_routes.route('/registros-sensores', methods=['GET'])
def list_registros_sensores():
    return get_registros_sensores()

@main_routes.route('/registros-sensores/<int:registro_id>', methods=['GET'])
def show_registro_sensor(registro_id):
    return get_registro_sensor(registro_id)

@main_routes.route('/registros-sensores', methods=['POST'])
def add_registro_sensor():
    return create_registro_sensor()

@main_routes.route('/registros-sensores/<int:registro_id>', methods=['PUT'])
def modify_registro_sensor(registro_id):
    return update_registro_sensor(registro_id)

@main_routes.route('/registros-sensores/<int:registro_id>', methods=['DELETE'])
def remove_registro_sensor(registro_id):
    return delete_registro_sensor(registro_id)

# ==================================================
# Rutas para Historial de Inyecciones
# ==================================================
@main_routes.route('/historial-inyecciones', methods=['GET'])
def list_historial_inyecciones():
    return get_historial_inyecciones()

@main_routes.route('/historial-inyecciones/<int:historial_id>', methods=['GET'])
def show_historial_inyeccion(historial_id):
    return get_historial_inyeccion(historial_id)

@main_routes.route('/historial-inyecciones', methods=['POST'])
def add_historial_inyeccion():
    return create_historial_inyeccion()

@main_routes.route('/historial-inyecciones/<int:historial_id>', methods=['PUT'])
def modify_historial_inyeccion(historial_id):
    return update_historial_inyeccion(historial_id)

@main_routes.route('/historial-inyecciones/<int:historial_id>', methods=['DELETE'])
def remove_historial_inyeccion(historial_id):
    return delete_historial_inyeccion(historial_id)




# # Sensor Oximetro
# @main_routes.route('/data', methods=['POST'])
# def create_data():
#     return SensorOximetroController.create_sensor_data()

# @main_routes.route('/data', methods=['GET'])
# def get_data():
#     return SensorOximetroController.get_sensor_data()

@main_routes.route('/data/all', methods=['GET'])
def get_all_sensor_data():
    return SensorOximetroController.get_all_sensor_data()


# Variable global para comando actual
current_command = None

# Ruta para manejar comandos (POST para establecer, GET para obtener)
@main_routes.route('/command', methods=['POST', 'GET'])
def handle_command():
    global current_command

    if request.method == 'POST':
        data = request.get_json()
        current_command = data
        return jsonify({'status': 'success'})

    elif request.method == 'GET':
        if current_command:
            response = current_command
            current_command = None
            return jsonify(response)
        return jsonify({'status': 'no command'})
    


# Oximetro

# Configuración
logging.basicConfig(level=logging.INFO)
data = deque(maxlen=100)  # Buffer circular

# Umbrales médicos actualizados
MEDICAL_RANGES = {
    'spo2': {
        'normal': (95, 100),
        'hypoxia': (90, 94),
        'severe_hypoxia': (0, 89)
    },
    'bpm': {
        'normal': (60, 100),
        'bradycardia': (40, 59),
        'tachycardia': (101, 140)
    },
    'temperature': {
        'normal': (30, 37.5),
        'hypothermia': (0, 35.9),
        'fever': (37.6, 39.9),
        'hyperpyrexia': (40.0, 45.0)
    }
}
@main_routes.route('/data', methods=['POST'])
def receive_data():
    try:
        # Parseo y validación mejorada
        sensor_data = {
            'dc_red': float(request.form.get('red', 0)),
            'dc_ir': float(request.form.get('ir', 0)),
            'spo2': float(request.form.get('spo2', 0)),
            'bpm': int(request.form.get('bpm', 0)),
            'temp': float(request.form.get('temp', 0)),
            'timestamp': int(request.form.get('t', 0)),
            'raw_red': float(request.form.get('red', 0)),  # Para análisis futuro
            'raw_ir': float(request.form.get('ir', 0))     # Para análisis futuro
        }

        # Validación avanzada
        if not (0 <= sensor_data['spo2'] <= 100):
            raise ValueError("SpO2 fuera de rango (0-100%)")
        if not (30 <= sensor_data['bpm'] <= 200):
            raise ValueError("BPM fuera de rango (30-200)")
        if not (25.0 <= sensor_data['temp'] <= 45.0):
            raise ValueError("Temperatura fuera de rango (25-45°C)")

        # Metadata adicional
        sensor_data['received_at'] = datetime.now().isoformat()
        sensor_data['processed'] = False  # Para procesamiento posterior
        
        data.append(sensor_data)
        current_app.logger.info(f"Datos recibidos: {sensor_data}")
        
        return jsonify({'status': 'success', 'message': 'Datos almacenados'}), 200
        
    except Exception as e:
        current_app.logger.error(f"Error: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 400

# Actualizar la ruta /get_data
@main_routes.route('/get_data', methods=['GET'])
def get_data():
    try:
        response_data = {
            'status': 'success',
            'data': list(data),
            'diagnosis': generate_empty_diagnosis(),
            'signal_quality': 'unknown',
            'trends': {}
        }

        if data:
            latest = data[-1]
            response_data['diagnosis'] = generate_diagnosis(latest)
            response_data['stats'] = calculate_statistics()
            response_data['signal_quality'] = calculate_signal_quality(latest)
            response_data['trends'] = calculate_trends()

        return jsonify(response_data)
        
    except Exception as e:
        current_app.logger.error(f"Error: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e),
            'data': [],
            'diagnosis': generate_error_diagnosis(str(e))
        }), 500
    
# Añadir función de tendencias
def calculate_trends():
    """Calcula tendencias de los últimos 10 datos"""
    if len(data) < 2:
        return {}
    
    trends = {}
    last_10 = list(data)[-10:]
    
    for metric in ['spo2', 'bpm', 'temp']:
        values = [x[metric] for x in last_10]
        avg_change = (values[-1] - values[0]) / len(values)
        
        if abs(avg_change) < 0.5:
            trends[metric] = 'stable'
        elif avg_change > 0:
            trends[metric] = 'rising'
        else:
            trends[metric] = 'falling'
    
    return trends

def calculate_statistics():
    """Calcula estadísticas avanzadas de los datos históricos"""
    if not data:
        return {}

    stats = {
        'spo2': {'min': 100, 'max': 0, 'avg': 0},
        'bpm': {'min': 200, 'max': 0, 'avg': 0},
        'temp': {'min': 45.0, 'max': 0.0, 'avg': 0.0}
    }

    total = len(data)
    for entry in data:
        for metric in ['spo2', 'bpm', 'temp']:
            stats[metric]['min'] = min(stats[metric]['min'], entry[metric])
            stats[metric]['max'] = max(stats[metric]['max'], entry[metric])
            stats[metric]['avg'] += entry[metric]

    for metric in stats:
        stats[metric]['avg'] = round(stats[metric]['avg'] / total, 1)

    return stats

# Modificar la función generate_diagnosis
def generate_diagnosis(reading):
    """Genera diagnóstico médico integrado con estructura para el frontend"""
    diagnosis = {
        'spo2': {
            **analyze_spo2(reading['spo2']),
            'value': reading['spo2'],
            'normal_range': f"{MEDICAL_RANGES['spo2']['normal'][0]}-{MEDICAL_RANGES['spo2']['normal'][1]}%"
        },
        'bpm': {
            **analyze_bpm(reading['bpm']),
            'value': reading['bpm'],
            'normal_range': f"{MEDICAL_RANGES['bpm']['normal'][0]}-{MEDICAL_RANGES['bpm']['normal'][1]} bpm"
        },
        'temp': {
            **analyze_temp(reading['temp']),
            'value': reading['temp'],
            'normal_range': f"{MEDICAL_RANGES['temperature']['normal'][0]}-{MEDICAL_RANGES['temperature']['normal'][1]}°C"
        },
        'messages': [],
        'severity': 'normal',
        'timestamp': reading['received_at']
    }

    # Determinar severidad y mensajes (mantenemos la lógica original)
    severities = {'normal': 0, 'warning': 1, 'critical': 2}
    for metric in ['spo2', 'bpm', 'temp']:
        if severities[diagnosis[metric]['severity']] > severities[diagnosis['severity']]:
            diagnosis['severity'] = diagnosis[metric]['severity']
    
    diagnosis['messages'] = [diagnosis[metric]['description'] for metric in ['spo2', 'bpm', 'temp'] 
                            if diagnosis[metric]['status'] != 'Normal']
    
    if not diagnosis['messages']:
        diagnosis['messages'].append("Todos los parámetros están dentro de rangos normales")

    return diagnosis

# Añadir función para calidad de señal
def calculate_signal_quality(entry):
    """Determina la calidad de señal basada en los valores RAW"""
    ir = abs(entry['raw_ir'])
    red = abs(entry['raw_red'])
    
    if ir > 50000 and red > 50000:
        return 'excellent'
    elif ir > 30000 or red > 30000:
        return 'weak'
    else:
        return 'poor'

def analyze_spo2(value):
    ranges = MEDICAL_RANGES['spo2']
    if value >= ranges['normal'][0]:
        return medical_condition('Normal', 'normal', 'fa-check-circle', f"SpO2 normal ({value}%)")
    elif value >= ranges['hypoxia'][0]:
        return medical_condition('Hipoxia leve', 'warning', 'fa-exclamation-circle', 
                              f"Oxigenación sanguínea baja ({value}%)")
    else:
        return medical_condition('Hipoxia severa', 'critical', 'fa-exclamation-triangle',
                              f"Oxigenación sanguínea peligrosamente baja ({value}%)")

def analyze_bpm(value):
    ranges = MEDICAL_RANGES['bpm']
    if ranges['normal'][0] <= value <= ranges['normal'][1]:
        return medical_condition('Normal', 'normal', 'fa-check-circle', f"Ritmo cardíaco normal ({value} bpm)")
    elif ranges['bradycardia'][0] <= value <= ranges['bradycardia'][1]:
        return medical_condition('Bradicardia', 'warning', 'fa-exclamation-circle',
                               f"Ritmo cardíaco lento ({value} bpm)")
    elif ranges['tachycardia'][0] <= value <= ranges['tachycardia'][1]:
        return medical_condition('Taquicardia', 'warning', 'fa-exclamation-circle',
                               f"Ritmo cardíaco acelerado ({value} bpm)")
    else:
        return medical_condition('Arritmia', 'critical', 'fa-exclamation-triangle',
                               f"Ritmo cardíaco peligroso ({value} bpm)")

def analyze_temp(value):
    ranges = MEDICAL_RANGES['temperature']
    if ranges['normal'][0] <= value <= ranges['normal'][1]:
        return medical_condition('Normal', 'normal', 'fa-check-circle', f"Temperatura normal ({value}°C)")
    elif value <= ranges['hypothermia'][1]:
        return medical_condition('Hipotermia', 'critical', 'fa-exclamation-triangle',
                               f"Temperatura corporal baja ({value}°C)")
    elif ranges['fever'][0] <= value <= ranges['fever'][1]:
        return medical_condition('Fiebre', 'warning', 'fa-exclamation-circle',
                               f"Temperatura elevada ({value}°C)")
    else:
        return medical_condition('Hiperpirexia', 'critical', 'fa-exclamation-triangle',
                               f"Temperatura peligrosamente alta ({value}°C)")

def medical_condition(status, severity, icon, description):
    return {
        'status': status,
        'severity': severity,
        'icon': icon,
        'description': description
    }

def generate_empty_diagnosis():
    return {
        'spo2': medical_condition('Sin datos', 'normal', 'fa-question-circle', "Esperando datos de SpO2"),
        'bpm': medical_condition('Sin datos', 'normal', 'fa-question-circle', "Esperando datos de ritmo cardíaco"),
        'temp': medical_condition('Sin datos', 'normal', 'fa-question-circle', "Esperando datos de temperatura"),
        'messages': ['Esperando datos del sensor...'],
        'severity': 'normal',
        'timestamp': datetime.now().isoformat()
    }

def generate_error_diagnosis(error_msg):
    return {
        'spo2': medical_condition('Error', 'critical', 'fa-exclamation-triangle', "Error en lectura de SpO2"),
        'bpm': medical_condition('Error', 'critical', 'fa-exclamation-triangle', "Error en lectura de ritmo cardíaco"),
        'temp': medical_condition('Error', 'critical', 'fa-exclamation-triangle', "Error en lectura de temperatura"),
        'messages': [f'Error del sistema: {error_msg}'],
        'severity': 'critical',
        'timestamp': datetime.now().isoformat()
    }