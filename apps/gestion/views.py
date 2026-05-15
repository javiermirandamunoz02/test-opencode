from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Curso, Asignatura, AsignacionCurso
from apps.core.decorators import rol_requerido


@login_required
def curso_list(request):
    cursos = Curso.objects.all().order_by("anio", "nombre")
    return render(request, "gestion/curso_list.html", {"cursos": cursos})


@login_required
@rol_requerido("admin")
def curso_create(request):
    if request.method == "POST":
        nombre = request.POST.get("nombre")
        anio = request.POST.get("anio")
        descripcion = request.POST.get("descripcion", "")
        Curso.objects.create(nombre=nombre, anio=anio, descripcion=descripcion)
        messages.success(request, "Curso creado exitosamente")
        return redirect("curso_list")
    return render(request, "gestion/curso_form.html")


@login_required
@rol_requerido("admin")
def curso_edit(request, pk):
    curso = get_object_or_404(Curso, pk=pk)
    if request.method == "POST":
        curso.nombre = request.POST.get("nombre")
        curso.anio = request.POST.get("anio")
        curso.descripcion = request.POST.get("descripcion", "")
        curso.save()
        messages.success(request, "Curso actualizado exitosamente")
        return redirect("curso_list")
    return render(request, "gestion/curso_form.html", {"curso": curso, "editar": True})


@login_required
@rol_requerido("admin")
def curso_delete(request, pk):
    curso = get_object_or_404(Curso, pk=pk)
    if request.method == "POST":
        curso.delete()
        messages.success(request, "Curso eliminado")
    return redirect("curso_list")


@login_required
def asignatura_list(request, curso_pk=None):
    if curso_pk:
        asignaturas = Asignatura.objects.filter(curso_id=curso_pk).select_related("curso")
    else:
        asignaturas = Asignatura.objects.all().select_related("curso").order_by("curso", "nombre")
    cursos = Curso.objects.all()
    return render(request, "gestion/asignatura_list.html", {
        "asignaturas": asignaturas,
        "cursos": cursos,
        "curso_seleccionado": curso_pk,
    })


@login_required
@rol_requerido("admin")
def asignatura_create(request):
    if request.method == "POST":
        nombre = request.POST.get("nombre")
        curso_id = request.POST.get("curso")
        descripcion = request.POST.get("descripcion", "")
        Asignatura.objects.create(nombre=nombre, curso_id=curso_id, descripcion=descripcion)
        messages.success(request, "Asignatura creada exitosamente")
        return redirect("asignatura_list")
    cursos = Curso.objects.all()
    return render(request, "gestion/asignatura_form.html", {"cursos": cursos})


@login_required
def asignacion_list(request):
    asignaciones = AsignacionCurso.objects.all().select_related("profesor__usuario", "curso", "asignatura")
    return render(request, "gestion/asignacion_list.html", {"asignaciones": asignaciones})


@login_required
@rol_requerido("admin")
def asignacion_create(request):
    if request.method == "POST":
        profesor_id = request.POST.get("profesor")
        curso_id = request.POST.get("curso")
        asignatura_id = request.POST.get("asignatura")
        AsignacionCurso.objects.create(
            profesor_id=profesor_id, curso_id=curso_id, asignatura_id=asignatura_id
        )
        messages.success(request, "Asignación creada exitosamente")
        return redirect("asignacion_list")

    from apps.usuarios.models import Profesor
    profesores = Profesor.objects.all().select_related("usuario")
    cursos = Curso.objects.all()
    asignaturas = Asignatura.objects.all()
    return render(request, "gestion/asignacion_form.html", {
        "profesores": profesores,
        "cursos": cursos,
        "asignaturas": asignaturas,
    })


@login_required
@rol_requerido("admin")
def asignacion_delete(request, pk):
    asignacion = get_object_or_404(AsignacionCurso, pk=pk)
    if request.method == "POST":
        asignacion.delete()
        messages.success(request, "Asignación eliminada")
    return redirect("asignacion_list")
