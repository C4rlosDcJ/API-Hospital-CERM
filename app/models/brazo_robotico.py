from app import db

class BrazoRobotico(db.Model):
    __tablename__ = 'brazos_roboticos'

    id = db.Column(db.Integer, primary_key=True)
    modelo = db.Column(db.String(255), nullable=False)
    fabricante = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
    updated_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    # Relaciones
    sensores = db.relationship('Sensor', backref='brazo_robotico', lazy=True)
    operaciones = db.relationship('Operacion', backref='brazo_robotico', lazy=True)

    def __repr__(self):
        return f'<BrazoRobotico {self.modelo}>'

    def to_dict(self):
        return {
            'id': self.id,
            'modelo': self.modelo,
            'fabricante': self.fabricante,
            'user_id': self.user_id,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'sensores': [sensor.to_dict() for sensor in self.sensores],  
            'operaciones': [operacion.to_dict() for operacion in self.operaciones], 
        }
