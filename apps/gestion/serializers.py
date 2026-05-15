from rest_framework import serializers
from .models import Curso, Asignatura, AsignacionCurso


class CursoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Curso
        fields = ["id", "nombre", "anio", "descripcion"]


class AsignaturaSerializer(serializers.ModelSerializer):
    curso_nombre = serializers.CharField(source="curso.__str__", read_only=True)

    class Meta:
        model = Asignatura
        fields = ["id", "nombre", "curso", "curso_nombre", "descripcion"]


class AsignacionCursoSerializer(serializers.ModelSerializer):
    profesor_nombre = serializers.CharField(source="profesor.__str__", read_only=True)
    curso_nombre = serializers.CharField(source="curso.__str__", read_only=True)
    asignatura_nombre = serializers.CharField(source="asignatura.nombre", read_only=True)

    class Meta:
        model = AsignacionCurso
        fields = [
            "id", "profesor", "profesor_nombre",
            "curso", "curso_nombre",
            "asignatura", "asignatura_nombre",
        ]
