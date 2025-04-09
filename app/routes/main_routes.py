from flask import Blueprint
from flask import request, jsonify
from app.controllers.registro_sensor_oximetro import SensorOximetroController


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




# Sensor Oximetro
@main_routes.route('/data', methods=['POST'])
def create_data():
    return SensorOximetroController.create_sensor_data()

@main_routes.route('/data', methods=['GET'])
def get_data():
    return SensorOximetroController.get_sensor_data()

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