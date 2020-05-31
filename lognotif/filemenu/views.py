from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


@login_required(login_url="/account/login/")
def open_new_window_view(request):
    return render(request, "redirect.html", {})


@login_required(login_url="/account/login/")
def quit_app_view(request):
    return render(request, "quitapp.html", {})