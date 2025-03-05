from app import db

class RegistroSensor(db.Model):
    __tablename__ = 'registros_sensores'

    id = db.Column(db.Integer, primary_key=True)
    sensor_id = db.Column(db.Integer, db.ForeignKey('sensores.id'), nullable=False)
    valor = db.Column(db.String(255), nullable=False)
    fecha_hora = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
    updated_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def __repr__(self):
        return f'<RegistroSensor {self.valor}>'

    def to_dict(self):
        return {
            'id': self.id,
            'sensor_id': self.sensor_id,
            'valor': self.valor,
            'fecha_hora': self.fecha_hora,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
