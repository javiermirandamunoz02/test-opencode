from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Usuario, Alumno, Profesor, Administrativo


class UsuarioAdmin(BaseUserAdmin):
    list_display = ("email", "nombre", "apellido", "rol", "is_active", "is_staff")
    list_filter = ("rol", "is_active", "is_staff")
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Información personal", {"fields": ("nombre", "apellido", "rol")}),
        ("Permisos", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "nombre", "apellido", "rol", "password1", "password2"),
        }),
    )
    search_fields = ("email", "nombre", "apellido")
    ordering = ("email",)


admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Alumno)
admin.site.register(Profesor)
admin.site.register(Administrativo)
