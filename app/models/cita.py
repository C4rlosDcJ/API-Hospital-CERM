from app import db

class Cita(db.Model):
    __tablename__ = 'citas'

    id = db.Column(db.Integer, primary_key=True)
    paciente_id = db.Column(db.Integer, db.ForeignKey('pacientes.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctores.id'), nullable=False)
    oximetro_id = db.Column(db.Integer, db.ForeignKey('oximetro.id'), nullable=False)
    fecha_hora = db.Column(db.DateTime, nullable=False)
    estatus = db.Column(db.Enum('programada', 'en_proceso', 'completada', 'cancelada'), default='programada')
    diagnostico = db.Column(db.String(500))
    codigo = db.Column(db.String(25))
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
    updated_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    paciente = db.relationship('Paciente', backref='citas')
    doctor = db.relationship('Doctor', backref='citas')
    oximetro = db.relationship(
        'Oximetro', 
        backref='cita', 
        uselist=False,  # Relación uno-a-uno
        lazy=True
    )

    def __repr__(self):
        return f'<Cita {self.id}>'

    def to_dict(self):
        oximetro_data = None
        if self.oximetro:
            oximetro_data = {
                'spo2': self.oximetro.spo2,
                'bpm': self.oximetro.bpm,
                'temp': self.oximetro.temp
            }
        return {
            'id': self.id,
            'paciente_id': self.paciente_id,
            'doctor_id': self.doctor_id,
            'fecha_hora': self.fecha_hora.isoformat() if self.fecha_hora else None,
            'estatus': self.estatus,
            'diagnostico': self.diagnostico,
            'codigo': self.codigo,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'paciente': self.paciente.nombre if self.paciente else None,
            'doctor': self.doctor.nombre if self.doctor else None,
            'oximetro': oximetro_data,
            'diagnosis': self._get_oximetro_diagnosis()
        }

    def _get_oximetro_diagnosis(self):
        if self.oximetro:
            return {
                'bpm': self.oximetro._analyze_bpm() if hasattr(self.oximetro, '_analyze_bpm') else None,
                'spo2': self.oximetro._analyze_spo2() if hasattr(self.oximetro, '_analyze_spo2') else None,
                'temp': self.oximetro._analyze_temp() if hasattr(self.oximetro, '_analyze_temp') else None,
            }
        return None
