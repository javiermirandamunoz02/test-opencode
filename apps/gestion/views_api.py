from rest_framework import viewsets, permissions
from .models import Curso, Asignatura, AsignacionCurso
from .serializers import CursoSerializer, AsignaturaSerializer, AsignacionCursoSerializer


class CursoViewSet(viewsets.ModelViewSet):
    queryset = Curso.objects.all().order_by("anio", "nombre")
    serializer_class = CursoSerializer
    permission_classes = [permissions.IsAuthenticated]


class AsignaturaViewSet(viewsets.ModelViewSet):
    queryset = Asignatura.objects.all().select_related("curso")
    serializer_class = AsignaturaSerializer
    permission_classes = [permissions.IsAuthenticated]


class AsignacionCursoViewSet(viewsets.ModelViewSet):
    queryset = AsignacionCurso.objects.all().select_related("profesor__usuario", "curso", "asignatura")
    serializer_class = AsignacionCursoSerializer
    permission_classes = [permissions.IsAuthenticated]
