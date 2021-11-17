from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.shortcuts import render
from main.forms import AuthForm
from main.forms import RegForm
from psycopg2 import IntegrityError


def main_page(request):
    return render(request, "main/main-page.html")


def registration_view(request):
    form = None
    message = ""
    if request.method == "POST":
        form = RegForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                user = form.save()
                login(request, user)
                return redirect("main")
            # Это нужно, когда кто-то руками в базе менял id и сбились внутренние счетчики
            except IntegrityError:
                message = "Try to register one more time, please"
        else:
            message = "Form not valid, something missing"
    return render(
        request,
        "main/user/register.html",
        {
            "form": form,
            "message": message,
        },
    )


class UserLoginView(LoginView):
    form_class = AuthForm
    template_name = "main/user/login.html"
    redirect_authenticated_user = False


def login_view(request):
    form = None
    if request.method == "POST":
        form = AuthForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]

            user = authenticate(request, email=email, password=password)

            if user is None:
                form.add_error("email", "Неправильный логин или пароль")
            else:
                login(request, user)
                return redirect("main")
    return render(request, "main/user/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("main")


@login_required()
def account_view(request):
    return render(request, "main/user/profile.html")
