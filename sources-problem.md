# Fuentes para fundamentar el proyecto Registro de incidencias

**Fecha de consulta:** 2026-10-25

## Fuente 1. Atlassian — Incident Management Handbook

- URL: https://www.atlassian.com/incident-management/handbook
- Tipo: documentación técnica de una empresa especializada en
  herramientas de colaboración y gestión de servicios.
- Aporte: describe el registro de incidencias, la asignación de
  responsables, el seguimiento de acciones y el aprendizaje posterior.
- Aplicación al proyecto: fundamenta la necesidad de representar una
  incidencia como un registro consultable y de mantener su seguimiento.
- Limitación: describe prácticas de gestión de servicios; no demuestra
  que el problema exista en el contexto específico del proyecto.

## Fuente 2. GitHub Docs — About issues

- URL: https://docs.github.com/en/issues/tracking-your-work-with-issues/about-issues
- Tipo: documentación oficial de producto.
- Aporte: documenta el uso de incidencias para registrar, discutir y
  dar seguimiento a errores, tareas e ideas.
- Aplicación al proyecto: sirve como referencia para organizar reportes,
  conversaciones y seguimiento del trabajo.
- Limitación: documenta la funcionalidad de GitHub y no constituye una
  evaluación independiente de la solución propuesta.

## Fuente 3. OWASP — Authorization Cheat Sheet

- URL: https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html
- Tipo: guía técnica de seguridad para aplicaciones.
- Aporte: distingue autenticación de autorización y recomienda aplicar
  permisos mínimos, denegar por defecto y comprobar autorizaciones en
  cada solicitud pertinente.
- Aplicación al proyecto: fundamenta la separación de permisos entre
  reportantes y administradores y la validación de acceso en el servidor.
- Limitación: es una guía técnica; su existencia no demuestra que la
  aplicación cumpla estas recomendaciones. Esto deberá verificarse
  mediante implementación y pruebas.

## Conclusión provisional

Las tres fuentes respaldan decisiones de diseño relacionadas con el
registro, el seguimiento y la seguridad de las incidencias.

No sustituyen la evidencia directa del problema en el contexto de uso.
Esa validación permanece pendiente hasta recabar información real.
