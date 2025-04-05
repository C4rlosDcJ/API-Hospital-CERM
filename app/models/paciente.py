from app import db

class Paciente(db.Model):
    __tablename__ = 'pacientes'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    nombre = db.Column(db.String(255), nullable=False)
    edad = db.Column(db.Integer)
    grupo_sanguineo = db.Column(db.Enum('A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-'))  # Corregido de db.emun a db.Enum
    historial_medico = db.Column(db.Text)
    contacto_emergencia = db.Column(db.String(255))
    peso = db.Column(db.Float)
    altura = db.Column(db.Float)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
    updated_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    operaciones = db.relationship('Operacion', backref='paciente', lazy=True)
    historial_inyecciones = db.relationship('HistorialInyeccion', backref='paciente', lazy=True)

    def __repr__(self):
        return f'<Paciente {self.nombre}>'

    def to_dict(self):
        operaciones_data = [operacion.to_dict() for operacion in self.operaciones] if self.operaciones else []
        inyecciones_data = [inyeccion.to_dict() for inyeccion in self.historial_inyecciones] if self.historial_inyecciones else []
        
        return {
            'id': self.id,
            'user_id': self.user_id,
            'nombre': self.nombre,
            'edad': self.edad,
            'historial_medico': self.historial_medico,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'operaciones': operaciones_data,
            'historial_inyecciones': inyecciones_data,
            'contacto_emergencia': self.contacto_emergencia,
            'peso': self.peso,
            'altura': self.altura,
            'grupo_sanguineo': self.grupo_sanguineo,
        }
