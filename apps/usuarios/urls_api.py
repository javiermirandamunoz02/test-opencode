from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.routers import DefaultRouter
from . import views_api

router = DefaultRouter()
router.register(r"usuarios", views_api.UsuarioViewSet)
router.register(r"alumnos", views_api.AlumnoViewSet)
router.register(r"profesores", views_api.ProfesorViewSet)

urlpatterns = [
    path("token/", TokenObtainPairView.as_view(), name="token_obtain"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
] + router.urls
