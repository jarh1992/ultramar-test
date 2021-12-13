from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import NON_FIELD_ERRORS
from django.forms import Form
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    """
    Formulario para creacion de Usuarios
    """

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ['first_name', 'last_name', 'id_user', 'email', 'username']

        error_messages = {
            NON_FIELD_ERRORS: {
                'unique_together': "%(User)s's %(id_user)s are not unique.",
            }
        }


class CustomUserChangeForm(Form):
    """
    Formulario para modificacion de Usuarios
    """

    prefix = 'm'
    username = forms.CharField(max_length=100, required=True)
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
