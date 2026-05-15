from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from apps.gestion.models import Curso, Asignatura, CicloLectivo
from apps.usuarios.models import Alumno, Profesor, Administrativo
from .models import Nota, Tarea, EntregaTarea, Asistencia, Comentario
from datetime import date, timedelta

Usuario = get_user_model()


class NotaModelTest(TestCase):
    def setUp(self):
        self.profe_user = Usuario.objects.create_user(
            email="profe@test.com", password="test123",
            nombre="Profe", apellido="Test", rol=Usuario.Rol.PROFESOR,
        )
        self.alumno_user = Usuario.objects.create_user(
            email="alumno@test.com", password="test123",
            nombre="Alumno", apellido="Test", rol=Usuario.Rol.ALUMNO,
        )
        self.curso = Curso.objects.create(nombre="1° A", anio=2025)
        self.asignatura = Asignatura.objects.create(nombre="Matemáticas", curso=self.curso)
        self.profesor = Profesor.objects.create(usuario=self.profe_user)
        self.alumno = Alumno.objects.create(usuario=self.alumno_user, legajo="LEG-TEST", curso=self.curso)

    def test_crear_nota(self):
        nota = Nota.objects.create(
            alumno=self.alumno, asignatura=self.asignatura,
            profesor=self.profesor, valor=8.5,
        )
        self.assertEqual(float(nota.valor), 8.5)
        self.assertIn("8.5", str(nota))

    def test_nota_sin_profesor(self):
        nota = Nota.objects.create(alumno=self.alumno, asignatura=self.asignatura, profesor=None, valor=6.0)
        self.assertIsNone(nota.profesor)

    def test_nota_fuera_de_rango(self):
        nota = Nota(alumno=self.alumno, asignatura=self.asignatura, profesor=self.profesor, valor=11)
        with self.assertRaises(Exception):
            nota.full_clean()


class TareaModelTest(TestCase):
    def setUp(self):
        user = Usuario.objects.create_user(
            email="profe@test.com", password="test123",
            nombre="Profe", apellido="Test", rol=Usuario.Rol.PROFESOR,
        )
        self.curso = Curso.objects.create(nombre="1° A", anio=2025)
        self.asignatura = Asignatura.objects.create(nombre="Matemáticas", curso=self.curso)
        self.profesor = Profesor.objects.create(usuario=user)

    def test_crear_tarea_sin_profesor(self):
        tarea = Tarea.objects.create(
            titulo="TP Test", descripcion="Test",
            asignatura=self.asignatura, profesor=None, fecha_entrega=date.today(),
        )
        self.assertIsNone(tarea.profesor)

    def test_crear_tarea_con_profesor(self):
        tarea = Tarea.objects.create(
            titulo="TP Test", descripcion="Test",
            asignatura=self.asignatura, profesor=self.profesor, fecha_entrega=date.today(),
        )
        self.assertEqual(tarea.profesor, self.profesor)


class AsistenciaModelTest(TestCase):
    def setUp(self):
        self.profe_user = Usuario.objects.create_user(
            email="profe@test.com", password="test123",
            nombre="Profe", apellido="Test", rol=Usuario.Rol.PROFESOR,
        )
        self.alumno_user = Usuario.objects.create_user(
            email="alumno@test.com", password="test123",
            nombre="Alumno", apellido="Test", rol=Usuario.Rol.ALUMNO,
        )
        self.curso = Curso.objects.create(nombre="1° A", anio=2025)
        self.asignatura = Asignatura.objects.create(nombre="Matemáticas", curso=self.curso)
        self.profesor = Profesor.objects.create(usuario=self.profe_user)
        self.alumno = Alumno.objects.create(usuario=self.alumno_user, legajo="LEG-TEST", curso=self.curso)

    def test_crear_asistencia_presente(self):
        a = Asistencia.objects.create(
            alumno=self.alumno, asignatura=self.asignatura,
            fecha=date.today(), presente=True, registrado_por=self.profesor,
        )
        self.assertTrue(a.presente)

    def test_asistencia_ausente(self):
        a = Asistencia.objects.create(
            alumno=self.alumno, asignatura=self.asignatura, fecha=date.today(), presente=False,
        )
        self.assertFalse(a.presente)

    def test_asistencia_unique(self):
        Asistencia.objects.create(alumno=self.alumno, asignatura=self.asignatura, fecha=date.today(), presente=True)
        with self.assertRaises(Exception):
            Asistencia.objects.create(alumno=self.alumno, asignatura=self.asignatura, fecha=date.today(), presente=False)


class ComentarioModelTest(TestCase):
    def setUp(self):
        self.user = Usuario.objects.create_user(
            email="user@test.com", password="test123",
            nombre="User", apellido="Test", rol=Usuario.Rol.PROFESOR,
        )
        self.curso = Curso.objects.create(nombre="1° A", anio=2025)
        self.asignatura = Asignatura.objects.create(nombre="Matemáticas", curso=self.curso)
        self.tarea = Tarea.objects.create(
            titulo="TP Test", descripcion="Desc",
            asignatura=self.asignatura, fecha_entrega=date.today(),
        )

    def test_crear_comentario(self):
        c = Comentario.objects.create(tarea=self.tarea, usuario=self.user, texto="Comentario de prueba")
        self.assertIn("Comentario de prueba", c.texto)

    def test_comentarios_orden(self):
        c1 = Comentario.objects.create(tarea=self.tarea, usuario=self.user, texto="Primero")
        Comentario.objects.create(tarea=self.tarea, usuario=self.user, texto="Segundo")
        Comentario.objects.create(tarea=self.tarea, usuario=self.user, texto="Tercero")
        comentarios = list(Comentario.objects.all())
        self.assertEqual(comentarios[0].texto, "Primero")


class ProfesorProfileTest(TestCase):
    def test_profesor_campos_extra(self):
        user = Usuario.objects.create_user(
            email="profe@test.com", password="test123",
            nombre="Profe", apellido="Test", rol=Usuario.Rol.PROFESOR,
        )
        profe = Profesor.objects.create(
            usuario=user, especialidad="Matemáticas",
            telefono="123456789", horario_atencion="Lunes 14-16",
        )
        self.assertEqual(profe.telefono, "123456789")
        self.assertEqual(profe.horario_atencion, "Lunes 14-16")


class ViewAuthTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = Usuario.objects.create_superuser(email="admin@test.com", password="test123")
        self.profe_user = Usuario.objects.create_user(
            email="profe@test.com", password="test123",
            nombre="Profe", apellido="Test", rol=Usuario.Rol.PROFESOR,
        )
        self.alumno_user = Usuario.objects.create_user(
            email="alumno@test.com", password="test123",
            nombre="Alumno", apellido="Test", rol=Usuario.Rol.ALUMNO,
        )
        Administrativo.objects.create(usuario=self.admin_user, cargo="Admin")
        Profesor.objects.create(usuario=self.profe_user)
        curso = Curso.objects.create(nombre="Test", anio=2025)
        Alumno.objects.create(usuario=self.alumno_user, legajo="LEG-TEST", curso=curso)

    def test_login_required(self):
        r = self.client.get(reverse("profile"))
        self.assertEqual(r.status_code, 302)

    def test_admin_login(self):
        self.client.login(email="admin@test.com", password="test123")
        r = self.client.get(reverse("dashboard_admin"))
        self.assertEqual(r.status_code, 200)

    def test_profesor_login(self):
        self.client.login(email="profe@test.com", password="test123")
        r = self.client.get(reverse("dashboard_profesor"))
        self.assertEqual(r.status_code, 200)

    def test_alumno_login(self):
        self.client.login(email="alumno@test.com", password="test123")
        r = self.client.get(reverse("dashboard_alumno"))
        self.assertEqual(r.status_code, 200)

    def test_alumno_no_accede_admin(self):
        self.client.login(email="alumno@test.com", password="test123")
        r = self.client.get(reverse("dashboard_admin"))
        self.assertIn(r.status_code, [302, 403])


class ViewIntegrationTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = Usuario.objects.create_superuser(email="admin@test.com", password="test123")
        self.profe_user = Usuario.objects.create_user(
            email="profe@test.com", password="test123",
            nombre="Profe", apellido="Test", rol=Usuario.Rol.PROFESOR,
        )
        self.alumno_user = Usuario.objects.create_user(
            email="alumno@test.com", password="test123",
            nombre="Alumno", apellido="Test", rol=Usuario.Rol.ALUMNO,
        )
        Administrativo.objects.create(usuario=self.admin, cargo="Admin")
        self.curso = Curso.objects.create(nombre="1° A", anio=2025)
        self.asignatura = Asignatura.objects.create(nombre="Matemáticas", curso=self.curso)
        self.profesor = Profesor.objects.create(usuario=self.profe_user)
        self.alumno = Alumno.objects.create(usuario=self.alumno_user, legajo="LEG-001", curso=self.curso)

    def test_nota_list_search(self):
        self.client.login(email="profe@test.com", password="test123")
        r = self.client.get(reverse("nota_list") + "?q=Matemáticas&tipo=examen&periodo=Trimestre")
        self.assertEqual(r.status_code, 200)

    def test_nota_create_profesor_get(self):
        self.client.login(email="profe@test.com", password="test123")
        r = self.client.get(reverse("nota_create"))
        self.assertEqual(r.status_code, 200)

    def test_nota_carga_masiva_get(self):
        self.client.login(email="admin@test.com", password="test123")
        r = self.client.get(reverse("nota_carga_masiva"))
        self.assertEqual(r.status_code, 200)

    def test_nota_carga_masiva_with_asignatura(self):
        self.client.login(email="admin@test.com", password="test123")
        r = self.client.get(reverse("nota_carga_masiva") + f"?asignatura={self.asignatura.id}&periodo=1er+Trimestre&tipo=examen")
        self.assertEqual(r.status_code, 200)

    def test_nota_carga_masiva_post(self):
        self.client.login(email="admin@test.com", password="test123")
        r = self.client.post(reverse("nota_carga_masiva") + f"?asignatura={self.asignatura.id}&periodo=1er+Trimestre&tipo=examen", {
            "asignatura": self.asignatura.id,
            "periodo": "1er Trimestre", "tipo": "examen",
            f"nota_{self.alumno.id}": "8.5",
            f"obs_{self.alumno.id}": "Bien",
        })
        self.assertEqual(r.status_code, 302)
        self.assertEqual(Nota.objects.count(), 1)

    def test_tarea_list_search(self):
        self.client.login(email="profe@test.com", password="test123")
        Tarea.objects.create(titulo="TP Matemáticas", descripcion="Test", asignatura=self.asignatura, fecha_entrega=date.today())
        r = self.client.get(reverse("tarea_list") + "?q=Matemáticas")
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "TP Matemáticas")

    def test_tarea_create_post(self):
        self.client.login(email="profe@test.com", password="test123")
        r = self.client.post(reverse("tarea_create"), {
            "titulo": "Nueva", "descripcion": "Desc",
            "asignatura": self.asignatura.id, "fecha_entrega": date.today().isoformat(),
        })
        self.assertEqual(r.status_code, 302)

    def test_entrega_list_filter(self):
        self.client.login(email="profe@test.com", password="test123")
        tarea = Tarea.objects.create(titulo="TP", descripcion="Desc", asignatura=self.asignatura, fecha_entrega=date.today())
        EntregaTarea.objects.create(tarea=tarea, alumno=self.alumno, estado=EntregaTarea.Estado.ENTREGADO)
        r = self.client.get(reverse("entrega_list") + "?estado=entregado")
        self.assertEqual(r.status_code, 200)

    def test_entrega_calificar_post(self):
        self.client.login(email="profe@test.com", password="test123")
        tarea = Tarea.objects.create(titulo="TP", descripcion="Desc", asignatura=self.asignatura, fecha_entrega=date.today())
        entrega = EntregaTarea.objects.create(tarea=tarea, alumno=self.alumno, estado=EntregaTarea.Estado.ENTREGADO)
        r = self.client.post(reverse("entrega_calificar", args=[entrega.pk]), {"nota": 8.5, "observacion": "Bien"})
        self.assertEqual(r.status_code, 302)
        entrega.refresh_from_db()
        self.assertEqual(entrega.estado, EntregaTarea.Estado.CALIFICADO)

    def test_asistencia_list(self):
        self.client.login(email="admin@test.com", password="test123")
        r = self.client.get(reverse("asistencia_list"))
        self.assertEqual(r.status_code, 200)

    def test_asistencia_tomar_get(self):
        self.client.login(email="admin@test.com", password="test123")
        r = self.client.get(reverse("asistencia_tomar") + f"?asignatura={self.asignatura.id}&fecha={date.today().isoformat()}")
        self.assertEqual(r.status_code, 200)

    def test_asistencia_tomar_post(self):
        self.client.login(email="admin@test.com", password="test123")
        r = self.client.post(reverse("asistencia_tomar") + f"?asignatura={self.asignatura.id}&fecha={date.today().isoformat()}", {
            "asignatura": self.asignatura.id, "fecha": date.today().isoformat(),
            f"presente_{self.alumno.id}": "true",
        })
        self.assertEqual(r.status_code, 302)
        self.assertEqual(Asistencia.objects.count(), 1)

    def test_calendario(self):
        self.client.login(email="profe@test.com", password="test123")
        r = self.client.get(reverse("calendario"))
        self.assertEqual(r.status_code, 200)

    def test_calendario_with_data(self):
        self.client.login(email="profe@test.com", password="test123")
        tarea = Tarea.objects.create(titulo="TP", descripcion="Desc", asignatura=self.asignatura,
                                      profesor=self.profesor, fecha_entrega=date.today() + timedelta(days=5))
        Nota.objects.create(alumno=self.alumno, asignatura=self.asignatura, valor=7.0, fecha=date.today())
        r = self.client.get(reverse("calendario"))
        self.assertEqual(r.status_code, 200)

    def test_calendario_navegacion(self):
        self.client.login(email="admin@test.com", password="test123")
        r = self.client.get(reverse("calendario") + "?mes=1&anio=2025")
        self.assertEqual(r.status_code, 200)

    def test_comentario_list_get(self):
        self.client.login(email="profe@test.com", password="test123")
        tarea = Tarea.objects.create(titulo="TP", descripcion="Desc", asignatura=self.asignatura, fecha_entrega=date.today())
        r = self.client.get(reverse("comentario_list", args=[tarea.pk]))
        self.assertEqual(r.status_code, 200)

    def test_comentario_list_post(self):
        self.client.login(email="profe@test.com", password="test123")
        tarea = Tarea.objects.create(titulo="TP", descripcion="Desc", asignatura=self.asignatura, fecha_entrega=date.today())
        r = self.client.post(reverse("comentario_list", args=[tarea.pk]), {"texto": "Mi comentario"})
        self.assertEqual(r.status_code, 302)
        self.assertEqual(Comentario.objects.count(), 1)

    def test_tarea_detail(self):
        self.client.login(email="profe@test.com", password="test123")
        tarea = Tarea.objects.create(titulo="TP", descripcion="Desc", asignatura=self.asignatura, fecha_entrega=date.today())
        Comentario.objects.create(tarea=tarea, usuario=self.profe_user, texto="Comentario")
        r = self.client.get(reverse("tarea_detail", args=[tarea.pk]))
        self.assertEqual(r.status_code, 200)

    def test_buscar_global(self):
        self.client.login(email="profe@test.com", password="test123")
        r = self.client.get(reverse("buscar_global") + "?q=Matemáticas")
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "Matemáticas")

    def test_buscar_sin_resultados(self):
        self.client.login(email="profe@test.com", password="test123")
        r = self.client.get(reverse("buscar_global") + "?q=zzzznotfound")
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "No se encontraron resultados")

    def test_buscar_vacio(self):
        self.client.login(email="profe@test.com", password="test123")
        r = self.client.get(reverse("buscar_global"))
        self.assertEqual(r.status_code, 200)

    def test_profile_edit_profesor(self):
        self.client.login(email="profe@test.com", password="test123")
        r = self.client.post(reverse("profile_edit"), {
            "nombre": "NuevoNombre", "apellido": "NuevoApellido",
            "telefono": "123456789", "horario_atencion": "Lun-Vie 14-16", "especialidad": "Matemáticas",
        })
        self.assertEqual(r.status_code, 302)
        self.profe_user.refresh_from_db()
        self.assertEqual(self.profe_user.nombre, "NuevoNombre")

    def test_nota_export_excel(self):
        self.client.login(email="admin@test.com", password="test123")
        Nota.objects.create(alumno=self.alumno, asignatura=self.asignatura, valor=7.0)
        r = self.client.get(reverse("nota_exportar_excel"))
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r["Content-Type"], "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")


class PasswordResetTest(TestCase):
    def setUp(self):
        self.client = Client()
        Usuario.objects.create_user(email="test@test.com", password="test123", nombre="Test", apellido="User", rol=Usuario.Rol.ALUMNO)

    def test_password_reset_page(self):
        r = self.client.get(reverse("password_reset"))
        self.assertEqual(r.status_code, 200)

    def test_password_reset_post(self):
        r = self.client.post(reverse("password_reset"), {"email": "test@test.com"})
        self.assertEqual(r.status_code, 302)


class LoginFormTest(TestCase):
    def test_login_form_invalid(self):
        from apps.usuarios.forms import LoginForm
        form = LoginForm(data={"email": "bad@email.com", "password": "wrong"})
        self.assertFalse(form.is_valid())
