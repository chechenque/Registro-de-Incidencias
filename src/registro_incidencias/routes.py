from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user, login_required, login_user, logout_user
from sqlalchemy import select

from registro_incidencias.extensions import db
from registro_incidencias.forms import LoginForm, RegistroForm
from registro_incidencias.models import Usuario

main = Blueprint("main", __name__)


@main.get("/")
def index():
    return render_template("index.html")


@main.route("/registro", methods=["GET", "POST"])
def registro():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    form = RegistroForm()

    if form.validate_on_submit():
        correo = form.correo.data.strip().lower()

        usuario_existente = db.session.scalar(
            select(Usuario).where(Usuario.correo == correo)
        )

        if usuario_existente is not None:
            flash("Ya existe una cuenta con ese correo electrónico.", "error")
            return render_template("registro.html", form=form), 409

        usuario = Usuario(
            nombre=form.nombre.data.strip(),
            correo=correo,
            rol="reportante",
        )
        usuario.establecer_password(form.password.data)

        db.session.add(usuario)
        db.session.commit()

        flash("Tu cuenta se creó correctamente. Ya puedes iniciar sesión.", "success")
        return redirect(url_for("main.login"))

    return render_template("registro.html", form=form)


@main.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    form = LoginForm()

    if form.validate_on_submit():
        correo = form.correo.data.strip().lower()

        usuario = db.session.scalar(
            select(Usuario).where(Usuario.correo == correo)
        )

        if usuario is None or not usuario.verificar_password(form.password.data):
            flash("Correo o contraseña incorrectos.", "error")
            return render_template("login.html", form=form), 401

        login_user(usuario)
        flash("Has iniciado sesión correctamente.", "success")
        return redirect(url_for("main.index"))

    return render_template("login.html", form=form)


@main.post("/logout")
@login_required
def logout():
    logout_user()
    flash("Has cerrado sesión.", "success")
    return redirect(url_for("main.index"))