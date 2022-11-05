from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from board.models import CustomUser
from django import forms


class BaseRegisterForm(UserCreationForm):
    email = forms.EmailField(label="Email")
    required_css_class = "form-control"
    error_css_class = "error"

    class Meta:
        model = CustomUser
        fields = ("username", "email", "password1", "password2")


class CodeForm(forms.Form):
    code = forms.CharField(max_length=8)


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Email / Username')
