from flask import (
    Blueprint,
    abort,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import (
    current_user,
    login_required,
    login_user,
    logout_user,
)
from sqlalchemy import select

from registro_incidencias.extensions import db
from registro_incidencias.forms import (
    ComentarioForm,
    EstadoIncidenciaForm,
    IncidenciaForm,
    LoginForm,
    RegistroForm,
)
from registro_incidencias.models import Comentario, Incidencia, Usuario

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


@main.get("/incidencias")
@login_required
def listar_incidencias():
    consulta = select(Incidencia).order_by(
        Incidencia.fecha_actualizacion.desc()
    )

    if not current_user.es_administrador():
        consulta = consulta.where(
            Incidencia.reportante_id == current_user.id
        )

    incidencias = db.session.scalars(consulta).all()

    return render_template(
        "incidencias.html",
        incidencias=incidencias,
    )


@main.route("/incidencias/nueva", methods=["GET", "POST"])
@login_required
def nueva_incidencia():
    form = IncidenciaForm()

    if form.validate_on_submit():
        incidencia = Incidencia(
            titulo=form.titulo.data.strip(),
            descripcion=form.descripcion.data.strip(),
            prioridad=form.prioridad.data,
            estado="abierta",
            reportante_id=current_user.id,
        )

        db.session.add(incidencia)
        db.session.commit()

        flash("La incidencia se registró correctamente.", "success")
        return redirect(
            url_for("main.detalle_incidencia", incidencia_id=incidencia.id)
        )

    return render_template("incidencia_nueva.html", form=form)


def obtener_incidencia_autorizada(incidencia_id: int) -> Incidencia:
    incidencia = db.session.get(Incidencia, incidencia_id)

    if incidencia is None:
        abort(404)

    if (
        not current_user.es_administrador()
        and incidencia.reportante_id != current_user.id
    ):
        abort(403)

    return incidencia


@main.route("/incidencias/<int:incidencia_id>", methods=["GET", "POST"])
@login_required
def detalle_incidencia(incidencia_id: int):
    incidencia = obtener_incidencia_autorizada(incidencia_id)

    comentario_form = ComentarioForm()
    estado_form = EstadoIncidenciaForm()

    if request.method == "POST":
        if request.form.get("accion") != "comentario":
            abort(400)

        if comentario_form.validate_on_submit():
            comentario = Comentario(
                contenido=comentario_form.contenido.data.strip(),
                incidencia_id=incidencia.id,
                autor_id=current_user.id,
            )

            db.session.add(comentario)
            db.session.commit()

            flash("El comentario se agregó correctamente.", "success")
            return redirect(
                url_for(
                    "main.detalle_incidencia",
                    incidencia_id=incidencia.id,
                )
            )

    return render_template(
        "incidencia_detalle.html",
        incidencia=incidencia,
        comentario_form=comentario_form,
        estado_form=estado_form,
    )


def request_es_actualizacion_estado() -> bool:
    from flask import request

    return (
        request.method == "POST"
        and request.form.get("accion") == "actualizar_estado"
    )


@main.post("/incidencias/<int:incidencia_id>/estado")
@login_required
def actualizar_estado_incidencia(incidencia_id: int):
    if not current_user.es_administrador():
        abort(403)

    incidencia = db.session.get(Incidencia, incidencia_id)

    if incidencia is None:
        abort(404)

    form = EstadoIncidenciaForm()

    if form.validate_on_submit():
        incidencia.estado = form.estado.data
        db.session.commit()

        flash("El estado de la incidencia se actualizó correctamente.", "success")
        return redirect(
            url_for("main.detalle_incidencia", incidencia_id=incidencia.id)
        )

    flash("No se pudo actualizar el estado.", "error")
    return redirect(
        url_for("main.detalle_incidencia", incidencia_id=incidencia.id)
    )