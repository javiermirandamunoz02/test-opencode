from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.core.exceptions import ValidationError
from apps.usuarios.models import Profesor, Alumno, Administrativo
from .models import Curso, Asignatura, AsignacionCurso, CicloLectivo
from datetime import date

Usuario = get_user_model()


class CicloLectivoTest(TestCase):
    def test_crear_ciclo(self):
        ciclo = CicloLectivo.objects.create(
            nombre="Ciclo Lectivo 2025",
            fecha_inicio=date(2025, 3, 1),
            fecha_fin=date(2025, 12, 20),
        )
        self.assertEqual(str(ciclo), "Ciclo Lectivo 2025")
        self.assertTrue(ciclo.activo)

    def test_curso_pertenece_ciclo(self):
        ciclo = CicloLectivo.objects.create(
            nombre="Ciclo 2025", fecha_inicio=date(2025, 3, 1), fecha_fin=date(2025, 12, 20),
        )
        curso = Curso.objects.create(nombre="1° A", anio=2025, ciclo_lectivo=ciclo)
        self.assertEqual(curso.ciclo_lectivo, ciclo)


class CursoModelTest(TestCase):
    def setUp(self):
        self.curso = Curso.objects.create(nombre="1° A", anio=2025, descripcion="Primer año")

    def test_crear_curso(self):
        self.assertEqual(str(self.curso), "1° A (2025)")

    def test_curso_unico(self):
        with self.assertRaises(Exception):
            Curso.objects.create(nombre="1° A", anio=2025)

    def test_asignatura_en_curso(self):
        asignatura = Asignatura.objects.create(nombre="Matemáticas", curso=self.curso)
        self.assertEqual(asignatura.curso, self.curso)


class AsignacionCursoTest(TestCase):
    def setUp(self):
        self.curso = Curso.objects.create(nombre="1° A", anio=2025)
        self.asignatura = Asignatura.objects.create(nombre="Matemáticas", curso=self.curso)
        self.profesor = Profesor.objects.create(
            usuario=Usuario.objects.create_user(
                email="profe@test.com", password="test123",
                nombre="P", apellido="Test", rol=Usuario.Rol.PROFESOR,
            ),
        )

    def test_crear_asignacion(self):
        asig = AsignacionCurso.objects.create(
            profesor=self.profesor, curso=self.curso, asignatura=self.asignatura,
        )
        self.assertIn(str(self.profesor), str(asig))

    def test_asignacion_unica(self):
        AsignacionCurso.objects.create(
            profesor=self.profesor, curso=self.curso, asignatura=self.asignatura,
        )
        with self.assertRaises(Exception):
            AsignacionCurso.objects.create(
                profesor=self.profesor, curso=self.curso, asignatura=self.asignatura,
            )

    def test_validacion_asignatura_no_pertenece_curso(self):
        otro_curso = Curso.objects.create(nombre="2° B", anio=2025)
        otra_asig = Asignatura.objects.create(nombre="Física", curso=otro_curso)
        asig = AsignacionCurso(profesor=self.profesor, curso=self.curso, asignatura=otra_asig)
        with self.assertRaises(ValidationError):
            asig.clean()


class GestionViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = Usuario.objects.create_superuser(email="admin@test.com", password="test123")
        self.alumno = Usuario.objects.create_user(
            email="alumno@test.com", password="test123",
            nombre="A", apellido="B", rol=Usuario.Rol.ALUMNO,
        )
        Administrativo.objects.create(usuario=self.admin, cargo="Admin")
        self.curso = Curso.objects.create(nombre="1° A", anio=2025)
        self.asignatura = Asignatura.objects.create(nombre="Matemáticas", curso=self.curso)
        profe_user = Usuario.objects.create_user(
            email="p@test.com", password="test123",
            nombre="P", apellido="T", rol=Usuario.Rol.PROFESOR,
        )
        self.profesor = Profesor.objects.create(usuario=profe_user)

    def test_curso_list(self):
        self.client.login(email="alumno@test.com", password="test123")
        r = self.client.get(reverse("curso_list"))
        self.assertEqual(r.status_code, 200)

    def test_curso_create_get(self):
        self.client.login(email="admin@test.com", password="test123")
        r = self.client.get(reverse("curso_create"))
        self.assertEqual(r.status_code, 200)

    def test_curso_create_post(self):
        self.client.login(email="admin@test.com", password="test123")
        r = self.client.post(reverse("curso_create"), {"nombre": "2° B", "anio": 2025, "descripcion": "Test"})
        self.assertEqual(r.status_code, 302)
        self.assertEqual(Curso.objects.count(), 2)

    def test_curso_edit_get(self):
        self.client.login(email="admin@test.com", password="test123")
        r = self.client.get(reverse("curso_edit", args=[self.curso.pk]))
        self.assertEqual(r.status_code, 200)

    def test_curso_edit_post(self):
        self.client.login(email="admin@test.com", password="test123")
        r = self.client.post(reverse("curso_edit", args=[self.curso.pk]),
                             {"nombre": "1° B", "anio": 2025, "descripcion": "Editado"})
        self.assertEqual(r.status_code, 302)
        self.curso.refresh_from_db()
        self.assertEqual(self.curso.nombre, "1° B")

    def test_curso_delete_post(self):
        self.client.login(email="admin@test.com", password="test123")
        r = self.client.post(reverse("curso_delete", args=[self.curso.pk]))
        self.assertEqual(r.status_code, 302)
        self.assertEqual(Curso.objects.count(), 0)

    def test_curso_delete_get(self):
        self.client.login(email="admin@test.com", password="test123")
        r = self.client.get(reverse("curso_delete", args=[self.curso.pk]))
        self.assertEqual(r.status_code, 302)

    def test_asignatura_list(self):
        self.client.login(email="alumno@test.com", password="test123")
        r = self.client.get(reverse("asignatura_list"))
        self.assertEqual(r.status_code, 200)
        r2 = self.client.get(reverse("asignatura_list") + f"?curso={self.curso.pk}")
        self.assertEqual(r2.status_code, 200)

    def test_asignatura_create_get(self):
        self.client.login(email="admin@test.com", password="test123")
        r = self.client.get(reverse("asignatura_create"))
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "1° A")

    def test_asignatura_create_post(self):
        self.client.login(email="admin@test.com", password="test123")
        r = self.client.post(reverse("asignatura_create"),
                             {"nombre": "Física", "curso": self.curso.pk, "descripcion": "Test"})
        self.assertEqual(r.status_code, 302)
        self.assertEqual(Asignatura.objects.count(), 2)

    def test_asignacion_list(self):
        self.client.login(email="alumno@test.com", password="test123")
        r = self.client.get(reverse("asignacion_list"))
        self.assertEqual(r.status_code, 200)

    def test_asignacion_create_get(self):
        self.client.login(email="admin@test.com", password="test123")
        r = self.client.get(reverse("asignacion_create"))
        self.assertEqual(r.status_code, 200)

    def test_asignacion_create_post(self):
        self.client.login(email="admin@test.com", password="test123")
        r = self.client.post(reverse("asignacion_create"), {
            "profesor": self.profesor.pk, "curso": self.curso.pk, "asignatura": self.asignatura.pk,
        })
        self.assertEqual(r.status_code, 302)
        self.assertEqual(AsignacionCurso.objects.count(), 1)

    def test_asignacion_delete_post(self):
        asig = AsignacionCurso.objects.create(profesor=self.profesor, curso=self.curso, asignatura=self.asignatura)
        self.client.login(email="admin@test.com", password="test123")
        r = self.client.post(reverse("asignacion_delete", args=[asig.pk]))
        self.assertEqual(r.status_code, 302)
        self.assertEqual(AsignacionCurso.objects.count(), 0)
