# Agenda de Contactos — API REST

Backend en Django REST Framework para administrar contactos. La API usa JWT y
requiere autenticación para todas las operaciones de contactos. El cliente web
incluido permite iniciar sesión y ejecutar las operaciones CRUD desde el
navegador.

## Requisitos

- Python 3.10 o superior
- Una base de datos PostgreSQL disponible y sus credenciales

## Instalación y ejecución local

Desde la carpeta raíz del repositorio:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```


## Cliente web

Abre `http://127.0.0.1:8000/cliente/`, inicia sesión con un usuario de Django
y administra contactos desde la API. El cliente solicita y renueva tokens JWT,
y envía el token de acceso como `Authorization: Bearer <token>`.

