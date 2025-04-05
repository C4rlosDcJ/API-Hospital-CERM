from flask import jsonify, request
from app.models.oximetro import Oximetro
from app import db

class SensorOximetroController:
    @staticmethod
    def create_sensor_data():
        try:
            data = request.get_json()  # Recibir datos como JSON
            
            # Validación mejorada
            required_fields = {
                'red': (float, "Valor RED inválido"),
                'ir': (float, "Valor IR inválido"),
                'spo2': (float, "SpO2 inválido"),
                'bpm': (int, "BPM inválido"),
                'temp': (float, "Temperatura inválida"),
                't': (int, "Timestamp inválido")
            }
            
            for field, (type_, error_msg) in required_fields.items():
                if field not in data:
                    raise ValueError(f"Campo requerido faltante: {field}")
                try:
                    data[field] = type_(data[field])
                except (ValueError, TypeError):
                    raise ValueError(error_msg)

            # Crear registro con validación médica
            if not (0 <= data['spo2'] <= 100):
                raise ValueError("SpO2 fuera de rango (0-100%)")
                
            if not (30 <= data['bpm'] <= 200):
                raise ValueError("BPM fuera de rango (30-200)")

            sensor_data = Oximetro(
                dc_red=data['red'],
                dc_ir=data['ir'],
                spo2=data['spo2'],
                bpm=data['bpm'],
                temp=data['temp'],
                timestamp=data['t'],
                raw_red=data['red'],
                raw_ir=data['ir']
            )

            db.session.add(sensor_data)
            db.session.commit()

            return jsonify({
                'status': 'success',
                'message': 'Datos almacenados',
                'id': sensor_data.id
            }), 201

        except Exception as e:
            db.session.rollback()
            return jsonify({
                'status': 'error',
                'message': str(e)
            }), 400

    @staticmethod
    def get_sensor_data():
        try:
            latest_data = Oximetro.query.order_by(
                Oximetro.timestamp.desc()
            ).limit(10).all()
            
            if not latest_data:
                return jsonify({
                    'status': 'error',
                    'message': 'No se encontraron datos'
                }), 404
            
            response = {
                'status': 'success',
                'data': [{
                    'id': d.id,
                    'spo2': d.spo2,
                    'bpm': d.bpm,
                    'temp': d.temp,
                    'timestamp': d.timestamp,
                    'received_at': d.received_at.isoformat() if d.received_at else None
                } for d in latest_data]
            }
            
            # Solo incluir el diagnóstico si hay datos
            if latest_data and hasattr(latest_data[0], 'generate_diagnosis'):
                response['diagnosis'] = latest_data[0].generate_diagnosis()
            
            return jsonify(response), 200

        except Exception as e:
            return jsonify({
                'status': 'error',
                'message': str(e)
            }), 500

    @staticmethod
    def get_all_sensor_data():
        try:
            all_data = Oximetro.query.order_by(Oximetro.timestamp.desc()).all()
            
            if not all_data:
                return jsonify({
                    'status': 'error',
                    'message': 'No se encontraron datos'
                }), 404
            
            return jsonify({
                'status': 'success',
                'data': [{
                    'id': d.id,
                    'spo2': d.spo2,
                    'bpm': d.bpm,
                    'temp': d.temp,
                    'timestamp': d.timestamp,
                    'received_at': d.received_at.isoformat() if d.received_at else None
                } for d in all_data]
            }), 200

        except Exception as e:
            return jsonify({
                'status': 'error',
                'message': str(e)
            }), 500
