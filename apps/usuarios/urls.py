from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("dashboard/", views.dashboard_redirect, name="dashboard"),
    path("dashboard/admin/", views.dashboard_admin, name="dashboard_admin"),
    path("dashboard/profesor/", views.dashboard_profesor, name="dashboard_profesor"),
    path("dashboard/alumno/", views.dashboard_alumno, name="dashboard_alumno"),
    path("perfil/", views.profile_view, name="profile"),
    path("perfil/editar/", views.profile_edit, name="profile_edit"),
    path("buscar/", views.buscar_global, name="buscar_global"),
    path("password-reset/", auth_views.PasswordResetView.as_view(
        template_name="usuarios/password_reset_form.html",
        email_template_name="usuarios/password_reset_email.html",
        subject_template_name="usuarios/password_reset_subject.txt",
    ), name="password_reset"),
    path("password-reset/enviado/", auth_views.PasswordResetDoneView.as_view(
        template_name="usuarios/password_reset_done.html",
    ), name="password_reset_done"),
    path("password-reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(
        template_name="usuarios/password_reset_confirm.html",
    ), name="password_reset_confirm"),
    path("password-reset/completo/", auth_views.PasswordResetCompleteView.as_view(
        template_name="usuarios/password_reset_complete.html",
    ), name="password_reset_complete"),
]
