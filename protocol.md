# Protocolo del proyecto: Registro de incidencias

## 1. Identificación

- **Proyecto:** Registro de incidencias
- **Tipo:** Aplicación web para registrar y dar seguimiento a incidencias.
- **Estado del protocolo:** Borrador sujeto a validación.

## 2. Planteamiento del problema

El proyecto parte de la hipótesis de que un proceso de registro de
incidencias sin un seguimiento centralizado puede dificultar la consulta
del estado de cada reporte, la identificación de responsables y la
conservación de las comunicaciones relacionadas.

Esta hipótesis deberá validarse con evidencia del contexto concreto
en el que se utilizaría la aplicación. Las fuentes documentales citadas
fundamentan las prácticas de gestión y seguridad, pero no demuestran
por sí solas que el problema exista en una organización específica.

## 3. Objetivo general

Desarrollar una aplicación web que permita registrar incidencias,
consultar su estado y mantener un historial de comentarios, con
autenticación y permisos diferenciados según el rol del usuario.

## 4. Usuarios y roles

### Reportante

- Iniciar sesión.
- Registrar una incidencia.
- Consultar sus incidencias.
- Revisar el estado de sus reportes.
- Agregar comentarios cuando corresponda.

### Administrador

- Consultar las incidencias registradas.
- Cambiar el estado de una incidencia.
- Asignar responsables cuando corresponda.
- Agregar comentarios de seguimiento.
- Gestionar las acciones permitidas por su rol.

Los permisos definitivos deberán quedar implementados y probados
en el servidor, no solamente ocultando opciones en la interfaz.

## 5. Alcance funcional

1. Autenticación de usuarios.
2. Roles de reportante y administrador.
3. Registro y consulta de incidencias.
4. Estados y prioridades para organizar el seguimiento.
5. Comentarios asociados a cada incidencia.
6. Validación de formularios.
7. Protección CSRF en formularios que modifican datos.
8. Autorización para restringir el acceso a operaciones y registros.
9. Interfaz basada en plantillas reutilizables.
10. Pruebas de las reglas de negocio y los permisos.

## 6. Modelo de datos inicial

### Usuario

Representa a la persona autenticada y contiene los datos necesarios
para identificarla y determinar su rol.

### Incidencia

Representa un reporte e incluye, como mínimo, título, descripción,
estado, prioridad, fecha de creación y usuario reportante.

### Comentario

Representa una comunicación vinculada con una incidencia e incluye
contenido, autor y fecha de creación.

Relaciones previstas:

- Un usuario puede registrar varias incidencias.
- Una incidencia puede tener varios comentarios.
- Un usuario puede registrar varios comentarios.

Las restricciones de acceso deberán comprobarse para cada operación.

## 7. Fuera de alcance inicial

- Aplicación móvil nativa.
- Integraciones con plataformas externas.
- Notificaciones por SMS.
- Automatización mediante inteligencia artificial.
- Arquitectura distribuida de microservicios.

## 8. Criterios de aceptación

- Los usuarios pueden autenticarse.
- Los permisos difieren según el rol.
- Se pueden registrar y consultar incidencias.
- Los comentarios quedan asociados a su incidencia y autor.
- Los formularios validan los datos recibidos.
- Las operaciones que modifican datos están protegidas contra CSRF.
- Los usuarios no pueden acceder a registros ni acciones para los que
  no tienen autorización.
- Las pruebas cubren las principales reglas de negocio.
- La aplicación puede desplegarse públicamente sin exponer secretos.

## 9. Validación pendiente

Antes de considerar validado el planteamiento del problema:

1. Identificar el contexto real en el que se utilizaría el sistema.
2. Recabar evidencia directa mediante una entrevista, observación o
   revisión de un proceso existente.
3. Registrar el hallazgo sin inventar testimonios ni resultados.
4. Contrastar el hallazgo con las fuentes documentales.
5. Ajustar el alcance si la evidencia lo requiere.

## 10. Referencias

Las fuentes y su contribución al diseño se encuentran en
`sources-problem.md`.
