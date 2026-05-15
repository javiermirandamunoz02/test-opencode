from rest_framework import viewsets, permissions
from .models import Nota, Tarea, EntregaTarea
from .serializers import NotaSerializer, TareaSerializer, EntregaTareaSerializer


class NotaViewSet(viewsets.ModelViewSet):
    queryset = Nota.objects.all().select_related("alumno__usuario", "asignatura", "profesor__usuario")
    serializer_class = NotaSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        if user.es_alumno():
            return qs.filter(alumno=user.perfil_alumno)
        if user.es_profesor():
            return qs.filter(profesor=user.perfil_profesor)
        return qs


class TareaViewSet(viewsets.ModelViewSet):
    queryset = Tarea.objects.all().select_related("asignatura", "profesor__usuario")
    serializer_class = TareaSerializer
    permission_classes = [permissions.IsAuthenticated]


class EntregaTareaViewSet(viewsets.ModelViewSet):
    queryset = EntregaTarea.objects.all().select_related("alumno__usuario", "tarea")
    serializer_class = EntregaTareaSerializer
    permission_classes = [permissions.IsAuthenticated]
