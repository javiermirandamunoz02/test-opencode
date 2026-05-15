from django.urls import path
from . import views

urlpatterns = [
    path("cursos/", views.curso_list, name="curso_list"),
    path("cursos/crear/", views.curso_create, name="curso_create"),
    path("cursos/<int:pk>/editar/", views.curso_edit, name="curso_edit"),
    path("cursos/<int:pk>/eliminar/", views.curso_delete, name="curso_delete"),
    path("asignaturas/", views.asignatura_list, name="asignatura_list"),
    path("asignaturas/curso/<int:curso_pk>/", views.asignatura_list, name="asignatura_list_curso"),
    path("asignaturas/crear/", views.asignatura_create, name="asignatura_create"),
    path("asignaciones/", views.asignacion_list, name="asignacion_list"),
    path("asignaciones/crear/", views.asignacion_create, name="asignacion_create"),
    path("asignaciones/<int:pk>/eliminar/", views.asignacion_delete, name="asignacion_delete"),
]
