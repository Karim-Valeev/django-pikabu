from django.contrib.auth import logout
from django.shortcuts import redirect
from django.shortcuts import render


def main_page(request):
    return render(request, "main/main-page.html")


def logout_view(request):
    logout(request)
    return redirect("login")
