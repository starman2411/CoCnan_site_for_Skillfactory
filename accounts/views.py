from django.shortcuts import render, redirect
from .forms import BaseRegisterForm
from .models import RegistrationCodes
from board.models import CustomUser
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView
from .forms import LoginForm
from django.core.mail import send_mail
from django import forms
import random
import string


class MyLoginView(LoginView):
    form_class = LoginForm
    template_name = 'accounts/login.html'


def _generate_code():
    symbols = string.ascii_letters + string.digits
    code = ''.join(random.choice(symbols) for _ in range(8))
    return code


def _send_registration_code(code, email, username):
    send_mail(
        subject='Подтверждение почты на KoChan',
        message=f'Здравствуй, {username}! Твой код подтверждения почты на KoChan: {code}',
        from_email=None,
        recipient_list=[email]
    )
    return


def registration_view(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = BaseRegisterForm(request.POST)
            if form.is_valid():
                username = request.POST['username']
                email = request.POST['email']
                new_user = form.save(commit=False)
                new_user.is_active = False
                code = _generate_code()
                RegistrationCodes.objects.create(username=new_user.username, code=code, email=email)
                new_user.save()
                _send_registration_code(code, email, username)
                return redirect('accounts:registration_confirmation')
            return render(request, 'accounts/registration.html', {'form': form})
        else:
            form = BaseRegisterForm()
            return render(request, 'accounts/registration.html', {'form': form})
    else:
        return render(request, 'accounts/authanticated_already.html')


def registration_confirmation(request):
    if request.method == 'POST':
        username_email = request.POST['username_email']
        code = request.POST['code']

        if '@' in str(username_email):
            if CustomUser.objects.filter(email=username_email):
                user = CustomUser.objects.get(email=username_email)
        else:
            if CustomUser.objects.filter(username=username_email):
                user = CustomUser.objects.get(username=username_email)

        if (RegistrationCodes.objects.filter(code=code, username=username_email).exists()) or (RegistrationCodes.objects.filter(code=code, email=username_email).exists()):
            RegistrationCodes.objects.get(code=code).delete()
            user.is_active = True
            user.save()
            return render(request, 'accounts/registration_success.html')
        else:
            pass
        return render(request, 'accounts/code_confirmation.html')
    return render(request, 'accounts/code_confirmation.html')


def repeat_registration_code_view(request):
    email = request.POST['email']
    try:
        if RegistrationCodes.objects.filter(email=email):
            code = RegistrationCodes.objects.get(email=email)
            code.delete()
        new_code = _generate_code()
        RegistrationCodes.objects.create(username='', code=new_code, email=email)
        _send_registration_code(new_code, email, str(email))
        return redirect('accounts:registration_confirmation')
    except:
        return redirect('accounts:resend_code_form')


def resend_code_form_view(request):
    return render(request, 'accounts/repeat_code_sending.html')


def logout_view(request):
    if request.user:
        logout(request)
        return redirect('/main/')
    return redirect('/main/')
