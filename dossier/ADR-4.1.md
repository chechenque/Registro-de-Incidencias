# ADR-4.1 — Gestión reproducible de dependencias

- **Fecha:** 2026-10-24
- **Proyecto:** Registro de incidencias

## 1. Contexto

El proyecto necesita un entorno de desarrollo reproducible que permita
instalar sus dependencias en otra máquina y reconstruir el entorno sin
depender de instalaciones globales de Python.

Se compararon dos alternativas:

- A: entorno virtual de Python, `pip` y `requirements.txt`.
- B: `uv`, `pyproject.toml` y `uv.lock`.

El experimento se realizó en macOS ARM64 utilizando Python 3.12.14.
Se registraron las dependencias antes y después de eliminar y reconstruir
cada entorno.

## 2. Opciones consideradas

### Opción A: venv + pip + requirements.txt

Utiliza las herramientas habituales de Python. El archivo
`requirements.txt` registra versiones concretas de las dependencias
instaladas, lo que permite reproducir este conjunto de paquetes.

Ventajas:
- Herramientas conocidas y ampliamente utilizadas.
- Instalación mediante `pip install -r requirements.txt`.
- Compatible con flujos de trabajo sencillos.

Limitaciones:
- La reproducibilidad depende del contenido del archivo, la versión de
  Python, la plataforma y la disponibilidad de los paquetes.
- Un archivo generado con `pip freeze` refleja el entorno existente;
  no sustituye por sí mismo una estrategia completa de gestión del proyecto.

### Opción B: uv + pyproject.toml + uv.lock

Utiliza `uv` para administrar las dependencias del proyecto y conservar
las versiones resueltas en un archivo de bloqueo.

Ventajas:
- Centraliza la configuración y las dependencias del proyecto.
- Permite reconstruir el entorno a partir de `uv.lock`.
- Facilita mantener una resolución consistente entre instalaciones.

Limitaciones:
- El equipo necesita disponer de `uv` o instalarlo como parte de su
  configuración de desarrollo.
- La reproducibilidad también depende de Python, la plataforma y la
  disponibilidad de los paquetes.

## 3. Criterio de evaluación

Se utilizaron los siguientes criterios:

1. Que las dependencias pudieran reinstalarse desde los archivos
   declarativos de cada alternativa.
2. Que las versiones registradas antes y después de la reconstrucción
   fueran idénticas.
3. Que la configuración pudiera mantenerse de forma clara en el repositorio.

## 4. Evidencia experimental

Plataforma registrada: macOS 26.6.2, ARM64.
Versión de Python utilizada para la comparación: 3.12.14.

Resultados observados:

| Métrica | A: requirements.txt | B: uv.lock |
|---|---:|---:|
| Entradas registradas antes | 12 | 13 |
| Entradas registradas después | 12 | 13 |
| Diferencias antes/después | 0 | 0 |
| Resultado de la comparación | Idéntico | Idéntico |

Los resultados se encuentran en `spike-4.1/`:

- `A_antes.txt`
- `A_despues.txt`
- `B_antes.txt`
- `B_despues.txt`
- `diff_A.txt`
- `diff_B.txt`
- `entorno.txt`

Los archivos `diff_A.txt` y `diff_B.txt` quedaron vacíos, indicando
que las listas comparadas fueron idénticas.

La evidencia inicial `B_antes_original.txt` corresponde a una ejecución
anterior con Python 3.9.7. Se conserva como registro histórico, pero
no se utiliza para la comparación final, porque las versiones de Python
no eran equivalentes.

La cantidad de entradas de A y B no es directamente equivalente:
B puede incluir el propio proyecto instalado en modo editable, mientras
que A registra las dependencias congeladas del entorno. Por ello, el
criterio principal fue comparar cada alternativa consigo misma.

## 5. Decisión

Se elige **uv + pyproject.toml + uv.lock** para gestionar las dependencias
del proyecto Registro de incidencias.

La prueba realizada no demostró una diferencia de reproducibilidad:
ambas alternativas reconstruyeron las mismas entradas registradas
en sus respectivas listas.

La elección de uv se fundamenta en disponer de un archivo de bloqueo
dedicado y mantener la configuración y las dependencias del proyecto
en un flujo de trabajo integrado. Esta es una decisión de organización
y mantenimiento; no una afirmación de superioridad demostrada por
las mediciones realizadas.

## 6. Consecuencias

- `pyproject.toml` será la fuente de configuración del proyecto.
- `uv.lock` se mantendrá versionado en Git.
- Se utilizará `uv sync` para reconstruir el entorno.
- Se documentará la versión de Python empleada.
- Los archivos de evidencia del experimento permanecerán en el repositorio.

## 7. Qué me haría cambiar de opinión

Reconsideraría esta decisión si el equipo necesitara trabajar en
entornos donde `uv` no estuviera disponible o si una prueba posterior,
realizada en varias máquinas y plataformas, demostrara que el flujo
con `requirements.txt` satisface mejor las necesidades operativas
con menor complejidad.

## 8. Fuentes

Las referencias técnicas y su contribución se documentan en
`sources-4.1.md` en la raíz del proyecto.
