from django.contrib import admin
from .models import Nota, Tarea, EntregaTarea, Asistencia, Comentario

admin.site.register(Nota)
admin.site.register(Tarea)
admin.site.register(EntregaTarea)
admin.site.register(Asistencia)
admin.site.register(Comentario)
