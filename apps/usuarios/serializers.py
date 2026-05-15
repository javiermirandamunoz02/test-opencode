from rest_framework import serializers
from .models import Usuario, Alumno, Profesor, Administrativo


class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ["id", "email", "nombre", "apellido", "rol", "is_active", "date_joined"]
        read_only_fields = ["date_joined"]


class UsuarioCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Usuario
        fields = ["id", "email", "nombre", "apellido", "rol", "password"]

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = Usuario(**validated_data)
        user.set_password(password)
        user.save()

        rol = validated_data.get("rol")
        if rol == Usuario.Rol.ALUMNO:
            Alumno.objects.get_or_create(usuario=user)
        elif rol == Usuario.Rol.PROFESOR:
            Profesor.objects.get_or_create(usuario=user)
        elif rol == Usuario.Rol.ADMIN:
            Administrativo.objects.get_or_create(usuario=user, defaults={"cargo": "Administrador"})

        return user


class AlumnoSerializer(serializers.ModelSerializer):
    usuario = UsuarioSerializer(read_only=True)
    curso_nombre = serializers.CharField(source="curso.__str__", read_only=True)

    class Meta:
        model = Alumno
        fields = ["id", "usuario", "legajo", "curso", "curso_nombre"]


class ProfesorSerializer(serializers.ModelSerializer):
    usuario = UsuarioSerializer(read_only=True)

    class Meta:
        model = Profesor
        fields = ["id", "usuario", "especialidad"]


class AdministrativoSerializer(serializers.ModelSerializer):
    usuario = UsuarioSerializer(read_only=True)

    class Meta:
        model = Administrativo
        fields = ["id", "usuario", "cargo"]
