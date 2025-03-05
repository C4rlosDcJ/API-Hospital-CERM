from app import db

class Operacion(db.Model):
    __tablename__ = 'operaciones'

    id = db.Column(db.Integer, primary_key=True)
    brazo_robotico_id = db.Column(db.Integer, db.ForeignKey('brazos_roboticos.id'), nullable=False)
    paciente_id = db.Column(db.Integer, db.ForeignKey('pacientes.id'), nullable=False)
    tipo = db.Column(db.Enum('inyeccion', 'cirugia', 'monitoreo'), default='inyeccion')
    estado = db.Column(db.Enum('pendiente', 'completada', 'fallida'), default='pendiente')
    fecha_hora = db.Column(db.DateTime, nullable=False)
    observaciones = db.Column(db.Text)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
    updated_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    # Relaciones
    historial_inyecciones = db.relationship('HistorialInyeccion', backref='operacion', lazy=True)

    def __repr__(self):
        return f'<Operacion {self.tipo}>'

    def to_dict(self):
        return {
            'id': self.id,
            'brazo_robotico_id': self.brazo_robotico_id,
            'paciente_id': self.paciente_id,
            'tipo': self.tipo,
            'estado': self.estado,
            'fecha_hora': self.fecha_hora,
            'observaciones': self.observaciones,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'historial_inyecciones': [historial.to_dict() for historial in self.historial_inyecciones]
        }
