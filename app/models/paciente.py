from app import db

class Paciente(db.Model):
    __tablename__ = 'pacientes'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    nombre = db.Column(db.String(255), nullable=False)
    edad = db.Column(db.Integer)
    historial_medico = db.Column(db.Text)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
    updated_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    # Relaciones
    # citas = db.relationship('Cita', backref='paciente', lazy=True)
    operaciones = db.relationship('Operacion', backref='paciente', lazy=True)
    historial_inyecciones = db.relationship('HistorialInyeccion', backref='paciente', lazy=True)

    def __repr__(self):
        return f'<Paciente {self.nombre}>'

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'nombre': self.nombre,
            'edad': self.edad,
            'historial_medico': self.historial_medico,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'operaciones': [operacion.to_dict() for operacion in self.operaciones],
            'historial_inyecciones': [inyeccion.to_dict() for inyeccion in self.historial_inyecciones]
        }
