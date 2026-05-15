from rest_framework import viewsets, permissions
from .models import Usuario, Alumno, Profesor
from .serializers import (
    UsuarioSerializer,
    UsuarioCreateSerializer,
    AlumnoSerializer,
    ProfesorSerializer,
)


class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all().order_by("apellido", "nombre")
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action == "create":
            return UsuarioCreateSerializer
        return UsuarioSerializer

    def get_queryset(self):
        user = self.request.user
        if user.es_alumno():
            return Usuario.objects.filter(id=user.id)
        return super().get_queryset()


class AlumnoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Alumno.objects.all().select_related("usuario", "curso")
    serializer_class = AlumnoSerializer
    permission_classes = [permissions.IsAuthenticated]


class ProfesorViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Profesor.objects.all().select_related("usuario")
    serializer_class = ProfesorSerializer
    permission_classes = [permissions.IsAuthenticated]
