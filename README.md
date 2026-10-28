<p align="center">
  <img
    src="./assets/portada-passforge.svg"
    alt="PassForge — Generador de contraseñas en Python"
    width="100%"
  />
</p>

<p align="center">
  Generador de contraseñas desarrollado en Python que documenta
  la evolución de una implementación educativa basada en <code>random</code>
  hacia una versión mejorada utilizando <code>secrets</code>,
  con interfaces CLI y web mediante Flask y Astro.
</p>

<p align="center">
  <img
    src="https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white"
    alt="Python 3.9+"
  />
  <img
    src="https://img.shields.io/badge/Flask-Web-000000?style=for-the-badge&logo=flask&logoColor=white"
    alt="Flask"
  />
  <img
    src="https://img.shields.io/badge/Interfaz-CLI-181717?style=for-the-badge"
    alt="CLI"
  />
  <img
    src="https://img.shields.io/badge/Licencia-MIT-2ea44f?style=for-the-badge"
    alt="Licencia MIT"
  />
  <img
    src="https://img.shields.io/badge/Estado-v2%20web%20activa-0ea5a5?style=for-the-badge"
    alt="Estado: v2 web activa"
  />
</p>

---

## Sobre PassForge

PassForge comenzó como un proyecto básico para practicar Python mediante la creación de un generador de contraseñas por consola.

La primera versión (`v1`) utilizaba el módulo `random`. Posteriormente revisé esa implementación desde una perspectiva de seguridad y detecté que su fuente de aleatoriedad no era apropiada para generar valores que deban ser difíciles de predecir.

A partir de esa revisión desarrollé una segunda versión (`v2`) utilizando `secrets`, junto con una longitud mínima y reglas básicas sobre los caracteres generados.

La versión actual separa la lógica de generación de la interacción por consola, permitiendo reutilizar el generador desde otras interfaces.

PassForge evoluciona ahora hacia una aplicación web moderna: Flask expone una API REST en Python y Astro proporciona una interfaz rápida, reactiva y accesible. La contraseña se genera en el backend con `secrets` (y cuenta con un modo de respaldo local con Web Crypto CSPRNG si el servidor no está disponible), sin almacenarse ni registrarse en ningún momento.

El repositorio conserva la implementación original junto con la versión actual con un propósito educativo:

> Mostrar cómo una solución funcional puede evolucionar cuando se revisan sus decisiones de diseño, seguridad y estructura.

---

## Inicio rápido

### Requisitos

- Python 3.9 o superior.
- Las dependencias se encuentran en `requirements.txt`.

### Crear un entorno virtual

Se recomienda utilizar un entorno virtual para aislar las dependencias del proyecto.

Desde la raíz:

```bash
python -m venv .venv
```

En Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

En Linux o macOS:

```bash
source .venv/bin/activate
```

### Instalar dependencias

Con el entorno virtual activado:

```bash
python -m pip install -r requirements.txt
```

### Ejecutar la interfaz CLI

Desde la raíz del proyecto:

```bash
python -m src.cli
```

El programa solicita la longitud de la contraseña y aplica un rango seguro de **12 a 128 caracteres**.

> [!WARNING]
> La implementación ubicada en `legacy/` se conserva únicamente como referencia educativa. Para utilizar la versión actual por consola, ejecuta `src.cli`.

### Ejecutar la aplicación web

El backend Flask expone el generador mediante una API REST.

Desde la raíz del proyecto:

```bash
python -m flask --app backend.passforge.app run --debug
```

Flask iniciará un servidor local disponible normalmente en:

```text
http://127.0.0.1:5000
```

Puedes comprobar el servicio en `http://127.0.0.1:5000/api/health`. El endpoint `POST /api/passwords` recibe la longitud y los tipos de caracteres seleccionados.

### Ejecutar el frontend Astro

Desde otra terminal:

```bash
cd frontend
npm install
npm run dev
```

La interfaz estará disponible normalmente en `http://localhost:4321`. Para conectar un backend remoto, define `PUBLIC_API_URL` en un archivo `.env` dentro de `frontend`.

### Cómo interpretar la entropía

La interfaz muestra una **estimación**, no una garantía. Con las cuatro categorías activadas se utiliza un alfabeto de 94 caracteres, por lo que 12 caracteres representan aproximadamente `78.7 bits` bajo una selección uniforme. El tiempo mostrado supone una búsqueda exhaustiva a `10¹¹` intentos por segundo y no representa todos los ataques posibles.

La seguridad real también depende del servicio donde se use la contraseña, su almacenamiento, la ausencia de filtraciones, la no reutilización y la seguridad del dispositivo. PassForge no guarda ni registra las contraseñas generadas.

### Despliegue en Vercel

El repositorio incluye `api/index.py` y `vercel.json` para desplegar el backend Flask como función Python junto con el frontend de Astro y las cabeceras de seguridad HTTP (`CSP`, `HSTS`, `X-Frame-Options`, `X-Content-Type-Options`).

---

## Pruebas

PassForge incluye pruebas automatizadas para comprobar el comportamiento de la lógica principal del generador y de la API REST.

Las pruebas utilizan `unittest`, incluido en la biblioteca estándar de Python, por lo que no requieren instalar dependencias adicionales.

Desde la raíz del proyecto:

```bash
python -m unittest discover -s tests -v
python -m unittest discover -s backend/tests -v
```

Las pruebas verifican que:

- el resultado generado sea una cadena de texto;
- se respete la longitud solicitada y los límites mínimo (12) y máximo (128);
- exista al menos una letra minúscula, mayúscula, número y símbolo cuando están activos;
- se respete el filtrado de subconjuntos individuales de caracteres;
- se rechacen entradas no válidas (como booleanos o todos los conjuntos desactivados);
- se apliquen cabeceras de seguridad (`Cache-Control: no-store`, `X-Frame-Options: DENY`, CORS) y límite de tasa (*Rate Limiting*).

Si todas las pruebas se completan correctamente, el resultado finalizará con:

```text
OK
```

---

## Estructura del proyecto

```text
pass-forge/
├── assets/
│   ├── logo.svg
│   └── portada-passforge.svg
├── api/
│   └── index.py
├── backend/
│   ├── passforge/
│   │   ├── app.py
│   │   ├── generator.py
│   │   └── routes.py
│   └── tests/
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   │   ├── PasswordGenerator.astro
│   │   │   └── PasswordManagerGuide.astro
│   │   ├── layouts/
│   │   │   └── Layout.astro
│   │   ├── pages/
│   │   │   └── index.astro
│   │   └── styles/
│   │       └── global.css
│   ├── .env.example
│   ├── package-lock.json
│   ├── package.json
│   └── astro.config.mjs
├── legacy/
│   └── generator_v1.py
├── src/
│   ├── __init__.py
│   ├── cli.py
│   ├── generator.py
│   └── web.py
├── tests/
│   └── test_generator.py
├── .gitignore
├── LICENSE
├── README.md
├── requirements.txt
└── vercel.json
```

- `legacy/` conserva la implementación original basada en `random`.
- `backend/passforge/generator.py` contiene la lógica criptográfica de generación de contraseñas.
- `backend/passforge/routes.py` contiene los endpoints de la API Flask.
- `backend/passforge/app.py` crea la aplicación Flask con cabeceras de seguridad y *rate limiting*.
- `frontend/` contiene la interfaz Astro, estilos y recursos públicos.
- `frontend/src/components/PasswordGenerator.astro` proporciona el generador interactivo con soporte para la API Flask y modo de respaldo Web Crypto CSPRNG.
- `frontend/src/components/PasswordManagerGuide.astro` orienta sobre el almacenamiento seguro.
- `api/index.py` es el punto de entrada serverless para Vercel.
- `src/generator.py` mantiene compatibilidad con la CLI y las pruebas originales re-exportando el motor principal.
- `src/cli.py` contiene la interacción mediante consola.
- `src/web.py` mantiene compatibilidad con el comando Flask original.
- `src/__init__.py` permite utilizar `src` como paquete de Python.
- `tests/test_generator.py` y `backend/tests/test_api.py` contienen las pruebas automatizadas.

---

## Evolución del proyecto

### v1 — Implementación original

La primera versión utilizaba `random.choice()` para seleccionar los caracteres de la contraseña.

```python
import random

def generador():
    caracter = (
        '@#$_&-+()/*:;!?~`£¢€¥^°%'
        'abcdefghijklmnñopqrstuvwxyz'
        'ABCDEFGHIJKLMNÑOPQRSTUVWXYZ'
        '1234567890'
    )

    acumulador = ''
    entrada = int(
        input('Longitud de la contraseña (mayor a 9 caracteres): ')
    )

    for i in range(0, entrada):
        acumulador += random.choice(caracter)

    print('Su contraseña generada:', acumulador)

generador()
```

### ¿Cuál era el problema?

El módulo `random` de Python utiliza **Mersenne Twister**, un generador pseudoaleatorio adecuado para simulaciones y otros usos generales, pero no está diseñado para generar valores que necesiten ser resistentes frente a predicción.

Una contraseña puede parecer aleatoria visualmente y aun así proceder de una fuente que no es apropiada para este propósito.

Además, la primera implementación:

- no garantiza la presencia de diferentes clases de caracteres;
- mezcla la lógica del generador con `input()` y `print()`;
- tiene margen de mejora en validación y experiencia de uso.

---

## v2 — Implementación mejorada

La segunda versión sustituye `random` por `secrets` y separa la lógica de generación de la interacción por consola.

La implementación reutilizable actual se encuentra en `backend/passforge/generator.py` (y se re-exporta en `src/generator.py` por compatibilidad con la CLI):

```python
import secrets
import string

MIN_LENGTH = 12
MAX_LENGTH = 128

def generate_password(
    length: int,
    *,
    lowercase: bool = True,
    uppercase: bool = True,
    digits: bool = True,
    symbols: bool = True,
) -> str:
    # Selección criptográficamente segura con al menos un carácter de cada conjunto activo
    characters = [secrets.choice(pool) for pool in pools]
    alphabet = "".join(pools)
    characters.extend(secrets.choice(alphabet) for _ in range(length - len(pools)))

    secrets.SystemRandom().shuffle(characters)
    return "".join(characters)
```

### `secrets`

`secrets` está diseñado para generar valores que no deberían resultar predecibles, como:

- contraseñas;
- tokens;
- credenciales temporales;
- otros valores sensibles.

Este es el cambio más importante entre ambas versiones.

### Rango de longitud seguro

La versión actual utiliza una longitud mínima de **12 caracteres** y una máxima de **128 caracteres**.

Si se solicita una longitud inferior al mínimo, la lógica del generador la ajusta automáticamente a 12.

### Reglas de composición

Cuando los cuatro conjuntos están habilitados, la contraseña generada incluye al menos:

- una letra mayúscula;
- una letra minúscula;
- un número;
- un símbolo.

Estas reglas evitan resultados que, por azar, omitan alguna de las clases de caracteres seleccionadas.

### Separación entre lógica e interfaz

La versión actual divide el programa en responsabilidades independientes:

```text
src/cli.py
    │
    │ solicita y valida la entrada del usuario
    ▼
src/generator.py ──► backend/passforge/generator.py
    │
    │ genera la contraseña con secrets
    ▼
resultado
```

`generator.py` no depende de `input()` ni de `print()`, por lo que la lógica puede reutilizarse desde otras interfaces sin modificar el funcionamiento interno del generador.

---

## Aplicación web actual

PassForge incorpora Flask y Astro para exponer el generador en una interfaz web moderna.

La aplicación backend se organiza en:

```text
backend/passforge/app.py
```

La API incluye rutas de salud y generación de contraseñas:

```python
GET  /api/health
POST /api/passwords
```

El flujo actual integra tanto la CLI como la interfaz web con el generador:

```text
CLI ──────► src/generator.py ──────► backend/passforge/generator.py
                                               ▲
WEB (Astro) ──► /api/passwords (Flask) ────────┘
```

---

## Comparación entre versiones

| Característica | v1 | v2 |
|---|---|---|
| Fuente de aleatoriedad | `random` | `secrets` |
| Tipo de aleatoriedad | PRNG de propósito general | Fuente criptográficamente segura |
| Longitud mínima / máxima | 10 / sin límite | 12 / 128 |
| Mayúsculas | No garantizadas | Garantizadas (seleccionables) |
| Minúsculas | No garantizadas | Garantizadas (seleccionables) |
| Números | No garantizados | Garantizados (seleccionables) |
| Símbolos | No garantizados | Garantizados (seleccionables) |
| Separación entre lógica e interfaz | No | Sí |
| Pruebas automatizadas | No | Sí |
| Protección HTTP y Rate Limiting | No | Sí |
| Uso dentro del proyecto | Referencia educativa | Versión actual |

---

## ¿Por qué no basta con usar más caracteres?

La primera versión ya permitía utilizar un conjunto amplio de caracteres.

Eso aumenta el espacio de combinaciones posibles, pero no resuelve el problema principal: **la fuente de aleatoriedad**.

Aumentar el número de caracteres disponibles no convierte un generador pseudoaleatorio de propósito general en uno criptográficamente adecuado.

Por eso el cambio fundamental de PassForge no fue añadir más símbolos, sino pasar de:

```python
random.choice(...)
```

a una generación basada en:

```python
secrets.choice(...)
```

y:

```python
secrets.SystemRandom().shuffle(...)
```

---

## Ejemplo de ejecución

### CLI

```text
Longitud de la contraseña (mínimo 12, máximo 128): 16
Tu contraseña segura: ****************
```

La contraseña mostrada arriba es únicamente ilustrativa.

Si se introduce una longitud inferior al mínimo:

```text
Longitud de la contraseña (mínimo 12, máximo 128): 8
Por seguridad, ajustaremos la longitud a 12.
Tu contraseña segura: ************
```

Si la entrada no corresponde a un número:

```text
Longitud de la contraseña (mínimo 12, máximo 128): hola
"hola" no es un número válido.
Longitud de la contraseña (mínimo 12, máximo 128):
```

### API web

Al ejecutar:

```bash
python -m flask --app backend.passforge.app run --debug
```

y visitar el endpoint de salud:

```text
http://127.0.0.1:5000/api/health
```

la API responde:

```text
{"service":"passforge-api","status":"ok"}
```

---

## Consideraciones de seguridad

PassForge comenzó como un proyecto educativo y ha evolucionado para ofrecer generación de contraseñas criptográficamente segura tanto en consola como en la web.

- **Generación:** Utiliza el CSPRNG del sistema operativo mediante `secrets` en Python (y cuenta con respaldo local mediante `window.crypto.getRandomValues` en el navegador si la API no está disponible).
- **Privacidad:** La API procesa la solicitud en memoria, incluye `Cache-Control: no-store` y no almacena ni registra ninguna contraseña generada.
- **Protección de la aplicación:** Incluye cabeceras de seguridad (`CSP`, `HSTS`, `X-Frame-Options: DENY`, `X-Content-Type-Options: nosniff`), validación estricta de entrada y límite de peticiones por IP (*Rate Limiting*). En producción debe utilizarse HTTPS y configurarse `FRONTEND_URL` con el origen real del frontend.

---

## Hitos completados y evolución futura

- [x] Separar la lógica de generación de la interfaz CLI.
- [x] Incorporar pruebas automatizadas para el generador y la API.
- [x] Añadir la estructura de la aplicación Flask e integrar el generador.
- [x] Añadir una interfaz web moderna con Astro.
- [x] Permitir seleccionar los conjuntos de caracteres utilizados.
- [x] Añadir validaciones de entrada adicionales, cabeceras de seguridad y *rate limiting*.
- [x] Incorporar modo de respaldo local con Web Crypto CSPRNG en el navegador.
- [ ] Permitir excluir determinados símbolos ambiguos (`l`, `1`, `I`, `O`, `0`).
- [ ] Añadir generador de frases de paso (*passphrases* estilo Diceware).

---

## Aprendizajes del proyecto

PassForge me permitió practicar y reforzar conceptos como:

`Python` · `random` · `secrets` · `string` · `CLI` · `Flask` · `Astro` · `HTTP` · `rutas` · `unittest` · `testing` · `validación` · `aleatoriedad` · `modularización` · `código seguro`

También sirvió como ejercicio para revisar una solución anterior y documentar su evolución en lugar de reemplazarla sin conservar el razonamiento detrás de los cambios.

---

## Autor

**Josué Chacae**

<p>
  <a href="https://josuechacae.dev">
    <img
      src="https://img.shields.io/badge/Portafolio-josuechacae.dev-0f766e?style=flat-square"
      alt="Portafolio"
    />
  </a>
  <a href="https://www.linkedin.com/in/chacae-josue">
    <img
      src="https://img.shields.io/badge/LinkedIn-Josué_Chacae-0A66C2?style=flat-square&logo=linkedin&logoColor=white"
      alt="LinkedIn"
    />
  </a>
  <a href="https://github.com/chacaejosue">
    <img
      src="https://img.shields.io/badge/GitHub-chacaejosue-181717?style=flat-square&logo=github&logoColor=white"
      alt="GitHub"
    />
  </a>
</p>

---

## Licencia

Este proyecto se distribuye bajo la [Licencia MIT](LICENSE).

Puedes utilizarlo, modificarlo y distribuirlo respetando los términos de la licencia.
