from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import models
from django.views import View
from .forms import LoginForm
from apps.core.decorators import rol_requerido


class LoginView(View):
    template_name = "usuarios/login.html"

    def get(self, request):
        if request.user.is_authenticated:
            return redirect(self._get_dashboard(request.user))
        form = LoginForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data["user"]
            login(request, user)
            return redirect(self._get_dashboard(user))
        return render(request, self.template_name, {"form": form, "error": "Credenciales inválidas"})

    def _get_dashboard(self, user):
        if user.es_alumno():
            return "dashboard_alumno"
        elif user.es_profesor():
            return "dashboard_profesor"
        return "dashboard_admin"


def logout_view(request):
    logout(request)
    return redirect("login")


@login_required
def dashboard_redirect(request):
    user = request.user
    if user.es_alumno():
        return redirect("dashboard_alumno")
    elif user.es_profesor():
        return redirect("dashboard_profesor")
    return redirect("dashboard_admin")


@login_required
@rol_requerido("admin")
def dashboard_admin(request):
    from apps.usuarios.models import Usuario
    from apps.gestion.models import Curso, Asignatura, AsignacionCurso
    from apps.academicos.models import Nota, Tarea, EntregaTarea
    context = {
        "total_usuarios": Usuario.objects.count(),
        "total_alumnos": Usuario.objects.filter(rol=Usuario.Rol.ALUMNO).count(),
        "total_profesores": Usuario.objects.filter(rol=Usuario.Rol.PROFESOR).count(),
        "total_cursos": Curso.objects.count(),
        "total_asignaturas": Asignatura.objects.count(),
        "total_asignaciones": AsignacionCurso.objects.count(),
        "total_notas": Nota.objects.count(),
        "total_tareas": Tarea.objects.count(),
        "total_entregas": EntregaTarea.objects.count(),
    }
    return render(request, "dashboard/admin.html", context)


@login_required
@rol_requerido("profesor")
def dashboard_profesor(request):
    from apps.gestion.models import AsignacionCurso
    from apps.academicos.models import Tarea, EntregaTarea
    if not hasattr(request.user, "perfil_profesor") or not request.user.perfil_profesor:
        messages.error(request, "Perfil de profesor no encontrado")
        return redirect("logout")
    profesor = request.user.perfil_profesor
    asignaciones = AsignacionCurso.objects.filter(profesor=profesor).select_related("curso", "asignatura")
    tareas_recientes = Tarea.objects.filter(profesor=profesor)[:5]
    entregas_pendientes = EntregaTarea.objects.filter(
        tarea__profesor=profesor, estado=EntregaTarea.Estado.ENTREGADO
    ).count()
    context = {
        "asignaciones": asignaciones,
        "tareas_recientes": tareas_recientes,
        "entregas_pendientes": entregas_pendientes,
    }
    return render(request, "dashboard/profesor.html", context)


@login_required
@rol_requerido("alumno")
def dashboard_alumno(request):
    from apps.academicos.models import Nota, EntregaTarea
    if not hasattr(request.user, "perfil_alumno") or not request.user.perfil_alumno:
        messages.error(request, "Perfil de alumno no encontrado")
        return redirect("logout")
    alumno = request.user.perfil_alumno
    notas = Nota.objects.filter(alumno=alumno).select_related("asignatura")[:10]
    entregas = EntregaTarea.objects.filter(alumno=alumno).select_related("tarea")[:5]
    context = {
        "notas": notas,
        "entregas": entregas,
    }
    return render(request, "dashboard/alumno.html", context)


@login_required
def profile_view(request):
    from apps.academicos.models import Nota, EntregaTarea
    user = request.user
    context = {"profile_user": user}

    if user.es_alumno():
        alumno = user.perfil_alumno
        notas = Nota.objects.filter(alumno=alumno).select_related("asignatura")
        entregas = EntregaTarea.objects.filter(alumno=alumno).select_related("tarea")
        context.update({"alumno": alumno, "notas": notas, "entregas": entregas})

    if request.method == "POST" and request.POST.get("action") == "change_password":
        old = request.POST.get("old_password")
        new1 = request.POST.get("new_password1")
        new2 = request.POST.get("new_password2")
        if not user.check_password(old):
            messages.error(request, "Contraseña actual incorrecta")
        elif new1 != new2:
            messages.error(request, "Las contraseñas nuevas no coinciden")
        elif len(new1) < 6:
            messages.error(request, "La contraseña debe tener al menos 6 caracteres")
        else:
            user.set_password(new1)
            user.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Contraseña cambiada exitosamente")
        return redirect("profile")

    return render(request, "usuarios/profile.html", context)


@login_required
def profile_edit(request):
    user = request.user
    if request.method == "POST":
        user.nombre = request.POST.get("nombre", user.nombre)
        user.apellido = request.POST.get("apellido", user.apellido)
        user.save()
        if user.es_profesor():
            profe = user.perfil_profesor
            profe.telefono = request.POST.get("telefono", "")
            profe.horario_atencion = request.POST.get("horario_atencion", "")
            profe.especialidad = request.POST.get("especialidad", "")
            profe.save()
        messages.success(request, "Perfil actualizado")
        return redirect("profile")
    return render(request, "usuarios/profile_edit.html", {"profile_user": user})


@login_required
def buscar_global(request):
    q = request.GET.get("q", "").strip()
    resultados = []

    if q:
        from apps.usuarios.models import Usuario
        from apps.gestion.models import Curso, Asignatura
        from apps.academicos.models import Nota, Tarea

        usuarios = Usuario.objects.filter(
            models.Q(nombre__icontains=q) | models.Q(apellido__icontains=q) | models.Q(email__icontains=q)
        )[:10]
        for u in usuarios:
            resultados.append({"tipo": "Usuario", "titulo": str(u), "url": "/perfil/", "detalle": u.email})

        cursos = Curso.objects.filter(models.Q(nombre__icontains=q))[:5]
        for c in cursos:
            resultados.append({"tipo": "Curso", "titulo": str(c), "url": "/gestion/cursos/", "detalle": c.descripcion[:80]})

        asignaturas = Asignatura.objects.filter(models.Q(nombre__icontains=q))[:5]
        for a in asignaturas:
            resultados.append({"tipo": "Asignatura", "titulo": str(a), "url": "/gestion/asignaturas/", "detalle": a.descripcion[:80]})

        tareas = Tarea.objects.filter(
            models.Q(titulo__icontains=q) | models.Q(descripcion__icontains=q)
        )[:5]
        for t in tareas:
            resultados.append({"tipo": "Tarea", "titulo": t.titulo, "url": "/academicos/tareas/", "detalle": t.descripcion[:80]})

        notas = Nota.objects.filter(
            models.Q(observacion__icontains=q) | models.Q(alumno__usuario__nombre__icontains=q)
        ).select_related("alumno__usuario", "asignatura")[:10]
        for n in notas:
            resultados.append({"tipo": "Nota", "titulo": f"{n.alumno} - {n.asignatura}: {n.valor}", "url": "/academicos/notas/", "detalle": n.observacion[:80]})

    return render(request, "usuarios/buscar.html", {"q": q, "resultados": resultados})
