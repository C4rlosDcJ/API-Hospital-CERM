from .user_controller import (
    get_users, get_user, create_user, update_user, delete_user
)
from .brazo_robotico_controller import (
    get_brazos_roboticos, get_brazo_robotico, create_brazo_robotico, 
    update_brazo_robotico, delete_brazo_robotico
)
from .paciente_controller import (
    get_pacientes, get_paciente, create_paciente, 
    update_paciente, delete_paciente
)
from .doctor_controller import (
    get_doctores, get_doctor, create_doctor, 
    update_doctor, delete_doctor
)
from .sensor_controller import (
    get_sensores, get_sensor, create_sensor, 
    update_sensor, delete_sensor
)
from .operacion_controller import (
    get_operaciones, get_operacion, create_operacion, 
    update_operacion, delete_operacion
)
from .registro_sensor_controller import (
    get_registros_sensores, get_registro_sensor, 
    create_registro_sensor, update_registro_sensor, delete_registro_sensor
)
from .historial_inyeccion_controller import (
    get_historial_inyecciones, get_historial_inyeccion, 
    create_historial_inyeccion, update_historial_inyeccion, delete_historial_inyeccion
)
from .cita_controller import (
    get_citas, get_cita, create_cita, update_cita, delete_cita, search_citas
)
from.registro_sensor_oximetro import(
    SensorOximetroController
)