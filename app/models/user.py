from app import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum('admin', 'doctor', 'paciente'), default='paciente')
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
    updated_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    # Relaciones
    pacientes = db.relationship('Paciente', backref='user', lazy=True)
    doctores = db.relationship('Doctor', backref='user', lazy=True)
    brazos_roboticos = db.relationship('BrazoRobotico', backref='user', lazy=True)

    def __repr__(self):
        return f'<User {self.name}>'

    def to_dict(self):
        # Devuelve un diccionario con los atributos del objeto User
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'role': self.role,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
