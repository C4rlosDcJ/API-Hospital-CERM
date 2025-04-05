from app import db
from datetime import datetime

class Oximetro(db.Model):
    __tablename__ = 'oximetro'
    
    id = db.Column(db.Integer, primary_key=True)
    dc_red = db.Column(db.Float, nullable=False)
    dc_ir = db.Column(db.Float, nullable=False)
    spo2 = db.Column(db.Float, nullable=False)
    bpm = db.Column(db.Integer, nullable=False)
    temp = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.BigInteger, nullable=False)
    raw_red = db.Column(db.Float, nullable=False)
    raw_ir = db.Column(db.Float, nullable=False)
    received_at = db.Column(db.DateTime, default=datetime.utcnow)

    MEDICAL_RANGES = {
        'spo2': {'normal': (95, 100), 'hypoxia': (90, 94), 'severe_hypoxia': (0, 89)},
        'bpm': {'normal': (60, 100), 'bradycardia': (40, 59), 'tachycardia': (101, 140)},
        'temp': {'normal': (36.0, 37.5), 'hypothermia': (0, 35.9), 
                'fever': (37.6, 39.9), 'hyperpyrexia': (40.0, 45.0)}
    }

    def generate_diagnosis(self):
        return {
            'spo2': self._analyze_metric('spo2', self.spo2, '%'),
            'bpm': self._analyze_metric('bpm', self.bpm, 'bpm'),
            'temp': self._analyze_metric('temp', self.temp, '°C'),
            'timestamp': self.received_at.isoformat()
        }

    def _analyze_metric(self, metric, value, unit):
        # Validación de valores de métricas
        if value is None or value < 0:
            return {
                'value': value,
                'status': 'Invalid',
                'severity': 'critical',
                'unit': unit,
                'normal_range': 'N/A'
            }

        ranges = self.MEDICAL_RANGES[metric]
        status = 'Normal'
        severity = 'normal'
        
        if metric == 'spo2':
            if value >= ranges['normal'][0]:
                status = 'Normal'
            elif value >= ranges['hypoxia'][0]:
                status = 'Hipoxia leve'
                severity = 'warning'
            else:
                status = 'Hipoxia severa'
                severity = 'critical'
                
        elif metric == 'bpm':
            if ranges['normal'][0] <= value <= ranges['normal'][1]:
                status = 'Normal'
            elif ranges['bradycardia'][0] <= value <= ranges['bradycardia'][1]:
                status = 'Bradicardia'
                severity = 'warning'
            elif ranges['tachycardia'][0] <= value <= ranges['tachycardia'][1]:
                status = 'Taquicardia'
                severity = 'warning'
            else:
                status = 'Arritmia'
                severity = 'critical'
                
        elif metric == 'temp':
            if ranges['normal'][0] <= value <= ranges['normal'][1]:
                status = 'Normal'
            elif value <= ranges['hypothermia'][1]:
                status = 'Hipotermia'
                severity = 'critical'
            elif ranges['fever'][0] <= value <= ranges['fever'][1]:
                status = 'Fiebre'
                severity = 'warning'
            elif value >= ranges['hyperpyrexia'][0]:
                status = 'Hipertermia'
                severity = 'critical'

        return {
            'value': value,
            'status': status,
            'severity': severity,
            'unit': unit,
            'normal_range': ranges[status]
        }
        
    def to_dict(self):
        return {
            'id': self.id,
            'spo2': self.spo2,
            'bpm': self.bpm,
            'temp': self.temp,
            'timestamp': self.timestamp,
            'received_at': self.received_at.isoformat() if self.received_at else None,
            'diagnosis': self.generate_diagnosis()
        }
