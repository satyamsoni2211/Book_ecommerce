from django.shortcuts import render, redirect
from django.http import HttpRequest
from .forms import LoginForm
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from django.contrib import messages


# Create your views here.

def login_view(request: HttpRequest):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(request=request, **data)
            if user:
                login(request=request, user=user, )
                return redirect(settings.LOGIN_REDIRECT_URL)
            else:
                messages.add_message(request, messages.ERROR, "Incorrect username and password provided")
        else:
            messages.add_message(request, messages.ERROR, form.errors)
        return render(request, "index.html")


def logout_view(request: HttpRequest):
    logout(request)
    return redirect(settings.LOGOUT_REDIRECT_URL)
