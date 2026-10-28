---
name: conventional-commits-pr
description: >-
  Propone commits convencionales atómicos en español con verbos en 3.ª persona
  del presente (ej. 'añade', 'corrige', 'rediseña', 'sincroniza') y un Pull Request
  completo con título convencional, resumen conciso, pruebas y etiquetas. Espera
  la aprobación explícita del usuario antes de ejecutar los commits y publicar el PR con gh.
---

# Conventional Commits y Pull Request en Español

Esta skill guía al agente para analizar el árbol de trabajo de Git, estructurar cambios en commits atómicos bajo la especificación de Conventional Commits redactados en español con verbos en presente de indicativo (3.ª persona singular), redactar la propuesta de un Pull Request completo con etiquetas y ejecutarlo de forma desatendida con GitHub CLI (`gh`) una vez recibido el visto bueno del usuario.

## Reglas de Redacción de Commits

1. **Estructura Convencional**:
   `<tipo>(<ámbito opcional>): <descripción corta en presente indicativo>`
   
   Ejemplos:
   - `feat(security): implementa límite de peticiones y cabeceras HTTP`
   - `fix(cli): corrige la validación de rango entre 12 y 128 caracteres`
   - `refactor(ui): reorganiza la sección de custodia en 3 columnas simétricas`
   - `style(brand): rediseña el emblema en formato SVG autónomo`
   - `docs(readme): actualiza las instrucciones de despliegue y estructura`
   - `test(api): añade pruebas de integración para respuestas 429`

2. **Conjugación de Verbos en Español**:
   - **SIEMPRE** usar verbos en presente de indicativo (3.ª persona singular / imperativo afirmativo):
     - `añade` (NO "añadir", NO "agregado")
     - `corrige` (NO "corregir", NO "corrección")
     - `implementa` (NO "implementar")
     - `rediseña` (NO "rediseñar")
     - `reorganiza` (NO "reorganizar")
     - `sincroniza` (NO "sincronizar")
     - `actualiza` (NO "actualizar")
     - `elimina` (NO "eliminar")
     - `optimiza` (NO "optimizar")
     - `unifica` (NO "unificar")
     - `simplifica` (NO "simplificar")

3. **Agrupación Atómica**:
   - Cada commit debe abarcar un único propósito cohesivo (por ejemplo: seguridad backend, componentes UI, assets visuales, documentación).
   - No mezclar refactorizaciones estéticas con cambios de lógica de backend en el mismo commit.

4. **Estructura del Pull Request**:
   - **Título**: Convencional y representativo del objetivo general de la rama.
   - **Cuerpo del PR**:
     - *Resumen*: 2 a 3 líneas explicando el valor y contexto de los cambios.
     - *Cambios Principales*: Viñetas agrupadas por área/alcance.
     - *Verificación*: Comandos ejecutados y resultados (ej. pruebas unitarias, linters, compilación).
   - **Etiquetas (*Labels*)**: Sugerencia de etiquetas aplicables (`enhancement`, `security`, `ui`, `documentation`, etc.).

---

## Flujo de Trabajo

### Paso 1: Inspección de Cambios
1. Ejecutar `git status` para listar archivos modificados y sin seguimiento (*untracked*).
2. Ejecutar `git diff` para revisar las diferencias exactas de código.
3. Identificar la rama de trabajo actual con `git branch --show-current`.

### Paso 2: Formulación de la Propuesta
1. Agrupar los archivos modificados en commits lógicos y atómicos.
2. Redactar los mensajes de commit con los verbos conjugados en presente indicativo.
3. Redactar el borrador del Pull Request (título, cuerpo estructurado en markdown y etiquetas).
4. **DETENERSE Y ESPERAR APROBACIÓN**:
   - Presentar la propuesta completa al usuario.
   - **NUNCA ejecutar `git commit` ni `git push` sin la confirmación explícita del usuario.**

### Paso 3: Ejecución (Tras la aprobación del usuario)
1. Para cada commit aprobado:
   ```bash
   git add <archivos_del_commit>
   git commit -m "<mensaje_aprobado>"
   ```
2. Subir la rama al repositorio remoto:
   ```bash
   git push -u origin <rama_actual>
   ```
3. Crear el Pull Request usando GitHub CLI (`gh`):
   ```bash
   gh pr create --title "<titulo_pr>" --body "<cuerpo_pr>" --label "<labels>"
   ```
4. Confirmar al usuario la creación exitosa compartiendo el enlace generado.
