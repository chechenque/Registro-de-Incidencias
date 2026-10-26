from datetime import datetime, timezone

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from registro_incidencias.extensions import db


class Usuario(UserMixin, db.Model):
    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120), nullable=False)
    correo = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    rol = db.Column(db.String(20), nullable=False, default="reportante")

    incidencias = db.relationship(
        "Incidencia",
        back_populates="reportante",
        lazy="select",
    )
    comentarios = db.relationship(
        "Comentario",
        back_populates="autor",
        lazy="select",
    )

    def establecer_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def verificar_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def es_administrador(self) -> bool:
        return self.rol == "administrador"


class Incidencia(db.Model):
    __tablename__ = "incidencias"

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(160), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    estado = db.Column(db.String(30), nullable=False, default="abierta")
    prioridad = db.Column(db.String(20), nullable=False, default="media")
    fecha_creacion = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )
    fecha_actualizacion = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    reportante_id = db.Column(
        db.Integer,
        db.ForeignKey("usuarios.id"),
        nullable=False,
        index=True,
    )

    reportante = db.relationship(
        "Usuario",
        back_populates="incidencias",
    )
    comentarios = db.relationship(
        "Comentario",
        back_populates="incidencia",
        cascade="all, delete-orphan",
        order_by="Comentario.fecha_creacion",
        lazy="select",
    )


class Comentario(db.Model):
    __tablename__ = "comentarios"

    id = db.Column(db.Integer, primary_key=True)
    contenido = db.Column(db.Text, nullable=False)
    fecha_creacion = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    incidencia_id = db.Column(
        db.Integer,
        db.ForeignKey("incidencias.id"),
        nullable=False,
        index=True,
    )
    autor_id = db.Column(
        db.Integer,
        db.ForeignKey("usuarios.id"),
        nullable=False,
        index=True,
    )

    incidencia = db.relationship(
        "Incidencia",
        back_populates="comentarios",
    )
    autor = db.relationship(
        "Usuario",
        back_populates="comentarios",
    )