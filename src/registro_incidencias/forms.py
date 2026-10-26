from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import (
    DataRequired,
    Email,
    EqualTo,
    Length,
)


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