from rest_framework import serializers
from .models import Nota, Tarea, EntregaTarea


class NotaSerializer(serializers.ModelSerializer):
    alumno_nombre = serializers.CharField(source="alumno.__str__", read_only=True)
    asignatura_nombre = serializers.CharField(source="asignatura.nombre", read_only=True)
    profesor_nombre = serializers.CharField(source="profesor.__str__", read_only=True)

    class Meta:
        model = Nota
        fields = [
            "id", "alumno", "alumno_nombre",
            "asignatura", "asignatura_nombre",
            "profesor", "profesor_nombre",
            "valor", "tipo", "periodo", "fecha", "observacion",
        ]
        read_only_fields = ["fecha"]


class TareaSerializer(serializers.ModelSerializer):
    asignatura_nombre = serializers.CharField(source="asignatura.nombre", read_only=True)
    profesor_nombre = serializers.CharField(source="profesor.__str__", read_only=True)

    class Meta:
        model = Tarea
        fields = [
            "id", "titulo", "descripcion",
            "asignatura", "asignatura_nombre",
            "profesor", "profesor_nombre",
            "fecha_publicacion", "fecha_entrega", "archivo",
        ]
        read_only_fields = ["fecha_publicacion"]


class EntregaTareaSerializer(serializers.ModelSerializer):
    alumno_nombre = serializers.CharField(source="alumno.__str__", read_only=True)
    tarea_titulo = serializers.CharField(source="tarea.titulo", read_only=True)

    class Meta:
        model = EntregaTarea
        fields = [
            "id", "tarea", "tarea_titulo",
            "alumno", "alumno_nombre",
            "archivo", "fecha_entrega",
            "nota", "observacion", "estado",
        ]
        read_only_fields = ["fecha_entrega", "estado"]
