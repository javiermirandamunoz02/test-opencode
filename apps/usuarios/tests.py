from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from apps.usuarios.models import Alumno, Profesor, Administrativo
from apps.gestion.models import Curso, Asignatura

Usuario = get_user_model()


class UsuarioModelTest(TestCase):
    def setUp(self):
        self.user = Usuario.objects.create_user(
            email="test@test.com", password="test123",
            nombre="Juan", apellido="Pérez", rol=Usuario.Rol.ALUMNO,
        )

    def test_crear_usuario(self):
        self.assertEqual(self.user.email, "test@test.com")
        self.assertTrue(self.user.check_password("test123"))

    def test_roles(self):
        admin = Usuario(email="admin@test.com", nombre="A", apellido="B", rol=Usuario.Rol.ADMIN)
        self.assertTrue(admin.es_admin())
        self.assertFalse(admin.es_profesor())
        profe = Usuario(email="profe@test.com", nombre="A", apellido="B", rol=Usuario.Rol.PROFESOR)
        self.assertTrue(profe.es_profesor())
        alumno = Usuario(email="alum@test.com", nombre="A", apellido="B", rol=Usuario.Rol.ALUMNO)
        self.assertTrue(alumno.es_alumno())

    def test_superuser_creation(self):
        admin = Usuario.objects.create_superuser(email="super@test.com", password="admin123")
        self.assertTrue(admin.is_superuser)
        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.es_admin())


class AlumnoProfesorTest(TestCase):
    def test_crear_perfiles(self):
        user_alumno = Usuario.objects.create_user(
            email="alumno@test.com", password="test123", nombre="A", apellido="B", rol=Usuario.Rol.ALUMNO,
        )
        user_profe = Usuario.objects.create_user(
            email="profe@test.com", password="test123", nombre="C", apellido="D", rol=Usuario.Rol.PROFESOR,
        )
        user_admin = Usuario.objects.create_user(
            email="admin@test.com", password="test123", nombre="E", apellido="F", rol=Usuario.Rol.ADMIN,
        )
        curso = Curso.objects.create(nombre="1° A", anio=2025)
        alumno = Alumno.objects.create(usuario=user_alumno, legajo="LEG-001", curso=curso)
        profe = Profesor.objects.create(usuario=user_profe, especialidad="Matemáticas")
        admin = Administrativo.objects.create(usuario=user_admin, cargo="Secretario")
        self.assertIn("LEG-001", str(alumno))
        self.assertIn("Secretario", str(admin))


class UsuarioViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = Usuario.objects.create_superuser(email="admin@test.com", password="test123")
        self.profe = Usuario.objects.create_user(
            email="profe@test.com", password="test123", nombre="P", apellido="T", rol=Usuario.Rol.PROFESOR,
        )
        self.alumno_u = Usuario.objects.create_user(
            email="alumno@test.com", password="test123", nombre="A", apellido="B", rol=Usuario.Rol.ALUMNO,
        )
        Administrativo.objects.create(usuario=self.admin, cargo="Admin")
        Profesor.objects.create(usuario=self.profe)
        self.curso = Curso.objects.create(nombre="1° A", anio=2025)
        self.alumno = Alumno.objects.create(usuario=self.alumno_u, legajo="LEG-001", curso=self.curso)

    def test_login_get_authenticated_redirects(self):
        self.client.login(email="admin@test.com", password="test123")
        r = self.client.get(reverse("login"))
        self.assertEqual(r.status_code, 302)

    def test_login_post_invalid(self):
        r = self.client.post(reverse("login"), {"email": "bad@test.com", "password": "wrong"})
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "Credenciales inválidas")

    def test_logout(self):
        self.client.login(email="admin@test.com", password="test123")
        r = self.client.get(reverse("logout"))
        self.assertEqual(r.status_code, 302)

    def test_dashboard_admin_stats(self):
        self.client.login(email="admin@test.com", password="test123")
        r = self.client.get(reverse("dashboard_admin"))
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "Dashboard")

    def test_dashboard_profesor(self):
        self.client.login(email="profe@test.com", password="test123")
        r = self.client.get(reverse("dashboard_profesor"))
        self.assertEqual(r.status_code, 200)

    def test_dashboard_alumno(self):
        self.client.login(email="alumno@test.com", password="test123")
        r = self.client.get(reverse("dashboard_alumno"))
        self.assertEqual(r.status_code, 200)

    def test_dashboard_redirect_admin(self):
        self.client.login(email="admin@test.com", password="test123")
        r = self.client.get(reverse("dashboard"))
        self.assertEqual(r.status_code, 302)

    def test_profile_alumno(self):
        self.client.login(email="alumno@test.com", password="test123")
        r = self.client.get(reverse("profile"))
        self.assertEqual(r.status_code, 200)

    def test_profile_password_change(self):
        self.client.login(email="alumno@test.com", password="test123")
        r = self.client.post(reverse("profile"), {
            "action": "change_password",
            "old_password": "test123",
            "new_password1": "newpass123",
            "new_password2": "newpass123",
        })
        self.assertEqual(r.status_code, 302)
        self.alumno_u.refresh_from_db()
        self.assertTrue(self.alumno_u.check_password("newpass123"))

    def test_profile_password_mismatch(self):
        self.client.login(email="alumno@test.com", password="test123")
        r = self.client.post(reverse("profile"), {
            "action": "change_password",
            "old_password": "test123",
            "new_password1": "newpass1",
            "new_password2": "newpass2",
        })
        self.assertEqual(r.status_code, 302)
        msgs = list(r.cookies.get("messages", "").output())
        self.alumno_u.refresh_from_db()
        self.assertTrue(self.alumno_u.check_password("test123"))

    def test_profile_password_wrong_old(self):
        self.client.login(email="alumno@test.com", password="test123")
        r = self.client.post(reverse("profile"), {
            "action": "change_password",
            "old_password": "wrongpass",
            "new_password1": "newpass123",
            "new_password2": "newpass123",
        })
        self.assertEqual(r.status_code, 302)

    def test_profile_get(self):
        self.client.login(email="profe@test.com", password="test123")
        r = self.client.get(reverse("profile"))
        self.assertEqual(r.status_code, 200)

    def test_profile_edit_get(self):
        self.client.login(email="profe@test.com", password="test123")
        r = self.client.get(reverse("profile_edit"))
        self.assertEqual(r.status_code, 200)
