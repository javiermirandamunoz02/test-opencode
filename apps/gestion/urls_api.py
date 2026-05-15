from rest_framework.routers import DefaultRouter
from . import views_api

router = DefaultRouter()
router.register(r"cursos", views_api.CursoViewSet)
router.register(r"asignaturas", views_api.AsignaturaViewSet)
router.register(r"asignaciones", views_api.AsignacionCursoViewSet)

urlpatterns = router.urls
