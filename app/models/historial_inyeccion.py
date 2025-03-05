from app import db

class HistorialInyeccion(db.Model):
    __tablename__ = 'historial_inyecciones'

    id = db.Column(db.Integer, primary_key=True)
    paciente_id = db.Column(db.Integer, db.ForeignKey('pacientes.id'), nullable=False)
    operacion_id = db.Column(db.Integer, db.ForeignKey('operaciones.id'), nullable=False)
    observaciones = db.Column(db.Text)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
    updated_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def __repr__(self):
        return f'<HistorialInyeccion {self.id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'paciente_id': self.paciente_id,
            'operacion_id': self.operacion_id,
            'observaciones': self.observaciones,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
