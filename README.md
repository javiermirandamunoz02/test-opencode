# Sistema de Gestión Escolar

Aplicación web para la gestión de un colegio con roles de **Administrativo**, **Profesor** y **Alumno**.

## Tecnologías

| Componente | Tecnología |
|---|---|
| Backend | Django 5.x + Django REST Framework |
| Frontend | Django Templates + Bootstrap 5 |
| Autenticación | JWT (SimpleJWT) + Sesiones |
| Base de datos | PostgreSQL 16 |
| Contenedores | Docker Compose |

## Requisitos

- Docker y Docker Compose instalados

## Cómo levantar la aplicación

```bash
# 1. Clonar el repositorio
git clone <repo-url>
cd school

# 2. Iniciar los contenedores
docker compose up --build
```

Esto levanta:
- **PostgreSQL 16** en `localhost:5433`
- **App Django** en `http://localhost:8000`

> La primera vez, las migraciones y los datos mockeados se ejecutan automáticamente.

## Detener la aplicación

```bash
docker compose down
```

Para eliminar también los datos de la base de datos:
```bash
docker compose down -v
```

## Usuarios de prueba

Todos los usuarios tienen contraseña: **`test123`**

### Administradores
| Email | Nombre | Rol |
|---|---|---|
| admin@colegio.edu | Carlos Gutiérrez | Administrador |
| secretaria@colegio.edu | María López | Secretaria |

### Profesores
| Email | Nombre | Especialidad |
|---|---|---|
| profesor1@colegio.edu | Juan Martínez | Matemáticas |
| profesor2@colegio.edu | Ana Rodríguez | Lengua |
| profesor3@colegio.edu | Pedro García | Ciencias |
| profesor4@colegio.edu | Laura Fernández | Historia |
| profesor5@colegio.edu | Diego Pérez | Física |

### Alumnos
| Email | Legajo |
|---|---|
| alumno1@colegio.edu | LEG-20250001 |
| alumno2@colegio.edu | LEG-20250002 |
| ... hasta alumno30@colegio.edu | LEG-20250030 |

## Estructura del proyecto

```
school/
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── manage.py
├── .env
├── config/
│   ├── __init__.py
│   ├── settings.py          # Configuración general
│   ├── urls.py              # Rutas principales
│   └── wsgi.py
├── apps/
│   ├── usuarios/            # Gestión de usuarios y autenticación
│   │   ├── models.py        # CustomUser, Alumno, Profesor, Administrativo
│   │   ├── views.py         # Login, Dashboards por rol
│   │   ├── forms.py         # LoginForm por email
│   │   ├── serializers.py   # API serializers
│   │   └── authentication.py# Auth backend por email
│   ├── gestion/             # Cursos, Asignaturas, Asignaciones
│   │   ├── models.py
│   │   └── views.py
│   ├── academicos/          # Notas, Tareas, Entregas
│   │   ├── models.py
│   │   └── views.py
│   └── core/                # Base, decoradores, seed data
│       ├── decorators.py    # Decorador @rol_requerido
│       ├── context_processors.py
│       ├── management/commands/seed_data.py
│       ├── templates/       # Templates HTML
│       └── static/          # CSS y JS
└── README.md
```

## Modelo de datos

```
Usuario (email, nombre, apellido, rol)
  ├── Alumno (legajo, curso)
  ├── Profesor (especialidad)
  └── Administrativo (cargo)

Curso (nombre, año)
Asignatura (nombre, curso)
AsignacionCurso (profesor, curso, asignatura)

Nota (alumno, asignatura, profesor, valor, tipo, periodo)
Tarea (titulo, descripcion, asignatura, profesor, fecha_entrega)
EntregaTarea (tarea, alumno, archivo, nota, estado)
```

## Roles y permisos

| Acción | Admin | Profesor | Alumno |
|---|---|---|---|
| CRUD Usuarios | ✅ | ❌ | ❌ |
| CRUD Cursos | ✅ | ❌ | ❌ |
| Crear Asignaturas | ✅ | ❌ | ❌ |
| Asignar profesor a curso | ✅ | ❌ | ❌ |
| Subir Notas | ✅ | ✅ (suyas) | ❌ |
| Ver Notas | ✅ | ✅ (suyas) | ✅ (propias) |
| Crear Tareas | ✅ | ✅ | ❌ |
| Entregar Tareas | ❌ | ❌ | ✅ |
| Ver Tareas | ✅ | ✅ (suyas) | ✅ (de su curso) |
| Calificar entregas | ✅ | ✅ | ❌ |

## API REST

### Autenticación JWT
```bash
# Obtener token
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@colegio.edu", "password": "test123"}'

# Refrescar token
curl -X POST http://localhost:8000/api/token/refresh/ \
  -H "Content-Type: application/json" \
  -d '{"refresh": "<refresh_token>"}'
```

### Endpoints
| Método | Endpoint | Descripción |
|---|---|---|
| GET/POST | `/api/usuarios/` | Listar/Crear usuarios |
| GET | `/api/alumnos/` | Listar alumnos |
| GET | `/api/profesores/` | Listar profesores |
| GET/POST | `/api/cursos/` | Listar/Crear cursos |
| GET/POST | `/api/asignaturas/` | Listar/Crear asignaturas |
| GET/POST | `/api/notas/` | Listar/Crear notas |
| GET/POST | `/api/tareas/` | Listar/Crear tareas |
| GET/POST | `/api/entregas/` | Listar/Crear entregas |

## Comandos útiles

```bash
# Recargar datos mockeados
docker compose exec web python manage.py seed_data

# Crear migraciones
docker compose exec web python manage.py makemigrations

# Ejecutar migraciones
docker compose exec web python manage.py migrate

# Crear superusuario
docker compose exec web python manage.py createsuperuser

# Acceder a la shell de Django
docker compose exec web python manage.py shell

# Ver logs
docker compose logs -f web
```
