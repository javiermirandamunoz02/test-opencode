from django.db.models import Q, Count


def roles(request):
    ctx = {
        "es_admin": False,
        "es_profesor": False,
        "es_alumno": False,
        "notificaciones_count": 0,
        "seccion_actual": "",
    }
    if not request.user.is_authenticated:
        return ctx

    user = request.user
    ctx["es_admin"] = user.es_admin()
    ctx["es_profesor"] = user.es_profesor()
    ctx["es_alumno"] = user.es_alumno()
    ctx["seccion_actual"] = request.resolver_match.url_name if request.resolver_match else ""

    from apps.academicos.models import EntregaTarea
    if user.es_profesor() and hasattr(user, "perfil_profesor") and user.perfil_profesor:
        ctx["notificaciones_count"] = EntregaTarea.objects.filter(
            Q(tarea__profesor=user.perfil_profesor) | Q(tarea__profesor__isnull=True),
            estado=EntregaTarea.Estado.PENDIENTE,
        ).count()
    elif user.es_admin():
        ctx["notificaciones_count"] = EntregaTarea.objects.filter(
            estado=EntregaTarea.Estado.PENDIENTE,
        ).count()

    return ctx
