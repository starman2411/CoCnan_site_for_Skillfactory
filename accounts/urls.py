from django.urls import path
from .views import registration_view, registration_confirmation, logout_view, MyLoginView, repeat_registration_code_view, resend_code_form_view

urlpatterns = [
    path('', registration_view),
    path('registration', registration_view, name='registration'),
    path('registration_confirmation', registration_confirmation, name='registration_confirmation'),
    path('logout/', logout_view, name='logout'),
    path('login/', MyLoginView.as_view(), name="login"),
    path('resend_code', repeat_registration_code_view, name="resend_code"),
    path('resend_code_form', resend_code_form_view, name="resend_code_form"),

]
