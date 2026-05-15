from django.db import models
from django.core.exceptions import ValidationError


class CicloLectivo(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="nombre")
    fecha_inicio = models.DateField(verbose_name="fecha de inicio")
    fecha_fin = models.DateField(verbose_name="fecha de fin")
    activo = models.BooleanField(default=True, verbose_name="activo")

    class Meta:
        verbose_name = "ciclo lectivo"
        verbose_name_plural = "ciclos lectivos"

    def __str__(self):
        return self.nombre


class Curso(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="nombre")
    anio = models.IntegerField(verbose_name="año")
    descripcion = models.TextField(blank=True, verbose_name="descripción")
    ciclo_lectivo = models.ForeignKey(
        CicloLectivo, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="cursos", verbose_name="ciclo lectivo",
    )

    class Meta:
        verbose_name = "curso"
        verbose_name_plural = "cursos"
        unique_together = ["nombre", "anio"]

    def __str__(self):
        return f"{self.nombre} ({self.anio})"


class Asignatura(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="nombre")
    curso = models.ForeignKey(
        Curso, on_delete=models.CASCADE, related_name="asignaturas", verbose_name="curso"
    )
    descripcion = models.TextField(blank=True, verbose_name="descripción")

    class Meta:
        verbose_name = "asignatura"
        verbose_name_plural = "asignaturas"
        unique_together = ["nombre", "curso"]

    def __str__(self):
        return f"{self.nombre} - {self.curso}"


class AsignacionCurso(models.Model):
    profesor = models.ForeignKey(
        "usuarios.Profesor",
        on_delete=models.CASCADE,
        related_name="asignaciones",
        verbose_name="profesor",
    )
    curso = models.ForeignKey(
        Curso, on_delete=models.CASCADE, related_name="asignaciones", verbose_name="curso"
    )
    asignatura = models.ForeignKey(
        Asignatura,
        on_delete=models.CASCADE,
        related_name="asignaciones",
        verbose_name="asignatura",
    )

    class Meta:
        verbose_name = "asignación de curso"
        verbose_name_plural = "asignaciones de cursos"
        unique_together = ["profesor", "curso", "asignatura"]

    def clean(self):
        if self.asignatura.curso != self.curso:
            raise ValidationError("La asignatura no pertenece al curso seleccionado")

    def __str__(self):
        return f"{self.profesor} - {self.asignatura} ({self.curso})"
