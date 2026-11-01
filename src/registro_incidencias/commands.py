import click
from flask.cli import with_appcontext

from registro_incidencias.extensions import db
from registro_incidencias.models import Usuario


@click.command("crear-administrador")
@with_appcontext
def crear_administrador():
    """Crea una cuenta administrativa desde la terminal."""

    nombre = click.prompt("Nombre completo")
    correo = click.prompt("Correo electrónico").strip().lower()

    existente = db.session.query(Usuario).filter_by(
        correo=correo
    ).first()

    if existente:
        click.echo("Ya existe una cuenta con ese correo.")
        return

    password = click.prompt(
        "Contraseña",
        hide_input=True,
        confirmation_prompt=True,
    )

    if len(password) < 12:
        click.echo("La contraseña debe tener al menos 12 caracteres.")
        return

    administrador = Usuario(
        nombre=nombre.strip(),
        correo=correo,
        rol="administrador",
    )

    administrador.establecer_password(password)

    db.session.add(administrador)
    db.session.commit()

    click.echo("Administrador creado correctamente.")