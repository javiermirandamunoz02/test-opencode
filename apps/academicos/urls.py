from django.urls import path
from . import views

urlpatterns = [
    path("notas/", views.nota_list, name="nota_list"),
    path("notas/crear/", views.nota_create, name="nota_create"),
    path("notas/carga-masiva/", views.nota_carga_masiva, name="nota_carga_masiva"),
    path("notas/exportar/", views.nota_exportar_excel, name="nota_exportar_excel"),
    path("tareas/", views.tarea_list, name="tarea_list"),
    path("tareas/crear/", views.tarea_create, name="tarea_create"),
    path("entregas/", views.entrega_list, name="entrega_list"),
    path("entregas/tarea/<int:tarea_pk>/", views.entrega_list, name="entrega_list_tarea"),
    path("entregas/crear/", views.entrega_create, name="entrega_create"),
    path("entregas/<int:pk>/calificar/", views.entrega_calificar, name="entrega_calificar"),
    path("asistencia/", views.asistencia_list, name="asistencia_list"),
    path("asistencia/tomar/", views.asistencia_tomar, name="asistencia_tomar"),
    path("calendario/", views.calendario, name="calendario"),
    path("tareas/<int:pk>/", views.tarea_detail, name="tarea_detail"),
    path("comentarios/<int:tarea_pk>/", views.comentario_list, name="comentario_list"),
    path("boletin/<int:alumno_id>/", views.boletin_pdf, name="boletin_pdf"),
]
