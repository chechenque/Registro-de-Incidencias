from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import (
    DataRequired,
    Email,
    EqualTo,
    Length,
)
from wtforms import SelectField, TextAreaField
from wtforms.validators import Length
from wtforms.fields import SelectChoice


class RegistroForm(FlaskForm):
    nombre = StringField(
        "Nombre completo",
        validators=[DataRequired(), Length(min=2, max=120)],
    )
    correo = StringField(
        "Correo electrónico",
        validators=[DataRequired(), Email(), Length(max=255)],
    )
    password = PasswordField(
        "Contraseña",
        validators=[DataRequired(), Length(min=12, max=128)],
    )
    confirmar_password = PasswordField(
        "Confirmar contraseña",
        validators=[
            DataRequired(),
            EqualTo("password", message="Las contraseñas no coinciden."),
        ],
    )
    submit = SubmitField("Crear cuenta")


class LoginForm(FlaskForm):
    correo = StringField(
        "Correo electrónico",
        validators=[DataRequired(), Email(), Length(max=255)],
    )
    password = PasswordField(
        "Contraseña",
        validators=[DataRequired(), Length(min=12, max=128)],
    )
    submit = SubmitField("Iniciar sesión")


class IncidenciaForm(FlaskForm):
    titulo = StringField(
        "Título",
        validators=[
            DataRequired(),
            Length(min=5, max=160),
        ],
    )
    descripcion = TextAreaField(
        "Descripción",
        validators=[
            DataRequired(),
            Length(min=10, max=5000),
        ],
    )
    prioridad = SelectField(
        "Prioridad",
        choices=[
            SelectChoice("baja", "Baja"),
            SelectChoice("media", "Media"),
            SelectChoice("alta", "Alta"),
            SelectChoice("critica", "Crítica"),
        ],
        default="media",
        validators=[DataRequired()],
    )
    submit = SubmitField("Registrar incidencia")


class ComentarioForm(FlaskForm):
    contenido = TextAreaField(
        "Comentario",
        validators=[
            DataRequired(),
            Length(min=2, max=3000),
        ],
    )
    submit = SubmitField("Agregar comentario")


class EstadoIncidenciaForm(FlaskForm):
    estado = SelectField(
        "Estado",
        choices=[
            SelectChoice("abierta", "Abierta"),
            SelectChoice("en_proceso", "En proceso"),
            SelectChoice("resuelta", "Resuelta"),
            SelectChoice("cerrada", "Cerrada"),
        ],
        validators=[DataRequired()],
    )
    submit = SubmitField("Actualizar estado")