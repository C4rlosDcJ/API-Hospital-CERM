from app import db

class Cita(db.Model):
    __tablename__ = 'citas'

    id = db.Column(db.Integer, primary_key=True)
    paciente_id = db.Column(db.Integer, db.ForeignKey('pacientes.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctores.id'), nullable=False)
    fecha_hora = db.Column(db.DateTime, nullable=False)
    estatus = db.Column(db.String(50), default='En proceso')
    descripcion = db.Column(db.String(500))
    codigo = db.Column(db.String(25))
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
    updated_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    # Relación con la tabla Paciente
    paciente = db.relationship('Paciente', backref='citas')
    # Relación con la tabla Doctor
    doctor = db.relationship('Doctor', backref='citas', lazy=True)

    def __repr__(self):
        return f'<Cita {self.id}>'

    def to_dict(self):
        # Devuelve un diccionario con los atributos de la cita
        return {
            'id': self.id,
            'paciente_id': self.paciente_id,
            'doctor_id': self.doctor_id,
            'fecha_hora': self.fecha_hora.isoformat(),  # Si deseas un formato de fecha específico
            'estatus': self.estatus,
            'descripcion': self.descripcion,
            'codigo': self.codigo,
            'created_at': self.created_at.isoformat(), 
            'updated_at': self.updated_at.isoformat(),  
            'paciente': self.paciente.nombre if self.paciente else None,  
            'doctor': self.doctor.nombre if self.doctor else None  
        }
