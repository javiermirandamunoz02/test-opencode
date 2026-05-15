from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import date, timedelta
import random

Usuario = get_user_model()


class Command(BaseCommand):
    help = "Carga datos mockeados para desarrollo"

    def add_arguments(self, parser):
        parser.add_argument("--force", action="store_true", help="Recargar datos aunque existan")

    def handle(self, *args, **options):
        if Usuario.objects.count() > 10 and not options.get("force"):
            self.stdout.write(self.style.WARNING("Los datos ya existen. Usá --force para recargar."))
            return
        self._limpiar_datos()
        self._crear_grupos()
        self._crear_usuarios()
        self._crear_cursos()
        self._crear_asignaturas()
        self._crear_perfiles()
        self._crear_asignaciones()
        self._asignar_grupos()
        self._crear_notas()
        self._crear_tareas()
        self._crear_entregas()
        self.stdout.write(self.style.SUCCESS("✅ Datos mockeados cargados exitosamente"))

    def _limpiar_datos(self):
        from django.contrib.auth.models import Group
        from apps.academicos.models import Nota, Tarea, EntregaTarea
        from apps.gestion.models import Curso, Asignatura, AsignacionCurso
        from apps.usuarios.models import Alumno, Profesor, Administrativo
        self.stdout.write("Limpiando datos existentes...")
        Group.objects.all().delete()
        EntregaTarea.objects.all().delete()
        Tarea.objects.all().delete()
        Nota.objects.all().delete()
        AsignacionCurso.objects.all().delete()
        Asignatura.objects.all().delete()
        Curso.objects.all().delete()
        Alumno.objects.all().delete()
        Profesor.objects.all().delete()
        Administrativo.objects.all().delete()
        Usuario.objects.exclude(is_superuser=True).delete()

    def _crear_grupos(self):
        from django.contrib.auth.models import Group, Permission
        from django.contrib.contenttypes.models import ContentType
        from apps.usuarios.models import Usuario
        from apps.academicos.models import Nota, Tarea, EntregaTarea

        self.stdout.write("Creando grupos y permisos...")
        ct_usuario = ContentType.objects.get_for_model(Usuario)
        ct_nota = ContentType.objects.get_for_model(Nota)
        ct_tarea = ContentType.objects.get_for_model(Tarea)
        ct_entrega = ContentType.objects.get_for_model(EntregaTarea)

        admin_group, _ = Group.objects.get_or_create(name="Administrativo")
        admin_group.permissions.set([
            Permission.objects.get(codename="puede_ver_usuarios", content_type=ct_usuario),
            Permission.objects.get(codename="puede_crear_usuarios", content_type=ct_usuario),
            Permission.objects.get(codename="puede_editar_usuarios", content_type=ct_usuario),
            Permission.objects.get(codename="puede_eliminar_usuarios", content_type=ct_usuario),
            Permission.objects.get(codename="puede_subir_notas", content_type=ct_usuario),
            Permission.objects.get(codename="puede_ver_notas", content_type=ct_usuario),
            Permission.objects.get(codename="puede_crear_tareas", content_type=ct_usuario),
            Permission.objects.get(codename="puede_calificar_entregas", content_type=ct_usuario),
        ])

        prof_group, _ = Group.objects.get_or_create(name="Profesor")
        prof_group.permissions.set([
            Permission.objects.get(codename="puede_subir_notas", content_type=ct_usuario),
            Permission.objects.get(codename="puede_ver_notas", content_type=ct_usuario),
            Permission.objects.get(codename="puede_crear_tareas", content_type=ct_usuario),
            Permission.objects.get(codename="puede_calificar_entregas", content_type=ct_usuario),
        ])

        alumno_group, _ = Group.objects.get_or_create(name="Alumno")
        alumno_group.permissions.set([
            Permission.objects.get(codename="puede_ver_notas", content_type=ct_usuario),
            Permission.objects.get(codename="puede_entregar_tareas", content_type=ct_usuario),
        ])

    def _asignar_grupos(self):
        from django.contrib.auth.models import Group
        for u in Usuario.objects.all():
            if u.es_admin():
                u.groups.add(Group.objects.get(name="Administrativo"))
            elif u.es_profesor():
                u.groups.add(Group.objects.get(name="Profesor"))
            elif u.es_alumno():
                u.groups.add(Group.objects.get(name="Alumno"))

    def _limpiar_datos(self):
        from apps.academicos.models import Nota, Tarea, EntregaTarea
        from apps.gestion.models import Curso, Asignatura, AsignacionCurso
        from apps.usuarios.models import Alumno, Profesor, Administrativo
        self.stdout.write("Limpiando datos existentes...")
        EntregaTarea.objects.all().delete()
        Tarea.objects.all().delete()
        Nota.objects.all().delete()
        AsignacionCurso.objects.all().delete()
        Asignatura.objects.all().delete()
        Curso.objects.all().delete()
        Alumno.objects.all().delete()
        Profesor.objects.all().delete()
        Administrativo.objects.all().delete()
        Usuario.objects.exclude(is_superuser=True).delete()

    def _crear_usuarios(self):
        self.stdout.write("Creando usuarios...")
        usuarios_data = [
            # Admin
            {"email": "admin@colegio.edu", "nombre": "Carlos", "apellido": "Gutiérrez", "rol": Usuario.Rol.ADMIN, "is_staff": True},
            {"email": "secretaria@colegio.edu", "nombre": "María", "apellido": "López", "rol": Usuario.Rol.ADMIN, "is_staff": True},
            # Profesores
            {"email": "profesor1@colegio.edu", "nombre": "Juan", "apellido": "Martínez", "rol": Usuario.Rol.PROFESOR},
            {"email": "profesor2@colegio.edu", "nombre": "Ana", "apellido": "Rodríguez", "rol": Usuario.Rol.PROFESOR},
            {"email": "profesor3@colegio.edu", "nombre": "Pedro", "apellido": "García", "rol": Usuario.Rol.PROFESOR},
            {"email": "profesor4@colegio.edu", "nombre": "Laura", "apellido": "Fernández", "rol": Usuario.Rol.PROFESOR},
            {"email": "profesor5@colegio.edu", "nombre": "Diego", "apellido": "Pérez", "rol": Usuario.Rol.PROFESOR},
        ]
        for data in usuarios_data:
            Usuario.objects.create_user(password="test123", **data)

        self.usuarios = {u.email: u for u in Usuario.objects.all()}

    def _crear_cursos(self):
        self.stdout.write("Creando cursos...")
        from apps.gestion.models import Curso
        cursos_data = [
            {"nombre": "1° A", "anio": 2025, "descripcion": "Primer año, división A"},
            {"nombre": "2° B", "anio": 2025, "descripcion": "Segundo año, división B"},
            {"nombre": "3° C", "anio": 2025, "descripcion": "Tercer año, división C"},
        ]
        for data in cursos_data:
            Curso.objects.create(**data)
        self.cursos = list(Curso.objects.all())

    def _crear_asignaturas(self):
        self.stdout.write("Creando asignaturas...")
        from apps.gestion.models import Asignatura
        asignaturas_por_curso = [
            ["Matemáticas", "Lengua y Literatura", "Ciencias Naturales", "Historia"],
            ["Matemáticas", "Lengua y Literatura", "Física", "Geografía"],
            ["Matemáticas", "Literatura", "Química", "Historia Mundial"],
        ]
        for i, curso in enumerate(self.cursos):
            for nombre in asignaturas_por_curso[i]:
                Asignatura.objects.create(
                    nombre=nombre, curso=curso,
                    descripcion=f"Asignatura {nombre} para {curso}"
                )
        self.asignaturas = list(Asignatura.objects.all())

    def _crear_perfiles(self):
        self.stdout.write("Creando perfiles...")
        from apps.usuarios.models import Alumno, Profesor, Administrativo
        from apps.gestion.models import Curso

        # Perfiles de admin
        admin_user = self.usuarios["admin@colegio.edu"]
        Administrativo.objects.create(usuario=admin_user, cargo="Administrador del Sistema")
        secretaria_user = self.usuarios["secretaria@colegio.edu"]
        Administrativo.objects.create(usuario=secretaria_user, cargo="Secretaria Académica")

        # Perfiles de profesor
        especialidades = ["Matemáticas", "Lengua", "Ciencias", "Historia", "Física"]
        prof_emails = [e for e in self.usuarios if e.startswith("profesor")]
        for i, email in enumerate(prof_emails):
            Profesor.objects.create(
                usuario=self.usuarios[email],
                especialidad=especialidades[i % len(especialidades)]
            )

        # Perfiles de alumno
        nombres_alumnos = [
            ("Sofía", "Álvarez"), ("Mateo", "Benítez"), ("Valentina", "Castillo"),
            ("Benjamín", "Díaz"), ("Camila", "Espinoza"), ("Santiago", "Flores"),
            ("Isabella", "Gómez"), ("Lucas", "Hernández"), ("Emma", "Iglesias"),
            ("Nicolás", "Jiménez"), ("Martina", "Klein"), ("Felipe", "Luna"),
            ("Lucía", "Méndez"), ("Sebastián", "Núñez"), ("Victoria", "Ortega"),
            ("Joaquín", "Paredes"), ("Emilia", "Quiroga"), ("Tomás", "Ramos"),
            ("Julieta", "Sosa"), ("Gabriel", "Torres"), ("Renata", "Ulloa"),
            ("Daniel", "Vargas"), ("Abril", "Walsh"), ("Maximiliano", "Yáñez"),
            ("Florencia", "Zamora"), ("Thiago", "Acosta"), ("Catalina", "Barrera"),
            ("Emilio", "Cabrera"), ("Lara", "Duarte"), ("Bruno", "Estévez"),
        ]
        for i, (nombre, apellido) in enumerate(nombres_alumnos):
            email = f"alumno{i+1}@colegio.edu"
            user = Usuario.objects.create_user(
                email=email, password="test123",
                nombre=nombre, apellido=apellido, rol=Usuario.Rol.ALUMNO,
            )
            self.usuarios[email] = user
            curso = self.cursos[i % len(self.cursos)]
            Alumno.objects.create(
                usuario=user, legajo=f"LEG-{2025}{i+1:04d}", curso=curso
            )

    def _crear_asignaciones(self):
        self.stdout.write("Creando asignaciones de profesores a cursos...")
        from apps.gestion.models import AsignacionCurso
        from apps.usuarios.models import Profesor
        profesores = list(Profesor.objects.all())

        for i, asignatura in enumerate(self.asignaturas):
            profesor = profesores[i % len(profesores)]
            AsignacionCurso.objects.create(
                profesor=profesor,
                curso=asignatura.curso,
                asignatura=asignatura,
            )

    def _crear_notas(self):
        self.stdout.write("Creando notas...")
        from apps.academicos.models import Nota
        from apps.usuarios.models import Alumno, Profesor
        from apps.gestion.models import Asignatura

        alumnos = list(Alumno.objects.all())
        profesores = list(Profesor.objects.all())
        tipos_nota = ["examen", "tarea", "participacion", "proyecto"]

        for alumno in alumnos:
            asignaturas_alumno = Asignatura.objects.filter(curso=alumno.curso)
            for asignatura in asignaturas_alumno:
                for _ in range(random.randint(2, 4)):
                    profesor = random.choice(profesores)
                    Nota.objects.create(
                        alumno=alumno,
                        asignatura=asignatura,
                        profesor=profesor,
                        valor=round(random.uniform(3.0, 10.0), 2),
                        tipo=random.choice(tipos_nota),
                        periodo=f"{random.choice(['1er', '2do', '3er'])} Trimestre",
                        fecha=date.today() - timedelta(days=random.randint(1, 90)),
                        observacion=random.choice([
                            "", "Buen trabajo", "Debe mejorar", "Excelente desempeño",
                            "Tarea completa", "Presentó a tiempo", "Requiere refuerzo",
                        ]),
                    )

    def _crear_tareas(self):
        self.stdout.write("Creando tareas...")
        from apps.academicos.models import Tarea
        from apps.usuarios.models import Profesor
        from apps.gestion.models import Asignatura

        profesores = list(Profesor.objects.all())

        tareas_descripcion = [
            "Resolver los ejercicios del libro, capítulo 3, del 1 al 20.",
            "Escribir un ensayo de 500 palabras sobre el tema visto en clase.",
            "Completar la guía de estudio y preparar para el examen parcial.",
            "Realizar el trabajo práctico en grupos de 4 personas.",
            "Investigar y presentar un resumen sobre el tema asignado.",
            "Dibujar el diagrama y explicar cada una de sus partes.",
        ]

        for i, asignatura in enumerate(self.asignaturas):
            for j in range(2):
                profesor = profesores[(i + j) % len(profesores)]
                dias_para_entrega = random.randint(5, 30)
                Tarea.objects.create(
                    titulo=f"TP N°{j+1}: {asignatura.nombre}",
                    descripcion=random.choice(tareas_descripcion),
                    asignatura=asignatura,
                    profesor=profesor,
                    fecha_entrega=date.today() + timedelta(days=dias_para_entrega),
                )

    def _crear_entregas(self):
        self.stdout.write("Creando entregas de tareas...")
        from apps.academicos.models import Tarea, EntregaTarea
        from apps.usuarios.models import Alumno

        tareas = list(Tarea.objects.all())
        alumnos = list(Alumno.objects.all())

        for tarea in tareas:
            alumnos_tarea = [a for a in alumnos if a.curso == tarea.asignatura.curso]
            for alumno in alumnos_tarea[:random.randint(3, len(alumnos_tarea))]:
                if random.random() > 0.2:
                    esta_calificado = random.random() > 0.4
                    EntregaTarea.objects.create(
                        tarea=tarea,
                        alumno=alumno,
                        fecha_entrega=timezone.now() - timedelta(hours=random.randint(1, 48)),
                        nota=round(random.uniform(4.0, 10.0), 2) if esta_calificado else None,
                        observacion=random.choice(["", "Entregado a tiempo", "Consulta entregada"]) if esta_calificado else "",
                        estado=EntregaTarea.Estado.CALIFICADO if esta_calificado else EntregaTarea.Estado.ENTREGADO,
                    )
