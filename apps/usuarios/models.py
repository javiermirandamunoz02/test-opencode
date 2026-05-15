from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class UsuarioManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("El email es obligatorio")
        email = self.normalize_email(email)
        extra_fields.setdefault("is_active", True)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("rol", Usuario.Rol.ADMIN)
        return self.create_user(email, password, **extra_fields)


class Usuario(AbstractBaseUser, PermissionsMixin):
    class Rol(models.TextChoices):
        ADMIN = "admin", "Administrativo"
        PROFESOR = "profesor", "Profesor"
        ALUMNO = "alumno", "Alumno"

    email = models.EmailField(unique=True, verbose_name="correo electrónico")
    nombre = models.CharField(max_length=100, verbose_name="nombre")
    apellido = models.CharField(max_length=100, verbose_name="apellido")
    rol = models.CharField(
        max_length=20, choices=Rol.choices, default=Rol.ALUMNO, verbose_name="rol"
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = UsuarioManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["nombre", "apellido", "rol"]

    class Meta:
        verbose_name = "usuario"
        verbose_name_plural = "usuarios"
        permissions = [
            ("puede_ver_usuarios", "Puede ver usuarios"),
            ("puede_crear_usuarios", "Puede crear usuarios"),
            ("puede_editar_usuarios", "Puede editar usuarios"),
            ("puede_eliminar_usuarios", "Puede eliminar usuarios"),
            ("puede_subir_notas", "Puede subir notas"),
            ("puede_ver_notas", "Puede ver notas"),
            ("puede_crear_tareas", "Puede crear tareas"),
            ("puede_entregar_tareas", "Puede entregar tareas"),
            ("puede_calificar_entregas", "Puede calificar entregas"),
        ]

    def __str__(self):
        return f"{self.apellido}, {self.nombre} ({self.get_rol_display()})"

    def get_full_name(self):
        return f"{self.nombre} {self.apellido}"

    def es_admin(self):
        return self.rol == self.Rol.ADMIN

    def es_profesor(self):
        return self.rol == self.Rol.PROFESOR

    def es_alumno(self):
        return self.rol == self.Rol.ALUMNO


class Alumno(models.Model):
    usuario = models.OneToOneField(
        Usuario, on_delete=models.CASCADE, related_name="perfil_alumno"
    )
    legajo = models.CharField(max_length=20, unique=True, verbose_name="legajo")
    curso = models.ForeignKey(
        "gestion.Curso",
        on_delete=models.SET_NULL,
        null=True,
        related_name="alumnos",
        verbose_name="curso",
    )

    class Meta:
        verbose_name = "alumno"
        verbose_name_plural = "alumnos"

    def __str__(self):
        return f"{self.usuario.get_full_name()} - Legajo: {self.legajo}"


class Profesor(models.Model):
    usuario = models.OneToOneField(
        Usuario, on_delete=models.CASCADE, related_name="perfil_profesor"
    )
    especialidad = models.CharField(max_length=200, blank=True, verbose_name="especialidad")
    telefono = models.CharField(max_length=50, blank=True, verbose_name="teléfono")
    horario_atencion = models.CharField(max_length=200, blank=True, verbose_name="horario de atención")

    class Meta:
        verbose_name = "profesor"
        verbose_name_plural = "profesores"

    def __str__(self):
        return self.usuario.get_full_name()


class Administrativo(models.Model):
    usuario = models.OneToOneField(
        Usuario, on_delete=models.CASCADE, related_name="perfil_administrativo"
    )
    cargo = models.CharField(max_length=200, verbose_name="cargo")

    class Meta:
        verbose_name = "administrativo"
        verbose_name_plural = "administrativos"

    def __str__(self):
        return f"{self.usuario.get_full_name()} - {self.cargo}"
