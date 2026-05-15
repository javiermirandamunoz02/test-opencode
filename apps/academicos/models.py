from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from simple_history.models import HistoricalRecords


class Nota(models.Model):
    class Tipo(models.TextChoices):
        EXAMEN = "examen", "Examen"
        TAREA = "tarea", "Tarea"
        PARTICIPACION = "participacion", "Participación"
        PROYECTO = "proyecto", "Proyecto"

    alumno = models.ForeignKey(
        "usuarios.Alumno",
        on_delete=models.CASCADE,
        related_name="notas",
        verbose_name="alumno",
    )
    asignatura = models.ForeignKey(
        "gestion.Asignatura",
        on_delete=models.CASCADE,
        related_name="notas",
        verbose_name="asignatura",
    )
    profesor = models.ForeignKey(
        "usuarios.Profesor",
        on_delete=models.SET_NULL,
        null=True,
        related_name="notas_cargadas",
        verbose_name="profesor",
    )
    valor = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        verbose_name="nota",
    )
    tipo = models.CharField(
        max_length=20, choices=Tipo.choices, default=Tipo.EXAMEN, verbose_name="tipo"
    )
    periodo = models.CharField(max_length=50, blank=True, verbose_name="periodo")
    fecha = models.DateField(auto_now_add=True, verbose_name="fecha")
    observacion = models.TextField(blank=True, verbose_name="observación")

    history = HistoricalRecords()

    class Meta:
        verbose_name = "nota"
        verbose_name_plural = "notas"
        ordering = ["-fecha"]

    def __str__(self):
        return f"{self.alumno} - {self.asignatura}: {self.valor}"


class Tarea(models.Model):
    titulo = models.CharField(max_length=200, verbose_name="título")
    descripcion = models.TextField(verbose_name="descripción")
    asignatura = models.ForeignKey(
        "gestion.Asignatura",
        on_delete=models.CASCADE,
        related_name="tareas",
        verbose_name="asignatura",
    )
    profesor = models.ForeignKey(
        "usuarios.Profesor",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="tareas_creadas",
        verbose_name="profesor",
    )
    fecha_publicacion = models.DateField(auto_now_add=True, verbose_name="fecha de publicación")
    fecha_entrega = models.DateField(verbose_name="fecha de entrega")
    archivo = models.FileField(
        upload_to="tareas/", blank=True, null=True, verbose_name="archivo adjunto"
    )

    history = HistoricalRecords()

    class Meta:
        verbose_name = "tarea"
        verbose_name_plural = "tareas"
        ordering = ["-fecha_publicacion"]

    def __str__(self):
        return self.titulo


class EntregaTarea(models.Model):
    class Estado(models.TextChoices):
        PENDIENTE = "pendiente", "Pendiente"
        ENTREGADO = "entregado", "Entregado"
        CALIFICADO = "calificado", "Calificado"

    tarea = models.ForeignKey(
        Tarea, on_delete=models.CASCADE, related_name="entregas", verbose_name="tarea"
    )
    alumno = models.ForeignKey(
        "usuarios.Alumno",
        on_delete=models.CASCADE,
        related_name="entregas",
        verbose_name="alumno",
    )
    archivo = models.FileField(
        upload_to="entregas/", blank=True, null=True, verbose_name="archivo"
    )
    fecha_entrega = models.DateTimeField(auto_now_add=True, verbose_name="fecha de entrega")
    nota = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        null=True,
        blank=True,
        verbose_name="nota",
    )
    observacion = models.TextField(blank=True, verbose_name="observación")
    estado = models.CharField(
        max_length=20,
        choices=Estado.choices,
        default=Estado.PENDIENTE,
        verbose_name="estado",
    )

    history = HistoricalRecords()

    class Meta:
        verbose_name = "entrega de tarea"
        verbose_name_plural = "entregas de tareas"
        unique_together = ["tarea", "alumno"]

    def __str__(self):
        return f"{self.alumno} - {self.tarea}: {self.get_estado_display()}"


class Comentario(models.Model):
    tarea = models.ForeignKey(
        Tarea, on_delete=models.CASCADE, related_name="comentarios", verbose_name="tarea"
    )
    usuario = models.ForeignKey(
        "usuarios.Usuario", on_delete=models.CASCADE, related_name="comentarios",
        verbose_name="usuario",
    )
    texto = models.TextField(verbose_name="comentario")
    fecha = models.DateTimeField(auto_now_add=True, verbose_name="fecha")

    class Meta:
        verbose_name = "comentario"
        verbose_name_plural = "comentarios"
        ordering = ["fecha"]

    def __str__(self):
        return f"{self.usuario.get_full_name()}: {self.texto[:50]}"


class Asistencia(models.Model):
    alumno = models.ForeignKey(
        "usuarios.Alumno",
        on_delete=models.CASCADE,
        related_name="asistencias",
        verbose_name="alumno",
    )
    asignatura = models.ForeignKey(
        "gestion.Asignatura",
        on_delete=models.CASCADE,
        related_name="asistencias",
        verbose_name="asignatura",
    )
    fecha = models.DateField(verbose_name="fecha")
    presente = models.BooleanField(default=True, verbose_name="presente")
    observacion = models.TextField(blank=True, verbose_name="observación")
    registrado_por = models.ForeignKey(
        "usuarios.Profesor",
        on_delete=models.SET_NULL,
        null=True,
        related_name="asistencias_registradas",
        verbose_name="registrado por",
    )
    history = HistoricalRecords()

    class Meta:
        verbose_name = "asistencia"
        verbose_name_plural = "asistencias"
        unique_together = ["alumno", "asignatura", "fecha"]
        ordering = ["-fecha"]

    def __str__(self):
        estado = "✓" if self.presente else "✗"
        return f"{self.alumno} - {self.asignatura} ({self.fecha}): {estado}"
