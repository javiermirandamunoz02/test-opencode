from rest_framework.routers import DefaultRouter
from . import views_api

router = DefaultRouter()
router.register(r"notas", views_api.NotaViewSet)
router.register(r"tareas", views_api.TareaViewSet)
router.register(r"entregas", views_api.EntregaTareaViewSet)

urlpatterns = router.urls
