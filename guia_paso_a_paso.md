# Guía paso a paso — Formularios en Django (Form, ModelForm, templates)

## Índice

1. [Preparación del entorno virtual](#1-preparación-del-entorno-virtual)
2. [Instalación de Django y creación del proyecto](#2-instalación-de-django-y-creación-del-proyecto)
3. [Creación de la aplicación](#3-creación-de-la-aplicación)
4. [Configuración de plantillas y archivos estáticos](#4-configuración-de-plantillas-y-archivos-estáticos)
5. [Formulario personalizado — `forms.py`](#5-formulario-personalizado---formspy)
6. [Vista — `views.py`](#6-vista---viewspy)
7. [Template base — `base.html`](#7-template-base---basehtml)
8. [Template de contacto — `contacto.html`](#8-template-de-contacto---contactohtml)
9. [Configuración de URLs](#9-configuración-de-urls)
10. [Probar el formulario](#10-probar-el-formulario)
11. [Git y buenas prácticas](#11-git-y-buenas-prácticas)
12. [Anexo — Explicaciones clave](#12-anexo--explicaciones-clave)

---

## 1. Preparación del entorno virtual

### 1.1 Verificar versión de Python

```bash
python --version
```

Django 4.x/5.x requiere Python 3.8+. Si no lo tienes, instálalo desde [python.org](https://python.org).

### 1.2 Crear el entorno virtual

El entorno virtual (**venv**) aísla las dependencias de este proyecto para que no interfieran con otros proyectos del sistema.

```bash
python -m venv venv
```

Esto crea una carpeta `venv/` que contiene una copia independiente de Python y pip.

```
venv/
├── bin/         # (Linux/Mac) scripts de activación, python, pip
├── include/
├── lib/
└── pyvenv.cfg
```

> **¿Qué es el venv?**  
> Es un mecanismo que crea un entorno Python aislado. Cada proyecto tiene sus propias dependencias sin conflicto con otros proyectos ni con el sistema operativo.

### 1.3 Activar el entorno virtual

**Linux / macOS:**
```bash
source venv/bin/activate
```

**Windows (CMD):**
```cmd
venv\Scripts\activate
```

**Windows (PowerShell):**
```powershell
venv\Scripts\Activate.ps1
```

Cuando el venv está activo, verás `(venv)` al inicio de la terminal:

```
(venv) $
```

### 1.4 Actualizar pip e instalar Django

```bash
pip install --upgrade pip
pip install django
```

### 1.5 Congelar dependencias

```bash
pip freeze > requirements.txt
```

> **requirements.txt** guarda la lista exacta de paquetes y versiones. Cualquier persona puede replicar el entorno con `pip install -r requirements.txt`.

---

## 2. Instalación de Django y creación del proyecto

### 2.1 Crear el proyecto

```bash
django-admin startproject actividad_m6_l4 .
```

> **IMPORTANTE:** El `.` (punto) al final le dice a Django que cree el proyecto **en el directorio actual**, sin crear una subcarpeta extra. Si omites el punto, Django crea `actividad_m6_l4/actividad_m6_l4/...` (doble anidación).

### 2.2 Estructura generada

```
actividad_m6_l4/
├── manage.py          # Herramienta de línea de comandos para el proyecto
├── actividad_m6_l4/   # Paquete de configuración del proyecto
│   ├── __init__.py    # Marca el directorio como un paquete Python
│   ├── asgi.py        # Configuración para servidores ASGI
│   ├── settings.py    # Configuración del proyecto (BD, apps, templates, etc.)
│   ├── urls.py        # Mapa de URLs raíz del proyecto
│   └── wsgi.py        # Configuración para servidores WSGI
├── venv/              # Entorno virtual
└── requirements.txt   # Dependencias
```

#### Explicación de cada archivo

| Archivo | Propósito |
|---|---|
| `manage.py` | Punto de entrada para comandos Django (runserver, startapp, migrate, etc.). No se modifica. |
| `settings.py` | Corazón de la configuración: base de datos, apps instaladas, plantillas, archivos estáticos, etc. |
| `urls.py` | Define las rutas URL del proyecto. Aquí se incluyen las rutas de las apps. |
| `wsgi.py` / `asgi.py` | Punto de entrada para servidores de producción (no tocar durante desarrollo). |

### 2.3 Probar que funciona

```bash
python manage.py runserver
```

Abre http://127.0.0.1:8000/ en el navegador. Deberías ver la página de bienvenida de Django (cohete).

Detén el servidor con `Ctrl + C`.

---

## 3. Creación de la aplicación

### 3.1 Crear la app

En Django, un **proyecto** contiene varias **aplicaciones** (apps). Cada app es un módulo independiente que encapsula una funcionalidad específica.

```bash
python manage.py startapp miapp
```

### 3.2 Estructura generada

```
miapp/
├── migrations/        # Migraciones de base de datos
│   └── __init__.py
├── __init__.py
├── admin.py           # Registro de modelos en el admin de Django
├── apps.py            # Configuración de la app
├── models.py          # Definición de modelos (tablas de BD)
├── tests.py           # Tests
└── views.py           # Vistas (lógica de cada página)
```

> **¿Qué falta?**  
> Django no crea `forms.py`, `urls.py`, `templates/` ni `static/` por defecto. Los creamos nosotros manualmente.

### 3.3 Registrar la app en `settings.py`

Abre `actividad_m6_l4/settings.py` y agrega `"miapp"` (o `"miapp.apps.MiappConfig"`) en `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "miapp",          # <--- nuestra app
]
```

> **¿Por qué es necesario?**  
> Django necesita saber qué apps existen para encontrar sus plantillas, archivos estáticos, migraciones, etc.

---

## 4. Configuración de plantillas y archivos estáticos

### 4.1 Crear carpetas

```bash
mkdir -p miapp/templates miapp/static/miapp/css miapp/static/miapp/js
```

### 4.2 Configurar `TEMPLATES` en `settings.py`

Por defecto, Django busca plantillas dentro de cada app (en `miapp/templates/`). No hace falta cambiar nada en `settings.py` si usas esa estructura.

Sin embargo, si también quieres una carpeta global de plantillas (en la raíz del proyecto), agrega `"DIRS"`:

```python
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],            # ← puedes agregar: BASE_DIR / "templates"
        "APP_DIRS": True,      # ← busca en miapp/templates/ automáticamente
        ...
    },
]
```

Con `APP_DIRS = True`, Django encuentra `miapp/templates/miapp/contacto.html` sin configuración extra.

### 4.3 Configurar archivos estáticos

Revisa que `settings.py` tenga:

```python
STATIC_URL = "static/"
```

Si quieres una carpeta global para estáticos (fuera de las apps), agrega:

```python
STATICFILES_DIRS = [
    BASE_DIR / "static",
]
```

Pero para este tutorial usaremos estáticos dentro de la app, así que no hace falta.

---

## 5. Formulario personalizado — `forms.py`

Crea el archivo `miapp/forms.py`:

```python
from django import forms


class ContactoForm(forms.Form):
    nombre = forms.CharField(
        label="Nombre",
        max_length=100,
        widget=forms.TextInput(attrs={"placeholder": "Tu nombre"}),
    )
    correo = forms.EmailField(
        label="Correo electrónico",
        widget=forms.EmailInput(attrs={"placeholder": "correo@ejemplo.com"}),
    )
    mensaje = forms.CharField(
        label="Mensaje",
        widget=forms.Textarea(attrs={"placeholder": "Escribe tu mensaje aquí..."}),
    )

    def clean_mensaje(self):
        """Validación personalizada: el mensaje debe tener al menos 10 caracteres."""
        mensaje = self.cleaned_data.get("mensaje", "")
        if len(mensaje) < 10:
            raise forms.ValidationError(
                "El mensaje debe tener al menos 10 caracteres."
            )
        return mensaje
```

### Explicación

| Elemento | Descripción |
|---|---|
| `forms.Form` | Formulario sin modelo asociado. Para formularios conectados a la BD usa `ModelForm`. |
| `CharField`, `EmailField` | Tipos de campo con validación incorporada (ej: `EmailField` valida el formato del email). |
| `widget` | Controla el HTML que se renderiza. `TextInput` → `<input type="text">`, `Textarea` → `<textarea>`. |
| `attrs` | Atributos HTML adicionales como `placeholder`, `class`, `id`. |
| `clean_mensaje()` | Método de validación **por campo**. Django lo llama automáticamente durante `is_valid()`. |
| `self.cleaned_data` | Diccionario con los datos **limpios y validados**. Solo está disponible *después* de la validación. |
| `ValidationError` | Excepción que Django asocia al campo y muestra como error. |

### Ciclo de validación de Django

```
1. request.POST entra al Form
2. Django llama a clean_<campo>() para cada campo que tenga el método
3. Django llama a clean() del formulario (validación cruzada entre campos)
4. Si todo OK → cleaned_data poblado, is_valid() = True
5. Si hay error → errores disponibles en form.errors y form.campo.errors
```

---

## 6. Vista — `views.py`

Edita `miapp/views.py`:

```python
from django.shortcuts import render, redirect
from .forms import ContactoForm


def contacto(request):
    """Vista que maneja el formulario de contacto."""
    if request.method == "POST":
        form = ContactoForm(request.POST)
        if form.is_valid():
            # 🟢 Datos válidos: procesarlos
            nombre = form.cleaned_data["nombre"]
            correo = form.cleaned_data["correo"]
            mensaje = form.cleaned_data["mensaje"]

            # Ejemplo: mostrar en consola (en producción se enviaría un email)
            print(f"📩 Nuevo mensaje de {nombre} ({correo}):")
            print(f"   {mensaje}")

            # Enviar éxito al template para mostrar mensaje al usuario
            return render(request, "miapp/contacto.html", {
                "form": ContactoForm(),     # formulario limpio para un nuevo envío
                "exito": True,              # bandera para mostrar mensaje de éxito
            })
    else:
        form = ContactoForm()

    return render(request, "miapp/contacto.html", {"form": form})
```

### Explicación del patrón

```
¿La petición es POST?
  ├── Sí → crear formulario con datos enviados
  │     └── ¿Los datos son válidos?
  │           ├── Sí → procesar y mostrar éxito
  │           └── No → renderizar con errores
  └── No → formulario vacío (GET inicial)
```

> **`request.method`** es "GET" cuando el usuario navega a la página y "POST" cuando el usuario envía el formulario.

### Alternativa con `redirect` después del éxito

Una práctica común es **redirigir** después de un POST exitoso (patrón POST-Redirect-GET):

```python
if form.is_valid():
    # ... procesar datos ...
    return redirect("contacto_exito")  # redirige a una URL de éxito
```

Pero para mantenerlo simple y mostrar el mensaje en la misma página, usamos `render` con una bandera `exito`.

---

## 7. Template base — `base.html`

Crea `miapp/templates/miapp/base.html`:

```html
{% load static %}
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Mi Proyecto Django{% endblock %}</title>
    <link rel="stylesheet" href="{% static 'miapp/css/estilos.css' %}">
    {% block extra_css %}{% endblock %}
</head>
<body>
    <header>
        <h1>Mi Aplicación Django</h1>
        <nav>
            <a href="{% url 'contacto' %}">Contacto</a>
        </nav>
    </header>

    <main>
        {% block content %}
        <!-- El contenido específico de cada página va aquí -->
        {% endblock %}
    </main>

    <footer>
        <p>&copy; 2026 - Proyecto Django</p>
    </footer>

    <script src="{% static 'miapp/js/script.js' %}"></script>
    {% block extra_js %}{% endblock %}
</body>
</html>
```

### Los bloques (`{% block %}`)

| Bloque | Propósito |
|---|---|
| `{% block title %}` | Título de la pestaña del navegador. Cada página hija puede redefinirlo. |
| `{% block content %}` | Contenido principal de la página. **Obligatorio** redefinirlo en cada página hija. |
| `{% block extra_css %}` | CSS adicional específico de una página (opcional). |
| `{% block extra_js %}` | JavaScript adicional específico de una página (opcional). |

### Explicación de herencia de plantillas

```
                 base.html (estructura general)
                     │
                     │  {% extends "base.html" %}
                     ▼
              contacto.html (contenido específico)
```

- `base.html` define el **layout general** (header, nav, footer, estructura HTML).
- Las páginas hijas **extienden** la base con `{% extends %}` y **llenan** los bloques con `{% block %}`.
- Si una página hija no redefine un bloque, se usa el contenido por defecto de la base.
- `{% extends "base.html" %}` **debe ser la primera etiqueta** del template hijo (antes de cualquier HTML).

---

## 8. Template de contacto — `contacto.html`

Crea `miapp/templates/miapp/contacto.html`:

```html
{% extends "miapp/base.html" %}

{% block title %}Contacto - Mi Proyecto Django{% endblock %}

{% block content %}
    <h2>Formulario de Contacto</h2>

    {% if exito %}
        <div class="alert alerta-exito">
            ✅ ¡Mensaje enviado correctamente! Gracias por contactarnos.
        </div>
    {% endif %}

    <form method="post" action="{% url 'contacto' %}" class="form-contacto">
        {% csrf_token %}

        {% if form.non_field_errors %}
            <div class="alert alerta-error">
                {{ form.non_field_errors }}
            </div>
        {% endif %}

        <div class="campo">
            {{ form.nombre.label_tag }}
            {{ form.nombre }}
            {% if form.nombre.errors %}
                <ul class="errores">
                    {% for error in form.nombre.errors %}
                        <li>{{ error }}</li>
                    {% endfor %}
                </ul>
            {% endif %}
        </div>

        <div class="campo">
            {{ form.correo.label_tag }}
            {{ form.correo }}
            {% if form.correo.errors %}
                <ul class="errores">
                    {% for error in form.correo.errors %}
                        <li>{{ error }}</li>
                    {% endfor %}
                </ul>
            {% endif %}
        </div>

        <div class="campo">
            {{ form.mensaje.label_tag }}
            {{ form.mensaje }}
            {% if form.mensaje.errors %}
                <ul class="errores">
                    {% for error in form.mensaje.errors %}
                        <li>{{ error }}</li>
                    {% endfor %}
                </ul>
            {% endif %}
        </div>

        <button type="submit">Enviar mensaje</button>
    </form>
{% endblock %}
```

### Formas de renderizar un formulario

| Forma | Descripción |
|---|---|
| `{{ form.as_p }}` | Renderiza cada campo envuelto en `<p>`. Rápido pero poco flexible. |
| `{{ form.as_table }}` | Renderiza en `<table>`. |
| `{{ form.as_ul }}` | Renderiza en `<li>`. |
| **Manual** (la de arriba) | Máximo control: cada campo por separado, con sus errores, clases, etc. |

### Explicación de la renderización manual

- `{{ form.nombre.label_tag }}` → renderiza la etiqueta `<label>` del campo.
- `{{ form.nombre }}` → renderiza el `<input>` / `<textarea>` del campo (respeta el `widget` definido en `forms.py`).
- `{{ form.nombre.errors }}` → lista de errores de validación de ese campo (si los hay).

### `{% csrf_token %}`

Es una etiqueta obligatoria en todo formulario que use `method="post"`. Genera un token de seguridad que Django verifica al recibir el POST para prevenir ataques **CSRF** (Cross-Site Request Forgery). Sin ella, Django devolverá un error 403 Forbidden.

### Mostrar errores

- **Errores de campo:** `{% if form.campo.errors %} ... {% endif %}` — se muestran bajo cada campo.
- **Errores globales:** `{{ form.non_field_errors }}` — errores de validación general (del `clean()` del formulario).
- **Mensaje de éxito:** lo controlamos con la variable `exito` que pasamos desde la vista.

---

## 9. Configuración de URLs

### 9.1 Crear `miapp/urls.py`

Crea el archivo `miapp/urls.py`:

```python
from django.urls import path
from . import views

urlpatterns = [
    path("contacto/", views.contacto, name="contacto"),
]
```

> **`name="contacto"`** permite referenciar esta URL en plantillas con `{% url 'contacto' %}` y en vistas con `redirect("contacto")`. Si cambias la ruta, solo cambias aquí y todas las referencias se actualizan automáticamente.

### 9.2 Incluir en el proyecto

Edita `actividad_m6_l4/urls.py`:

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("miapp.urls")),   # ← incluye las URLs de miapp
]
```

```
Petición del navegador
        │
        ▼
    actividad_m6_l4/urls.py  (raíz)
        │
        ├── /admin/     → django.contrib.admin
        └── /           → include("miapp.urls")
                │
                ▼
            miapp/urls.py
                │
                └── /contacto/  → views.contacto
```

---

## 10. Probar el formulario

### 10.1 Archivos estáticos (CSS básico)

Crea `miapp/static/miapp/css/estilos.css`:

```css
body {
    font-family: Arial, Helvetica, sans-serif;
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
    background: #f5f5f5;
}

.form-contacto {
    background: white;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.campo {
    margin-bottom: 15px;
}

.campo label {
    display: block;
    font-weight: bold;
    margin-bottom: 5px;
}

.campo input,
.campo textarea {
    width: 100%;
    padding: 8px;
    border: 1px solid #ccc;
    border-radius: 4px;
    box-sizing: border-box;
}

.errores {
    color: #d32f2f;
    list-style: none;
    padding: 0;
    margin: 5px 0;
    font-size: 0.9em;
}

.alerta-exito {
    background: #d4edda;
    color: #155724;
    padding: 12px;
    border-radius: 4px;
    margin-bottom: 15px;
}

.alerta-error {
    background: #f8d7da;
    color: #721c24;
    padding: 12px;
    border-radius: 4px;
    margin-bottom: 15px;
}

button {
    background: #007bff;
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 4px;
    cursor: pointer;
}

button:hover {
    background: #0056b3;
}
```

### 10.2 Ejecutar el servidor

```bash
python manage.py runserver
```

### 10.3 Probar escenarios

| Escenario | Acción | Resultado esperado |
|---|---|---|
| GET inicial | Navegar a `http://127.0.0.1:8000/contacto/` | Formulario vacío, sin errores |
| Todo vacío | Hacer click en "Enviar" sin llenar nada | Errores: "Este campo es obligatorio" en los 3 campos |
| Mensaje corto | Llenar nombre, correo válido, mensaje "hola" | Error: "El mensaje debe tener al menos 10 caracteres" |
| Correo inválido | Llenar nombre, correo "invalido", mensaje válido | Error: "Introduzca una dirección de correo electrónico válida" |
| Éxito | Llenar todo correctamente | Mensaje verde de éxito, formulario limpio |
| Consola | Revisar la terminal | Los datos ingresados se imprimen con `print()` |

### 10.4 Ver datos en consola

Después de un envío exitoso, la terminal mostrará:

```
📩 Nuevo mensaje de Juan Pérez (juan@ejemplo.com):
   Hola, me gustaría recibir más información sobre sus servicios.
```

---

## 11. Git y buenas prácticas

### 11.1 `.gitignore` para Django

Crea `.gitignore` en la raíz del proyecto:

```
# Entorno virtual
venv/
.env

# Python
__pycache__/
*.py[cod]
*.swp
*.swo

# Base de datos
db.sqlite3

# IDE
.vscode/
.idea/

# Django
*.log
media/
```

### 11.2 Commits iniciales

```bash
git init
git add .
git commit -m "feat: proyecto Django con formulario de contacto"
```

### 11.3 Mantener requirements.txt actualizado

Cada vez que instales un nuevo paquete:

```bash
pip freeze > requirements.txt
git add requirements.txt
git commit -m "chore: actualizar dependencias"
```

---

## 12. Anexo — Explicaciones clave

### 12.1 `forms.Form` vs `forms.ModelForm`

| `forms.Form` | `forms.ModelForm` |
|---|---|
| Formulario **sin** conexión a la BD | Formulario **conectado** a un modelo (tabla) |
| Defines todos los campos manualmente | Los campos se generan automáticamente desde el modelo |
| No hay `save()` | Tiene `save()` que guarda en BD |
| Ideal para: formularios de contacto, búsqueda, etc. | Ideal para: CRUD de modelos |

Ejemplo de `ModelForm`:

```python
from django.forms import ModelForm
from .models import Contacto

class ContactoModelForm(ModelForm):
    class Meta:
        model = Contacto
        fields = ["nombre", "correo", "mensaje"]
```

### 12.2 Ciclo request-response en Django

```
Navegador → URL → urls.py → views.py → (forms.py, models.py) → template → HTML → Navegador
```

1. El usuario escribe una URL.
2. `urls.py` encuentra la vista correspondiente.
3. La vista procesa la petición (lee BD, valida formularios, etc.).
4. La vista renderiza un template con contexto (variables).
5. Django devuelve el HTML al navegador.

### 12.3 CSRF — ¿Qué es y por qué es necesario?

**CSRF (Cross-Site Request Forgery)** es un ataque donde un sitio malicioso engaña al navegador de un usuario para que envíe una petición no deseada a un sitio donde el usuario está autenticado.

Django lo previene generando un **token único** por sesión que debe incluirse en cada formulario POST. Si el token no coincide, la petición es rechazada.

```html
<form method="post">
    {% csrf_token %}  <!-- ← este campo oculto contiene el token -->
    ...
</form>
```

### 12.4 Flujo completo de validación en Django

```
1. form = ContactoForm(request.POST)
2. form.is_valid() inicia la validación:
   a. Django llama a to_python() de cada campo (convierte string a tipo Python)
   b. Django llama a validate() de cada campo (validación por tipo)
   c. Django llama a run_validators() de cada campo (validadores adicionales, ej: max_length)
   d. Django llama a clean_<campo>() si existe (validación personalizada por campo)
   e. Django llama a clean() del formulario (validación cruzada, ej: confirmar contraseña)
3. Si todo pasa → cleaned_data lleno, is_valid() = True
4. Si algo falla → errors poblado, is_valid() = False
```

### 12.5 Resumen de comandos útiles

| Comando | Descripción |
|---|---|
| `python -m venv venv` | Crear entorno virtual |
| `source venv/bin/activate` | Activar venv (Linux/Mac) |
| `pip install django` | Instalar Django |
| `django-admin startproject nombre .` | Crear proyecto Django |
| `python manage.py startapp nombreapp` | Crear aplicación |
| `python manage.py runserver` | Iniciar servidor de desarrollo |
| `python manage.py makemigrations` | Preparar migraciones |
| `python manage.py migrate` | Aplicar migraciones a la BD |
| `pip freeze > requirements.txt` | Guardar dependencias |
| `pip install -r requirements.txt` | Instalar dependencias desde archivo |

---

> **📝 Nota final:**  
> Esta guía cubre desde la instalación del entorno hasta un formulario funcional con validación, reutilización de plantillas y buenas prácticas. Puedes usarla como referencia para cualquier proyecto Django que necesite formularios personalizados.
