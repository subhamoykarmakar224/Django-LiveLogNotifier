from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from .form import FormUser, FormNewServer
from django.contrib.auth.decorators import login_required
import accounts.DBOPS.MongoDBOps as db


@login_required(login_url="/account/login/")
def user_profile_view(request):
    if request.method == 'POST':
        formUserCreate = FormUser(request.POST)
        if formUserCreate.is_valid():
            validUserName = True
            try:
                User.objects.get(username=formUserCreate.cleaned_data['username'])
                validUserName = False
            except:
                print("Username valid")

            if validUserName:
                username = formUserCreate.cleaned_data['username']
                passwd = formUserCreate.cleaned_data['password']
                role = formUserCreate.cleaned_data['role']
                if role == "Admin":
                    User.objects.create_superuser(
                        username=str(username), email="", password=passwd)
                elif role == "Other":
                    User.objects.create_user(str(username), password=passwd)

                return redirect('accounts:user_profile_view')
            else:
                userlist = User.objects.all()
                log_servers = db.getAllServerData()
                context = {
                    "formusercreate": formUserCreate,
                    "profile_page": 'active',
                    "userlist": userlist,
                    "log_servers": log_servers,
                    "error_add_user": 'Username already in user. Please user a different one.',
                    "show_add_userform": "y"
                }
                return render(request, 'profile.html', context)
    else:
        formUserCreate = FormUser()

    if request.user.is_superuser:
        userlist = User.objects.all()
        log_servers = db.getAllServerData()
        context = {
            "formusercreate": formUserCreate,
            "profile_page": 'active',
            "userlist": userlist,
            "log_servers": log_servers,
            "error_add_user": ''
        }
    else:
        log_servers = db.getAllServerData()
        context = {
            "formusercreate": formUserCreate,
            "profile_page": 'active',
            "log_servers": log_servers,
            "error_add_user": ''
        }
    return render(request, "profile.html", context)


def user_login_view(request):
    if request.user.is_authenticated:
        return redirect("accounts:user_profile_view")
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if 'next' in request.POST:
                if not request.POST.get('next').__contains__('delete'):
                    return redirect(request.POST.get('next'))
                else:
                    return redirect("accounts:user_profile_view")
            else:
                return redirect("accounts:user_profile_view")
    else:
        form = AuthenticationForm()

    context = {
        "profile_page": 'active',
        "form": form
    }
    return render(request, "login.html", context)


def user_logout_view(request):
    if request.method == "POST":
        logout(request)
    return redirect("accounts:user_login_view")


@login_required(login_url="/account/login/")
def user_delete_view(request, name):
    try:
        u = User.objects.get(username=name)
        u.delete()
    except User.DoesNotExist:
        print("Cudnot delete user.")

    return redirect("accounts:user_profile_view")


@login_required(login_url="/account/login/")
def new_server_view(request):
    if request.method == "POST":
        form = FormNewServer(data=request.POST)
        if form.is_valid():
            if len(db.getServerData(form.cleaned_data['servername'])) > 0:
                context = {
                    "form": form,
                    "error": "Server name already exist. Please use  different one."
                }
                return render(request, "newserver.html", context)
            else:
                db.insertServerData(
                    form.cleaned_data['servername'],
                    form.cleaned_data['loglocation'],
                    form.cleaned_data['createdby']
                )
                return redirect("accounts:user_profile_view")
    else:
        form = FormNewServer()

    context = {
        "form": form,
        "error": ''
    }
    return render(request, "newserver.html", context)


@login_required(login_url="/account/login/")
def del_server_view(request, name):
    if request.method == 'POST':
        db.deleteServerData(name)
        return redirect("accounts:user_profile_view")
    return redirect("accounts:user_profile_view")