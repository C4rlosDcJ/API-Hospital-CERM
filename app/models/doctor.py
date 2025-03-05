from app import db

class Doctor(db.Model):
    __tablename__ = 'doctores'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    nombre = db.Column(db.String(255), nullable=False)
    especialidad = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
    updated_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def __repr__(self):
        return f'<Doctor {self.nombre}>'

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'nombre': self.nombre,
            'especialidad': self.especialidad,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
