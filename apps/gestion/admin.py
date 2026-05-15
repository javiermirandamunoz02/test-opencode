from django.contrib import admin
from .models import Curso, Asignatura, AsignacionCurso, CicloLectivo

admin.site.register(CicloLectivo)
admin.site.register(Curso)
admin.site.register(Asignatura)
admin.site.register(AsignacionCurso)
