from app import db

class Sensor(db.Model):
    __tablename__ = 'sensores'

    id = db.Column(db.Integer, primary_key=True)
    brazo_robotico_id = db.Column(db.Integer, db.ForeignKey('brazos_roboticos.id'), nullable=False)
    tipo = db.Column(db.String(255), nullable=False)
    unidad_medida = db.Column(db.String(50))
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
    updated_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    # Relaciones
    registros_sensores = db.relationship('RegistroSensor', backref='sensor', lazy=True)

    def __repr__(self):
        return f'<Sensor {self.tipo}>'

    def to_dict(self):
        return {
            'id': self.id,
            'brazo_robotico_id': self.brazo_robotico_id,
            'tipo': self.tipo,
            'unidad_medida': self.unidad_medida,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'registros_sensores': [registro.to_dict() for registro in self.registros_sensores]  # Si RegistroSensor tiene un método to_dict()
        }
