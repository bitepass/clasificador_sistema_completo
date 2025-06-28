from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import Index

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255))
    rol = db.Column(db.String(50), default='USUARIO')
    activo = db.Column(db.Boolean, default=True)
    ultimo_acceso = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    planillas = db.relationship('Planilla', backref='usuario', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'rol': self.rol,
            'activo': self.activo,
            'ultimo_acceso': self.ultimo_acceso.isoformat() if self.ultimo_acceso else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Planilla(db.Model):
    __tablename__ = 'planillas'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre_archivo = db.Column(db.String(255), nullable=False)
    fecha_subida = db.Column(db.DateTime, default=datetime.utcnow)
    usuario_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    partido = db.Column(db.String(100))
    fecha_inicio = db.Column(db.Date)
    fecha_fin = db.Column(db.Date)
    total_registros = db.Column(db.Integer, default=0)
    registros_procesados = db.Column(db.Integer, default=0)
    estado = db.Column(db.String(50), default='PROCESANDO')  # PROCESANDO, COMPLETADO, CANCELADO, ERROR
    archivo_resultado = db.Column(db.String(255))
    observaciones = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    hechos_delictivos = db.relationship('HechoDelictivo', backref='planilla', lazy=True, cascade='all, delete-orphan')
    logs = db.relationship('LogProcesamiento', backref='planilla', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Planilla {self.nombre_archivo}>'

    def to_dict(self):
        return {
            'id': self.id,
            'nombre_archivo': self.nombre_archivo,
            'fecha_subida': self.fecha_subida.isoformat() if self.fecha_subida else None,
            'usuario_id': self.usuario_id,
            'partido': self.partido,
            'fecha_inicio': self.fecha_inicio.isoformat() if self.fecha_inicio else None,
            'fecha_fin': self.fecha_fin.isoformat() if self.fecha_fin else None,
            'total_registros': self.total_registros,
            'registros_procesados': self.registros_procesados,
            'estado': self.estado,
            'archivo_resultado': self.archivo_resultado,
            'observaciones': self.observaciones,
            'progreso': (self.registros_procesados / self.total_registros * 100) if self.total_registros > 0 else 0
        }

class HechoDelictivo(db.Model):
    __tablename__ = 'hechos_delictivos'
    
    id = db.Column(db.Integer, primary_key=True)
    planilla_id = db.Column(db.Integer, db.ForeignKey('planillas.id'), nullable=False)
    
    # Datos originales del Excel
    id_hecho = db.Column(db.String(50))
    nro_registro = db.Column(db.String(50))
    ipp = db.Column(db.String(100))
    fecha_carga = db.Column(db.Date)
    fecha_hecho = db.Column(db.Date)
    hora_hecho = db.Column(db.Time)
    comisaria = db.Column(db.String(100))
    dependencia = db.Column(db.String(100))
    localidad = db.Column(db.String(100))
    barrio = db.Column(db.String(100))
    direccion = db.Column(db.Text)
    latitud = db.Column(db.Numeric(10, 8))
    longitud = db.Column(db.Numeric(11, 8))
    relato = db.Column(db.Text)
    
    # Clasificaciones automáticas
    jurisdiccion = db.Column(db.String(50))  # URBANA, RURAL, MIXTA, OTROS
    calificacion = db.Column(db.String(100))  # HOMICIDIO_SIMPLE, FEMICIDIO, etc.
    modalidad = db.Column(db.String(100))
    victimas = db.Column(db.String(50))  # FEMENINO, MASCULINO, AMBOS, OTROS
    lesionado = db.Column(db.String(10))  # SI, NO, OTROS
    imputados = db.Column(db.String(50))  # FEMENINO, MASCULINO, AMBOS, OTROS
    edad = db.Column(db.String(50))  # MAYOR, MENOR, AMBOS, OTROS
    armas = db.Column(db.String(50))  # FUEGO, BLANCA, IMPROPIA, NINGUNA, OTROS
    lugar = db.Column(db.String(100))  # FINCA, VIA_PUBLICA, COMERCIO, etc.
    tentativa = db.Column(db.String(10))  # SI, NO, OTROS
    observaciones = db.Column(db.Text)
    
    # Metadatos de procesamiento
    metodo_clasificacion = db.Column(db.String(50))  # GEMINI, OPENAI, REGLAS, DEFECTO
    confianza_clasificacion = db.Column(db.Numeric(3, 2))  # 0.00 a 1.00
    tiempo_procesamiento = db.Column(db.Integer)  # milisegundos
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    personas_involucradas = db.relationship('PersonaInvolucrada', backref='hecho', lazy=True, cascade='all, delete-orphan')
    logs = db.relationship('LogProcesamiento', backref='hecho', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<HechoDelictivo {self.id_hecho}>'

    def to_dict(self):
        return {
            'id': self.id,
            'planilla_id': self.planilla_id,
            'id_hecho': self.id_hecho,
            'nro_registro': self.nro_registro,
            'ipp': self.ipp,
            'fecha_carga': self.fecha_carga.isoformat() if self.fecha_carga else None,
            'fecha_hecho': self.fecha_hecho.isoformat() if self.fecha_hecho else None,
            'hora_hecho': self.hora_hecho.isoformat() if self.hora_hecho else None,
            'comisaria': self.comisaria,
            'dependencia': self.dependencia,
            'localidad': self.localidad,
            'barrio': self.barrio,
            'direccion': self.direccion,
            'latitud': float(self.latitud) if self.latitud else None,
            'longitud': float(self.longitud) if self.longitud else None,
            'relato': self.relato,
            'jurisdiccion': self.jurisdiccion,
            'calificacion': self.calificacion,
            'modalidad': self.modalidad,
            'victimas': self.victimas,
            'lesionado': self.lesionado,
            'imputados': self.imputados,
            'edad': self.edad,
            'armas': self.armas,
            'lugar': self.lugar,
            'tentativa': self.tentativa,
            'observaciones': self.observaciones,
            'metodo_clasificacion': self.metodo_clasificacion,
            'confianza_clasificacion': float(self.confianza_clasificacion) if self.confianza_clasificacion else None,
            'tiempo_procesamiento': self.tiempo_procesamiento
        }

class PersonaInvolucrada(db.Model):
    __tablename__ = 'personas_involucradas'
    
    id = db.Column(db.Integer, primary_key=True)
    hecho_id = db.Column(db.Integer, db.ForeignKey('hechos_delictivos.id'), nullable=False)
    
    # Tipo de involucrado
    tipo = db.Column(db.String(50), nullable=False)  # VICTIMA, IMPUTADO, TESTIGO, OTROS
    
    # Datos personales
    nombre = db.Column(db.String(200))
    apellido = db.Column(db.String(200))
    dni = db.Column(db.String(20))
    edad = db.Column(db.Integer)
    genero = db.Column(db.String(20))  # MASCULINO, FEMENINO, OTROS
    nacionalidad = db.Column(db.String(100))
    
    # Datos adicionales
    estado_civil = db.Column(db.String(50))
    ocupacion = db.Column(db.String(100))
    domicilio = db.Column(db.Text)
    telefono = db.Column(db.String(50))
    
    # Información específica del caso
    lesiones = db.Column(db.String(10))  # SI, NO
    tipo_lesiones = db.Column(db.Text)
    arma_utilizada = db.Column(db.String(50))
    rol_en_hecho = db.Column(db.Text)
    observaciones = db.Column(db.Text)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<PersonaInvolucrada {self.nombre} {self.apellido}>'

    def to_dict(self):
        return {
            'id': self.id,
            'hecho_id': self.hecho_id,
            'tipo': self.tipo,
            'nombre': self.nombre,
            'apellido': self.apellido,
            'dni': self.dni,
            'edad': self.edad,
            'genero': self.genero,
            'nacionalidad': self.nacionalidad,
            'estado_civil': self.estado_civil,
            'ocupacion': self.ocupacion,
            'domicilio': self.domicilio,
            'telefono': self.telefono,
            'lesiones': self.lesiones,
            'tipo_lesiones': self.tipo_lesiones,
            'arma_utilizada': self.arma_utilizada,
            'rol_en_hecho': self.rol_en_hecho,
            'observaciones': self.observaciones
        }

class Configuracion(db.Model):
    __tablename__ = 'configuraciones'
    
    id = db.Column(db.Integer, primary_key=True)
    clave = db.Column(db.String(100), unique=True, nullable=False)
    valor = db.Column(db.Text)
    descripcion = db.Column(db.Text)
    tipo = db.Column(db.String(50), default='STRING')  # STRING, INTEGER, BOOLEAN, JSON
    categoria = db.Column(db.String(50), default='GENERAL')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Configuracion {self.clave}>'

    def to_dict(self):
        return {
            'id': self.id,
            'clave': self.clave,
            'valor': self.valor,
            'descripcion': self.descripcion,
            'tipo': self.tipo,
            'categoria': self.categoria
        }

class LogProcesamiento(db.Model):
    __tablename__ = 'logs_procesamiento'
    
    id = db.Column(db.Integer, primary_key=True)
    planilla_id = db.Column(db.Integer, db.ForeignKey('planillas.id'))
    hecho_id = db.Column(db.Integer, db.ForeignKey('hechos_delictivos.id'))
    nivel = db.Column(db.String(20))  # INFO, WARNING, ERROR, DEBUG
    mensaje = db.Column(db.Text)
    detalle_error = db.Column(db.Text)
    metodo = db.Column(db.String(50))  # GEMINI, OPENAI, REGLAS
    tiempo_ejecucion = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<LogProcesamiento {self.nivel}: {self.mensaje[:50]}>'

    def to_dict(self):
        return {
            'id': self.id,
            'planilla_id': self.planilla_id,
            'hecho_id': self.hecho_id,
            'nivel': self.nivel,
            'mensaje': self.mensaje,
            'detalle_error': self.detalle_error,
            'metodo': self.metodo,
            'tiempo_ejecucion': self.tiempo_ejecucion,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

# Índices para optimización
Index('idx_hechos_planilla', HechoDelictivo.planilla_id)
Index('idx_hechos_fecha', HechoDelictivo.fecha_hecho)
Index('idx_hechos_calificacion', HechoDelictivo.calificacion)
Index('idx_hechos_localidad', HechoDelictivo.localidad)
Index('idx_hechos_coordenadas', HechoDelictivo.latitud, HechoDelictivo.longitud)

Index('idx_personas_hecho', PersonaInvolucrada.hecho_id)
Index('idx_personas_tipo', PersonaInvolucrada.tipo)

Index('idx_planillas_fecha', Planilla.fecha_subida)
Index('idx_planillas_partido', Planilla.partido)

Index('idx_logs_planilla', LogProcesamiento.planilla_id)
Index('idx_logs_nivel', LogProcesamiento.nivel)

