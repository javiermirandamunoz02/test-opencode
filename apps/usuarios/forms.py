from django import forms
from django.contrib.auth import authenticate
from .models import Usuario


class LoginForm(forms.Form):
    email = forms.EmailField(
        label="Correo electrónico",
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "correo@ejemplo.com"}),
    )
    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "••••••••"}),
    )

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")
        user = authenticate(email=email, password=password)
        if user is None:
            raise forms.ValidationError("Email o contraseña incorrectos")
        if not user.is_active:
            raise forms.ValidationError("Esta cuenta está desactivada")
        cleaned_data["user"] = user
        return cleaned_data
